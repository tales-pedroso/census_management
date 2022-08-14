# -*- coding: utf-8 -*-
from setup import setup
from extract import extract
from transform import transform
from load import load

from config import CAT420RAWFOLDER, CAT420TRANSFOLDER


def main():
    #
    extract(first_lc_num = '',
            last_lc_num  = '',
            category_folder = CAT520RAWFOLDER)
    
    transform(first_lc_num = '',
              last_lc_num  = '',
              raw_category_folder   = CAT520RAWFOLDER,
              trans_category_folder = CAT520TRANSFOLDER)
    
    load(trans_category_folder = CAT520TRANSFOLDER)


