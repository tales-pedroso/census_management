# -*- coding: utf-8 -*-

# ! fill remaining values of DimDate after each batch of insert in FactLc420
# !!! insert line count on schema
from connect import connect
import csv


def get_sql_for_procedure(db_name, schema, proc_name):
    sql = f'EXEC [{db_name}].[{schema}].[{proc_name}]'
              
    return sql


def from_csv_into_staging2(conn, csv_path):
    '''
    csv is expected to be filled with null instead of empty string
    '''
    
    with open(csv_path, 'r', encoding = 'utf-8') as f:
        rows = f.readlines()
        
    for row in rows:
        print(row)
        
def get_sql_insert(csv_file):
    start = '''
            INSERT INTO dbo.StagingFactLc420(LcYear, LcNum, ObYear, ObNum, WasObCanceled)
            VALUES 
            '''
            
    string = start
        
    with open(csv_file, 'r', encoding = 'utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            line = '({LcYear}, {LcNum}, {ObYear}, {ObNum}, {WasObCanceled}),'.format(**row)
            string += line
    
    string = string[:-1] # take away last char in string, which is the trailing comma
    
    return string

def get_sql_delete(db_name, schema, table_name):
    string = f'DELETE FROM [{db_name}].[{schema}].[{table_name}]'
    return string
        
def pass_string_to_db(string):
    # has to be inside try because if it fails, the connection doesn't close
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(string)
        conn.commit()
    except Exception as e:
        raise e
    finally:
        cursor.close()
        conn.close()
    

if __name__ == '__main__':
    path = 'C:\\Users\\Tales\\Desktop\\census_management\\setup\\fact_table_test.csv'
    
    # update DimDate so that DaysAgo make sense
    string = get_sql_for_procedure('census', 'dbo', 'UpdateDaysAgo')
    pass_string_to_db(string)
    
    # update DimDate so that WorkDaysAgo make sense
    
    # delete everything from staging, the csv_file is the official backup
    # staging should be replaced by some procedure in the future
    string = get_sql_delete('census', 'dbo', 'StagingFactLc420')
    pass_string_to_db(string)
    
    # insert into staging
    string = get_sql_insert(path)
    pass_string_to_db(string)
    
    # get which obs are new comparing staging and factable
    
    # get which obs were canceled since the last update
    
    # merge staging and fact table
    sql = get_sql_for_procedure('census', 'dbo', 'MergeStagingAndFactTable')
    pass_string_to_db(sql)
    
    # prompt user to get the obNumber of new obs
    
    # (future) get the list of LCs that need to be extracted for the day


   