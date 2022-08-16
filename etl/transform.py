# -*- coding: utf-8 -*-
from time import time
from glob import glob
from os import sep
import pandas as pd
from setup import get_folder_by_layer_name
from config import (STAND_FILE_NAME, WANTED_INTERVALS, COLUMNS_IN_CSV_FILES,
                   ROWS_INDEXES, DATA_INDEXES, TRANS_FILE_NAME, CANCELED_VALUES,
                   MONTHS)

# it would be more efficient if we could traverse the string in its order
# getting the (first row, first col), then (second row, second col)
# (third row, third col) and so on, since the string is in that order
# that could be tested later after profiling

#==============================================================================
# FUNCTIONS TO TRANSFORM FROM RAW TO STANDARDIZED
        
def list_txt_files(folder):
    txt_files = glob(folder + sep + '*.txt')
    return txt_files

def list_rows_in_page(page):
    rows_list = [page[row_index] for row_index in ROWS_INDEXES]
    return rows_list

def get_row_values_sep_by_comma(row):
    values_list = [row[data_index] for data_index in DATA_INDEXES]
    values_str = ','.join(values_list)
    values_str += '\n' # add new line to concatenate every row
    return values_str

def save_csv_to_stand(rows_sep_by_comma):
    stand_folder = get_folder_by_layer_name('standardized')
    
    path = stand_folder + sep + STAND_FILE_NAME + '.csv'
    
    with open(path, 'w', encoding = 'utf-8') as f:
        f.write(rows_sep_by_comma)
        
def create_header():
    header = ','.join(COLUMNS_IN_CSV_FILES)
    header += '\n'
    
    return header
    
def get_txt_file_paths_from_raw():
    raw_folder = get_folder_by_layer_name('raw')
    txt_file_paths = list_txt_files(raw_folder)
    
    return txt_file_paths

def process_txt_files_into_csv_string(txt_files):
    rows_sep_by_comma = create_header() # start by setting up the header
    
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding = 'utf-8') as f:
            page = f.read()   # page is a string ready get sliced
            
        rows = list_rows_in_page(page)  # list of strings, each with row data
        
        for row in rows:
            one_row_sep_by_comma = get_row_values_sep_by_comma(row)
            
            rows_sep_by_comma += one_row_sep_by_comma # accumulating into the final variable
            
    return rows_sep_by_comma


def from_raw_to_stand():
    txt_file_paths = get_txt_file_paths_from_raw()
    
    rows_sep_by_comma = process_txt_files_into_csv_string(txt_file_paths)
    
    # after all in-memory concatenation, save it to disk
    save_csv_to_stand(rows_sep_by_comma)
    
    
#==============================================================================
# FUNCTIONS TO TRANSFORM FROM STANDARDIZED TO TRANSFORMED
    
def strip_leading_zeros(series):
    return series.str.lstrip('0')
    
def change_spaces_into_nulls(series, how_many_spaces):
    space = ' ' * how_many_spaces
    return series.replace(space, 'NULL')

def change_words_into_ones(series, *words):
    for word in words:
        series = series.replace(word, '1')
        
    return series

def take_away_values_outside_this_range(df, col, intervals):
    conditions = False # initializing
    
    for interval in intervals:
        start  = int(interval[0])
        finish = int(interval[1])
        
        conditions |= df[col].between(start, finish)
    
    df = df[conditions]
    
    return df

def get_df_from_stand():
    stand_folder = get_folder_by_layer_name('standardized')
    path_to_stand = stand_folder + sep + STAND_FILE_NAME + '.csv'
    
    df = pd.read_csv(path_to_stand, 
                     dtype = {'LcYear': 'int64',
                              'LcNum': 'int64',
                              'LineCount': 'object',
                              'ObYear': 'object',
                              'ObNum': 'object',
                              'WasObCanceled': 'object'})
    return df

def process_df(df):
    # needs to enforce that only lcs between WANTED INTERVALS 
    # pass to the next stage
    df = take_away_values_outside_this_range(df, 'LcNum', WANTED_INTERVALS)
    
    # column transformations
    # it is throwing a warning 
    # cf https://realpython.com/pandas-settingwithcopywarning/
    df['LineCount'] = strip_leading_zeros(df.LineCount)
    df['ObYear'] = change_spaces_into_nulls(df.ObYear, 4)
    df['ObNum'] = change_spaces_into_nulls(df.ObNum, 6)
    df['WasObCanceled'] = change_spaces_into_nulls(df.WasObCanceled, 6)
    df['WasObCanceled'] = change_words_into_ones(df.WasObCanceled, CANCELED_VALUES)
    
    return df

def save_df_to_trans(df):
    trans_folder = get_folder_by_layer_name('transformed')
    path_to_trans = trans_folder + sep + TRANS_FILE_NAME + '.csv'
    
    df.to_csv(path_to_trans, index = False, quoting = None)
    
def from_stand_to_trans():
    df = get_df_from_stand()
    
    df = process_df(df)
                     
    save_df_to_trans(df)

    
def transform():
    # get_folder_by_layer_name('raw')
    # get_folder_by_layer_name('standardized')
    # get_folder_by_layer_name('transformed')
    start_raw = time()
    from_raw_to_stand()
    
    end_raw = time()
    total_raw = end_raw - start_raw
    
    print(f'Finished transforming raw into standardized. Time spent: {total_raw}')
    
    start_stand = time()
    from_stand_to_trans()
    
    end_stand = time()
    total_stand = end_stand - start_stand
    
    print(f'Finished transforming standardized into transformed. Time spent: {total_stand}')
    
#################################################################################    
# Functions related to Ob_date

def correct_one_date(date_in_str):
    '''
    assumes the given date is from 2000 to 2099
    '''
    # always a 7-char long string when it comes from conob
    if len(date_in_str) != 7:
        raise Exception(f'Given string is not a 7-char long string. Got {date_in_str}')
        
    d = date_in_str[0:2]
    m = MONTHS.get(date_in_str[2:5])
    y = '20' + date_in_str[5:7]
    
    return '-'.join([y, m, d])

def get_dates_into_db_format(raw_dates):
    # database is always yyyy-mm-dd
    # siafi is always dd-mm-yy
    processed_dates = [*map(correct_one_date, raw_dates)]
    return processed_dates


if __name__ == '__main__':
    df = get_df_from_stand()