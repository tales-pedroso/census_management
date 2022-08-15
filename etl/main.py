# -*- coding: utf-8 -*-
from setup import setup
from extract import extract, mock_extract
from transform import transform
from load import load
from config import FIRST_LC_NUM, LAST_LC_NUM


# needs to delete stuff after everything is said and done

def main():
    #
    setup()
    
    extract(FIRST_LC_NUM, LAST_LC_NUM)
    
    transform()
    
    load()

if __name__ == '__main__':
    main()
