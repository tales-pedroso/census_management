# -*- coding: utf-8 -*-
from setup import setup
from get_lc_needs import get_lc_needs
from ob_date import get_ob_dates
from pages import Scraper

# needs to delete stuff from data lake after everything is said and done

def main():
    #
    setup()
    
    scraper = Scraper()
    
    get_lc_needs(scraper) # it should be called etl_lc_needs
    
    get_ob_dates(scraper) # it should be called etl_ob_dates

if __name__ == '__main__':
    # set siafi at initial page first
    main()
