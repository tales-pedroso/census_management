# -*- coding: utf-8 -*-


import pyautogui as p
import time
from pages import Scraper
from extract import start_siafi

if __name__ == '__main__':
    scraper = Scraper()
    start_siafi(scraper)


    time.sleep(2)
    coords = p.position()
    print(coords)
    p.hotkey('alt', 'tab')