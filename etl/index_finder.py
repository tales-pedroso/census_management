# -*- coding: utf-8 -*-

from re import search
from os import sep



def index_finder(string, to_find):
    pattern = to_find
    match = search(pattern, string)
    indexes = match.span()
    return indexes

if __name__ == '__main__':
    folder = 'C:\\Users\\Tales\\desktop\\census_management\\test'
    file_name = 'siafi_menu'
    path = folder + sep + file_name + '.txt'
    
    with open(path, 'r', encoding = 'utf-8') as f:
        string = f.read()
        
        
        
    to_find1 = 'COMANDO: ______________________________________________________________________' 
    # to_find2 = 'LC'
    # to_find3 = '520156'
    # to_find4 = '08Jun2022'
    # to_find5 = '006594'
    # to_find6 = '  7.273.310,14'    
    # to_find7 = '2022O'
    # to_find8 = 'OB'
    # to_find9 = '852718'
    # to_find10 = 'CANC.P'
    # to_find11 = 'F'
    
    # to_find = (to_find1, to_find2, to_find3, to_find4, to_find5, to_find6, 
    #            to_find7, to_find8, to_find9, to_find10, to_find11)
    
    #[print(index_finder(string, i)) for i in to_find]
    
    indexes = index_finder(string, to_find1)
    print(indexes)
    
