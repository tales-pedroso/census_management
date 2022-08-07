'''
extract LCs from Siafi HoD (legacy system)
'''

import pyautogui as p
import pyperclip
import time
from window_manager import WindowMgr
from os import sep
from collections import deque

RAW_FOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\raw'

class Scraper:
    hod_name = 'Terminal 3270'
    from_point = (470,  400)
    to_point   = (1020, 400)
    
    def __init__(self):
        pass
    
    def write_at(self, x, y, text):
        text = str(text)
        
        p.click(x, y)
        p.write(text)
        
    def set_window_to_foreground(self, window_partial_name):
        w = WindowMgr()
        w.find_window_wildcard(f'.*{window_partial_name}.*')
        w.set_foreground()
        
    def enter(self):
        p.press('enter')
        
    def f2(self):
        p.press('f2')
        
    def f4(self):
        p.press('f4')
        
    def f8(self):
        p.press('f8')
        
    def f12(self):
        p.press('f12')
        
    def swipe(self):
        p.moveTo(self.from_point)
        p.dragTo(self.to_point)
        p.hotkey('ctrl', 'c')
        string = pyperclip.paste()
        return string
     


    
if __name__ == '__main__':
    # get a hold of mouse
    hod = HoD()
    
    
    hod.go_to_hod()
    
    string = hod.swipe()
    conlc = ConlcInitialPage(string)
    
    if conlc.validate():
        conlc.get_
        conlc.save_as_txt(RAW_FOLDER, '1')
    
    
    # choose_one_lc = Job()
    # choose_one_lc.alt_tab()
    # conlc = Conlc(choose_one_lc.get_string())
    
    # # time.sleep(3)
    # # p.hotkey('alt', 'tab')
    # # p.position()
    
    # OUTPUT_DIR = 'C:/Users/Tales/Desktop/census_management'
    # import os
    
    # with open(OUTPUT_DIR + os.sep + str('test') + '.txt', 'w', encoding = 'utf-8') as f:
    #     f.write(conlc.string)

    







    
