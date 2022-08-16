# -*- coding: utf-8 -*-
from extract import extract_lc_needs
from transform import transform
from load import load
from config import FIRST_LC_NUM, LAST_LC_NUM

def get_lc_needs(scraper):
    extract_lc_needs(scraper, FIRST_LC_NUM, LAST_LC_NUM)
    
    transform()
    
    load()


