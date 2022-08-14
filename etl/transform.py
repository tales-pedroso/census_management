# -*- coding: utf-8 -*-
from config import CAT520RAWFOLDER
from config import CAT520STANDFOLDER
from glob import glob
from os import sep
import pandas as pd



# it would be more efficient if we could traverse the string in its order
# getting the (first row, first col), then (second row, second col)
# (third row, third col) and so on, since the string is in that order
# that could be tested later after profiling

ROWS_INDEXES = (slice(496, 571),  #1st row
                slice(578, 653),  #2nd row
                slice(660, 735),  #3rd row ...
                slice(742, 817),
                slice(824, 899),
                slice(906, 981),
                slice(988, 1063),
                slice(1070, 1145),
                slice(1152, 1227),
                slice(1234, 1309),
                slice(1316, 1391),
                slice(1398, 1473),
                slice(1480, 1555),
                slice(1562, 1637),
                slice(1644, 1719))

DATA_INDEXES = (slice(0, 4),    # lc year       --> 2022
               #slice(4, 6),    # "LC" constant --> LC   --> we don't want that info
                slice(6, 12),   # lc number     --> 520296
               #slice(13, 22),  # lc date       --> 01Fev2022 --> we don't want that info
                slice(23, 29),  # line count    --> 000537
               #slice(38, 52),  # value         --> 1.231.186,65 --> we don't want that info
                slice(54, 58),  # ob year       --> 2022
               #slice(58, 60),  # "OB" constant --> OB --> we don't want that info
                slice(60, 66),  # ob number     --> 831021
                slice(67, 73))  # was_canceled? --> CANC.P 
               #slice(74, 75))  # was_closed?   --> F --> we don't want that info
               

        
def list_txt_files(folder):
    txt_files = glob(folder + sep + '*.txt')
    return txt_files

def list_rows_in_page(page, rows_indexes = ROWS_INDEXES):
    rows_list = [page[row_index] for row_index in rows_indexes]
    return rows_list

def get_row_values_sep_by_comma(row, data_indexes = DATA_INDEXES):
    values_list = [row[data_index] for data_index in data_indexes]
    values_str = ','.join(values_list)
    values_str += '\n' # add new line to concatenate every row
    return values_str

def save_as_csv(rows_sep_by_comma, conf_folder = CAT520STANDFOLDER):
    path = conf_folder + sep + 'standardized.csv'
    
    with open(path, 'w', encoding = 'utf-8') as f:
        f.write(rows_sep_by_comma)
    
def from_raw_to_stand(raw_folder = CAT520RAWFOLDER, 
                      stand_folder = CAT520STANDFOLDER):
    # this is going to accumulate the values of rows
    rows_sep_by_comma = 'LcYear,LcNum,LineCount,ObYear,ObNum,WasObCanceled\n' 
    
    txt_files = list_txt_files(raw_folder)
    
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding = 'utf-8') as f:
            page = f.read()
            
        rows = list_rows_in_page(page)
        
        for row in rows:
            one_row_sep_by_comma = get_row_values_sep_by_comma(row)
            
            rows_sep_by_comma += one_row_sep_by_comma
            
    #########
    save_as_csv(rows_sep_by_comma)
    
def strip_leading_zeros(series):
    return series.str.lstrip('0')
    
def change_spaces_into_nulls(series, how_many_spaces):
    space = ' ' * how_many_spaces
    return series.replace(space, 'NULL')

def change_words_into_ones(series, *words):
    for word in words:
        series = series.replace(word, '1')
        
    return series

def take_away_values_outside_this_range(df, col, start, finish):
    int_start   = int(start)
    int_finish  = int(finish)
    
    #df[col] = df[col].astype('int32')
    boolean_response = df[col].between(int_start, int_finish)
    df2 = df[boolean_response]
    #df[col] = df[col].astype('object')
    
    return df2
    
    
#################################################################################
    
if __name__ == '__main__':
    first_lc_num = '520160'
    last_lc_num  = '520999'
    
    
    # from_raw_to_stand()
    
    # LcYear is always a 4-digit number
    # LcNum is always a 6-digit number
    # LineCount is always a number >= 1
    # ObYear may be a 4-digit number or 4 spaces
    
    df = pd.read_csv(CAT520STANDFOLDER + sep + 'standardized.csv', 
                     dtype = {'LcYear': 'int64',
                              'LcNum': 'int64',
                              'LineCount': 'object',
                              'ObYear': 'object',
                              'ObNum': 'object',
                              'WasObCanceled': 'object'})
    
    # needs to enforce that only lcs between min_lc_num and max_lc_num get
    # to the next stage
                     
    df = take_away_values_outside_this_range(df, 'LcNum', 
                                             first_lc_num, 
                                             last_lc_num)
    
    
    df['LineCount'] = strip_leading_zeros(df.LineCount)
    df['ObYear'] = change_spaces_into_nulls(df.ObYear, 4)
    df['ObNum'] = change_spaces_into_nulls(df.ObNum, 6)
    df['WasObCanceled'] = change_spaces_into_nulls(df.WasObCanceled, 6)
    df['WasObCanceled'] = change_words_into_ones(df.WasObCanceled, ('CANC.P', 'CANC.T'))
    
    # needs a function to take away from standardized and put it in transformed
    