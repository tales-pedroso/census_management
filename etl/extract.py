# -*- coding: utf-8 -*-
'''
extract LCs from Siafi HoD (legacy system)
'''

from window_manager import WindowMgr
from os import sep
from pages import SiafiInitialPage1, SiafiLogin, SiafiMenu, ConlcInitialPage, ConlcDataPage, ConlcEntrance
from credentials import CPF, SIAFI_PASS
from config import SYSTEM_NAME, SYSTEM_YEAR, CONLC_COMMAND
from pages import Scraper

# ONE PAGE FUNCTIONS
# They could be generalized into classes, but they would get harder to read

def start_siafi(scraper):
    hod_name = 'Terminal 3270'
    scraper.set_window_to_foreground(hod_name)

def set_system_name_at_siafi_initial_page(scraper, system_name = SYSTEM_NAME):
    siafi_initial_page1 = SiafiInitialPage1(scraper)
    
    # read and validate
    if not siafi_initial_page1.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_initial_page1}')
    
    # set
    siafi_initial_page1.set_system_name(system_name)
    
    # advance and validate
    siafi_initial_page1.advance()
    if not siafi_initial_page1.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {siafi_initial_page1}')
        
    # report
    print('Inserted "sf" at Siafi\'s Initial Page.')
    
def set_credentials_at_siafi_login(scraper, cpf = CPF, 
                                   siafi_pass = SIAFI_PASS, system_year = SYSTEM_YEAR):
    siafi_login = SiafiLogin(scraper)
    
    # read and validate
    if not siafi_login.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_login}')
    
    # set
    siafi_login.set_cpf(cpf)
    siafi_login.set_pass(siafi_pass)
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
    
def set_conlc_at_siafi_menu(scraper, conlc_command = CONLC_COMMAND):
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
    
def download_conlc_data_page_as_txt(scraper, last_lc_num, category_folder):
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
        conlc_data_page.to_txt(category_folder, counter)
        
        # go to next page
        conlc_data_page.advance()
        
        # validate that it actually went to the next page
        if not conlc_data_page.wait_until_it_leaves_page('current_page'):
            raise Exception(f'Failed to move to the next page at {conlc_data_page}.' )
        
        conlc_data_page.increment_page_num()
        if not conlc_data_page.swipe_until_it_matches_other('current_page'):
            raise Exception(f'Failed to validate the next page at page object {conlc_data_page}')
            
    '''
    # !!! try this new implementation
    # it stopped advancing, but we should still save the last page
    # prepare counter to be used as file name
    counter = str(int(counter) + 1)
        
    # save
    conlc_data_page.to_txt(raw_folder, counter)


    '''        
        
    # if only the first page is relevant, save its data
    if counter == '0':
        # prepare counter to be used as file name
        counter = str(int(counter) + 1)
        
        # save
        conlc_data_page.to_txt(category_folder, counter)

    print(f'Downloaded {counter} LCs to {category_folder}')

def extract(first_lc_num, last_lc_num, category_folder):
    scraper = Scraper()
    
    start_siafi(scraper)
    
    set_system_name_at_siafi_initial_page(scraper, SYSTEM_NAME)
    
    set_credentials_at_siafi_login(scraper, CPF, SIAFI_PASS, SYSTEM_YEAR)
    
    set_conlc_at_siafi_menu(scraper, CONLC_COMMAND)
    
    set_first_lc_num(scraper, first_lc_num)
    
    download_conlc_data_page_as_txt(scraper, last_lc_num, category_folder)


    







    
