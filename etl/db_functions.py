# -*- coding: utf-8 -*-
from credentials import DATABASE, SCHEMA
import csv
from config import COLUMNS_IN_CSV_FILES, TRANS_FILE_NAME
from setup import get_folder_by_layer_name
from os import sep


def get_sql_for_procedure(proc_name):
    sql = f'EXEC [{DATABASE}].[{SCHEMA}].[{proc_name}]'
              
    return sql

def get_columns_sep_by_comma():
    col_sep_by_comma = ','.join(COLUMNS_IN_CSV_FILES)
    return col_sep_by_comma
        
def get_sql_for_insert(csv_file_path, table_name):
    # this needs to be generalized later
    cols = get_columns_sep_by_comma()
    start = f'''
             INSERT INTO {SCHEMA}.{table_name}({cols})
             VALUES 
             '''
            
    string = start
        
    with open(csv_file_path, 'r', encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = '({LcYear}, {LcNum}, {LineCount}, {ObYear}, {ObNum}, {WasObCanceled}),'.format(**row)
            string += line
    
    string = string[:-1] # take away last char in string, which is the trailing comma
    
    return string

def get_sql_to_update_1_ob_date(one_ob_year, one_ob_num, one_ob_date):
    '''
    probably not efficient
    '''
    sql = f'''UPDATE [{DATABASE}].[{SCHEMA}].[FactLc]
              SET   ObDate = '{one_ob_date}'
              WHERE ObYear = {one_ob_year} AND ObNum = {one_ob_num}
           '''
    return sql

# def update_many_ob_dates(conn, zip_ob_years_nums_and_dates):
#     cursor = conn.cursor()
    
#     try:
#         for one_ob_year, one_ob_num, one_ob_date in zip_ob_years_nums_and_dates:
#             sql = get_sql_to_update_1_ob_date(one_ob_year, one_ob_num, one_ob_date)
        
#             cursor.execute(sql)
        
#         cursor.commit()
#     except Exception as e:
#         raise e
        
#     finally:
#         cursor.close()
        
        
    

def get_sql_for_truncate(table_name):
    string = f'DELETE FROM [{DATABASE}].[{SCHEMA}].[{table_name}]'
    return string
        
def pass_string_to_db(string, conn):
    cursor = conn.cursor()
    try:
        #cursor.fast_executemany = True
        #cursor.executemany(string)
        cursor.execute(string)
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        
def pass_string_to_db_with_return(string, conn):
    cursor = conn.cursor()
    try:
        cursor.execute(string)
        data = cursor.fetchall()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        
    return data
        
def update_days_ago_column(conn):
    string = get_sql_for_procedure('UpdateDaysAgo')
    pass_string_to_db(string, conn)
    
    print('Updated DaysAgo Column in DimDate table')
    

def update_work_days_ago_column(conn):
    string = get_sql_for_procedure('UpdateWorkDaysAgo')
    pass_string_to_db(string, conn)
    
    print('Updated WorkDaysAgo Column in DimDate table')
    
def truncate_staging(conn):
    string = get_sql_for_truncate('StagingFactLc')
    pass_string_to_db(string, conn)
    
    print('Trucated StagingFactLc table')
    
def insert_into_staging_from_csv(conn):
    folder = get_folder_by_layer_name('transformed')
    csv_file_path = folder + sep + TRANS_FILE_NAME + '.csv'
    
    string = get_sql_for_insert(csv_file_path, 'StagingFactLc')
    pass_string_to_db(string, conn)
    
    print('Inserted data from transformed into StagingFactLc table')

def merge_staging_and_fact_tables(conn):
    string = get_sql_for_procedure('MergeStagingAndFactTable')
    pass_string_to_db(string, conn)
    
    print('Merged Staging and Fact tables')

def get_obs_that_dont_have_ob_date(conn):
    string = get_sql_for_procedure('GetObsThatDontHaveObDate')
    obs = pass_string_to_db_with_return(string, conn)
    
    print('Got the Obs that don\'t have Ob date just yet.')
    return obs
    
