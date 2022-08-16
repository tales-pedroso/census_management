# -*- coding: utf-8 -*-

from connect import connect
from time import time
from db_functions import (update_days_ago_column, update_work_days_ago_column,
                          truncate_staging, insert_into_staging_from_csv,
                          merge_staging_and_fact_tables, get_sql_to_update_1_ob_date)

def load():
    start = time()
    
    conn = connect()
    
    # update DimDate so that DaysAgo make sense
    update_days_ago_column(conn)
    
    # update DimDate so that WorkDaysAgo make sense
    update_work_days_ago_column(conn)
    
    # truncate staging table, so that we can upsert the most recent data
    truncate_staging(conn)
    
    # insert updated data into Staging table
    insert_into_staging_from_csv(conn)
    
    # merge staging and fact table
    merge_staging_and_fact_tables(conn)
    
    conn.close()
    
    end = time()
    
    total = end - start
    print(f'Finished loading data into database. Time spent: {total}')
   
def update_many_ob_dates(zip_ob_years_nums_and_dates):
    conn = connect()
    cursor = conn.cursor()
    
    try:
        for one_ob_year, one_ob_num, one_ob_date in zip_ob_years_nums_and_dates:
            sql = get_sql_to_update_1_ob_date(one_ob_year, one_ob_num, one_ob_date)
        
            cursor.execute(sql)
        
        cursor.commit()
    except Exception as e:
        raise e
        
    finally:
        cursor.close()
