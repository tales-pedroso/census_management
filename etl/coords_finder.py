# -*- coding: utf-8 -*-


import pyautogui as p
import time
from extract import Scraper

if __name__ == '__main__':
    scraper = Scraper()
    
    scraper.set_window_to_foreground(scraper.hod_name)

    time.sleep(2)
    coords = p.position()
    print(coords)
    p.hotkey('alt', 'tab')