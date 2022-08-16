# -*- coding: utf-8 -*-
from db_functions import get_obs_that_dont_have_ob_date
from connect import connect
from extract import extract_ob_dates
from transform import get_dates_into_db_format
from load import update_many_ob_dates


def get_ob_dates(scraper): # main function. should be called etl_ob_dates
    # possibly very inneficient, but it gets the job done
    # multiple updates and zip construction need to change
    conn = connect()
    obs = get_obs_that_dont_have_ob_date(conn) # this brings both ObYear and ObNum columns from database
    
    # what happens if the result set is empty? obs is an empty list
    if not obs:
        print('There are no OBs without dates')
        return
    
    obs_for_siafi = get_obs_into_siafi_format(obs)
    conn.close()
    
    raw_dates = extract_ob_dates(scraper, obs_for_siafi)
    
    processed_dates = get_dates_into_db_format(raw_dates)
    
    ob_years = []
    ob_nums = []
    
    for row in obs:
        ob_years.append(row[0])
        ob_nums.append(row[1])
        
    zip_ob_years_nums_and_dates = zip(ob_years, ob_nums, processed_dates)
    
    update_many_ob_dates(zip_ob_years_nums_and_dates)

def get_obs_into_siafi_format(obs):
    '''
    assumes we only want obs from the current year
    '''
    obs_for_siafi = [str(row[1]) for row in obs]
    return obs_for_siafi
