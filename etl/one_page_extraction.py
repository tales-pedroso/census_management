# -*- coding: utf-8 -*-
from pages import Scraper
from extract import start_siafi

if __name__ == '__main__':
    scraper = Scraper()
    
    start_siafi(scraper)
    string = scraper.swipe()
    
    folder = 'C:\\Users\\Tales\\Desktop\\census_management\\test\\'
    ext = '.txt'
    file_name = 'conob_data_page_last_page' # update this and go
    
    with open(folder + file_name + ext, 'w', encoding = 'utf-8') as f:
        f.write(string)
        
    scraper.alt_tab()
    
    
    

