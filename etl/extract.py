# -*- coding: utf-8 -*-
'''
extract LCs from Siafi HoD (legacy system)
'''

from pages import (SiafiInitialPage1, SiafiLogin, SiafiMenu, ConlcDataPage, ConlcEntrance,
                   ConobEntrance, ConobDataPage)
from credentials import CPF, SIAFI_PASS
from config import SYSTEM_NAME, SYSTEM_YEAR, CONLC_COMMAND, CONOB_COMMAND, SCREEN_NAME
from setup import get_folder_by_layer_name
from time import time

# ONE PAGE FUNCTIONS
# They could be generalized into classes
# they always take a page object
# they always validata they are in the right page
# they do something in that page
# then they move out of that page and validate
# they always throw exceptions (timeout exception, basically)

def start_siafi(scraper):
    scraper.set_window_to_foreground(SCREEN_NAME)

def set_system_name_at_siafi_initial_page(scraper):
    siafi_initial_page1 = SiafiInitialPage1(scraper)
    
    # read and validate
    if not siafi_initial_page1.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_initial_page1}')
    
    # set
    siafi_initial_page1.set_system_name(SYSTEM_NAME)
    
    # advance and validate
    siafi_initial_page1.advance()
    if not siafi_initial_page1.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {siafi_initial_page1}')
        
    # report
    print('Inserted "sf" at Siafi\'s Initial Page.')
    
def set_credentials_at_siafi_login(scraper):
    siafi_login = SiafiLogin(scraper)
    
    # read and validate
    if not siafi_login.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_login}')
    
    # set
    siafi_login.set_cpf(CPF)
    siafi_login.set_pass(SIAFI_PASS)
    siafi_login.submit()
    
    if not siafi_login.wait_until_input_appears():
        raise Exception(f'Failed to find the input to type the system year. Maybe the password needs to change. Page object: {siafi_login}')
    siafi_login.set_system_year(SYSTEM_YEAR)
    
    # advance and validate
    siafi_login.advance()
    if not siafi_login.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {siafi_login}')
    
    # report
    print("Inserted credentials at Siafi\'s login page.")
    
def set_conlc_at_siafi_menu(scraper):
    siafi_menu = SiafiMenu(scraper)
    
    # read and validate
    if not siafi_menu.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_menu}')
    
    # set
    siafi_menu.set_command(CONLC_COMMAND)
    
    # advance and validate
    siafi_menu.advance()
    if not siafi_menu.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {siafi_menu}')
    
    # report
    print(f'Inserted {CONLC_COMMAND} at Siafi\'s menu.')
    
def set_first_lc_num(scraper, first_lc_num):
    conlc_entrance = ConlcEntrance(scraper)
    
    # read and validate
    if not conlc_entrance.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {conlc_entrance}')
    
    # set
    conlc_entrance.set_lc_num(first_lc_num)
    
    # advance and validate
    conlc_entrance.advance()
    if not conlc_entrance.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {conlc_entrance}')
    
    # report
    print(f'Inserted {first_lc_num} as the first LC num to search for')
    
def download_conlc_data_page_as_txt(scraper, last_lc_num, raw_folder):
    # initialize
    counter = '0'
    
    # read and validate
    conlc_data_page = ConlcDataPage(scraper, last_lc_num)
    if not conlc_data_page.swipe_until_it_matches_other('current_page'):
        raise Exception(f'Failed to validate the page object {conlc_data_page}')
    
    # iterate and save on disk
    while not conlc_data_page.should_i_stop_advancing():
        # prepare counter to be used as file name
        counter = str(int(counter) + 1)
        
        # save
        conlc_data_page.to_txt(raw_folder, counter)
        
        # go to next page
        conlc_data_page.advance()
        
        # validate that it actually went to the next page
        if not conlc_data_page.wait_until_it_leaves_page('current_page'):
            raise Exception(f'Failed to move to the next page at {conlc_data_page}.' )
        
        conlc_data_page.increment_page_num()
        if not conlc_data_page.swipe_until_it_matches_other('current_page'):
            raise Exception(f'Failed to validate the next page at page object {conlc_data_page}')
            
    # it stopped advancing, but we should still save the last page
    # prepare counter to be used as file name
    counter = str(int(counter) + 1)
        
    # save
    conlc_data_page.to_txt(raw_folder, counter)
    
    # report
    print(f'Downloaded {counter} LC pages to {raw_folder}')

def extract_lc_needs(scraper, first_lc_num, last_lc_num):
    print(f'Starting extraction from {first_lc_num} to {last_lc_num}')
    start = time()
    
    raw_folder = get_folder_by_layer_name('raw')
    
    start_siafi(scraper)
    
    set_system_name_at_siafi_initial_page(scraper)
    
    set_credentials_at_siafi_login(scraper)
    
    set_conlc_at_siafi_menu(scraper)
    
    set_first_lc_num(scraper, first_lc_num)
    
    download_conlc_data_page_as_txt(scraper, last_lc_num, raw_folder)
    
    end = time()
    total_time = end - start
    
    print(f'Finished LC extraction. Time spent: {total_time}')
    
def mock_extract():
    print('Pretended to finish extraction')
    
#==============================================================================

def leave_conlc_data_page(scraper):
    # it is not always the case that goes back to Conlc entrance. 
    # if the system is left hanging, it moves all the way up to login again
    conlc_data_page = ConlcDataPage(scraper)
    
    # assert we are still on Conlc data page
    if not conlc_data_page.swipe_until_it_matches_main():
        raise Exception(f'Expected to be in page object {conlc_data_page}, but it is not')
    
    # go back and validate
    conlc_data_page.go_back()
    if not conlc_data_page.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of page object {conlc_data_page}')
        
    print('Moved out of Conlc data page')
    
def leave_conlc_entrance(scraper):
    conlc_entrance = ConlcEntrance(scraper)
    
    # assert we are still on Conlc entrance
    if not conlc_entrance.swipe_until_it_matches_main():
        raise Exception(f'Expected to be in page object {conlc_entrance}, but it is not')
    
    # go back and validate
    conlc_entrance.go_back()
    if not conlc_entrance.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of page object {conlc_entrance}')
        
    print('Moved out of Conlc entrance')
    
def set_conob_at_siafi_menu(scraper):
    siafi_menu = SiafiMenu(scraper)
    
    # read and validate
    if not siafi_menu.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_menu}')
    
    # set
    siafi_menu.set_command(CONOB_COMMAND)
    
    # advance and validate
    siafi_menu.advance()
    if not siafi_menu.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {siafi_menu}')
    
    # report
    print(f'Inserted {CONOB_COMMAND} at Siafi\'s menu.')
    
def set_ob_num(scraper, ob_num):
    conob_entrance = ConobEntrance(scraper)
    
    # read and validate
    if not conob_entrance.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {conob_entrance}')
    
    # set
    conob_entrance.set_ob_num(ob_num)
    
    # advance and validate
    conob_entrance.advance()
    if not conob_entrance.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {conob_entrance}')
    
    # report
    print(f'Inserted {ob_num} at page object {conob_entrance}')
    
def get_ob_date_and_go_back(scraper, ob_num):
    conob_data_page = ConobDataPage(scraper, ob_num)
    
    # read and validate
    if not conob_data_page.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {conob_data_page}')
        
    if not conob_data_page.is_wanted_ob_on_page():
        raise Exception(f'Failed to find {ob_num} as the first OB on page.')
        
    # get
    ob_date = conob_data_page.get_date_of_first_ob_on_page()
    
    # report
    print(f'Got {ob_date} for {ob_num}')
    
    # leave and validate
    conob_data_page.go_back()
    if not conob_data_page.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to leave the page object {conob_data_page}')
        
    # report
    print(f'Left the page object {conob_data_page}')
    return ob_date
    
def get_multiple_ob_dates(scraper, obs_for_siafi):
    # assumes we start at conob entrance
    raw_dates = []
    
    for ob_num in obs_for_siafi:
        set_ob_num(scraper, ob_num)
        ob_date = get_ob_date_and_go_back(scraper, ob_num)
        raw_dates.append(ob_date)
        
    return raw_dates
    
def extract_ob_dates(scraper, obs_for_siafi):
    # assumes it is in Conlc Data Page
    print('Starting extracion of OB dates in Siafi.')
    
    start_siafi(scraper)
    
    leave_conlc_data_page(scraper) 
    
    set_conob_at_siafi_menu(scraper)
    
    raw_dates = get_multiple_ob_dates(scraper, obs_for_siafi)
    
    print('Finished extraction of OB dates in Siafi')
    # leaves user in ConobEntrance
    
    return raw_dates
    
    
    
    
    
    
    
    
    
    







    
