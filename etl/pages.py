# -*- coding: utf-8 -*-    
import pyautogui as p
from time import sleep, time
from os import sep
import pdb
from window_manager import WindowMgr
from pyperclip import paste

#==============================================================================
# DECORATORS

def twenty_times(func):
    def wrapper(*args, **kwargs):
        counter = 0
        output = None
        
        while counter < 20:
            counter += 1
            output = func(*args, **kwargs)
            
            if output is None:
                continue
            else:
                return output
    return wrapper

def poll_until_10_seconds(func):
    def wrapper(*args, **kwargs):
        interval = 0.1
        elapsed = 0
        start = time()
        
        while elapsed < 10:
            output = func(*args, **kwargs)
            if output is None:
                sleep(interval)
                elapsed = time() - start
            else:
                return output
        
        raise Exception(f'Timeout. {func} has taken more than 10 seconds to return a value')
            
    return wrapper

#==============================================================================
# HELPER FUNCTIONS

def strip_and_no_dots(string):
    no_dots = string.replace('.', '')
    stripped_and_no_dots = no_dots.strip()
    
    return stripped_and_no_dots

#==============================================================================
# CLASSES

class Scraper:
    from_point = (470,  400)
    to_point   = (1020, 400)
        
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
        string = paste()
        return string

######

class Page():
    def __init__(self, scraper):
        self.scraper = scraper
        
    def _get_mapping(self, name, type_):
        valid_types = ('validation', 'setter', 'getter')
        
        if type_ not in valid_types:
            raise ValueError(f'Invalid type_ given. Got {type_}')
        
        obj = 'self.' + type_        # a string called self.validation or self.mapper
        list_of_mappings = eval(obj) # the actual reference to self.validation or self.mapper
        
        for mapping in list_of_mappings:
            if mapping['name'] == name:
                return mapping
        
        # if list is exhausted and the name wasn't found, throw an error
        raise ValueError(f'Invalid name given. Got {name}')
        
    def _validate(self, string, name):
        '''
        type_ is either main or other
        '''
        mapping     = self._get_mapping(name, 'validation')
        slice_      = mapping['slice_']
        to_validate = mapping['to_validate']
        processing  = mapping.get('processing', None)
        
        if processing is None:
            is_valid = string[slice_] == to_validate
        else:
            raw_string = string[slice_]
            processed_string = processing(raw_string)
            is_valid = processed_string == to_validate
            
        return is_valid
        
    def _validate_main(self, string):
        is_valid = self._validate(string, 'main')
        return is_valid
        
    def _validate_other(self, string, name):
        is_valid = self._validate(string, name)
        return is_valid
    
    def _get(self, string, name):
        mapping = self._get_mapping(name, 'getter')
        slice_ = mapping['slice_']
        piece_of_data = string[slice_]
        return piece_of_data
        
    @twenty_times
    def swipe_until_it_matches_main(self):
        string = self.scraper.swipe()
        is_valid = self._validate_main(string)
        
        if is_valid:
            self.string = string
            return True # it returns True to the decorator
        else:
            return None
        
    @twenty_times
    def swipe_until_it_matches_other(self, name):
        string = self.scraper.swipe()
        
        #pdb.set_trace()
        
        is_valid = self._validate_other(string, name)
        
        if is_valid:
            self.string = string
            return True # it returns True to the decorator
        else:
            return None
        
    @poll_until_10_seconds
    def wait_until_it_leaves_page(self, name):
        string = self.scraper.swipe()
        
        # name will be main when we are leaving a page. It will be other, 
        # when we are dealing with different versions of a page
        is_still_on_page = self._validate_other(string, name) 
        
        if not is_still_on_page:
            return True # it returns True to the decorator
        else:
            return None
        
    def _get_coords(self, name):
        mapping = self._get_mapping(name, 'setter')
        coords = mapping['coords']
        
        (x, y) = (coords['x'], coords['y'])
        return (x, y)
        
    def _write(self, name, text):
        (x, y) = self._get_coords(name)
        p.click(x, y)
        p.write(text)
        
    def to_txt(self, folder, file_name):
        path = folder + sep + file_name + '.txt'
        with open(path, 'w', encoding = 'utf-8') as f:
            f.write(self.string)
            
######
        
class SiafiInitialPage1(Page):
    validation = [dict(name        = 'main',
                       slice_      = slice(28, 52), 
                       to_validate = '-  MENU  DE  SISTEMAS  -')]
    
    setter = [dict(name = 'system_input',
                   coords = dict(x = 642, 
                                 y = 816))]
    
    def set_system_name(self, system_name):
        self._write('system_input', system_name)
        
    def advance(self):
        self.scraper.enter()
        
######

class SiafiLogin(Page):
     validation = [dict(name        = 'main',
                        slice_      = slice(776, 816),
                        to_validate = 'SSSSSSSS  III  AAA   AAA  FFF        III'),
                   dict(name = 'input_that_appears_after_credentials',
                        slice_ = slice(1760, 1790),
                        to_validate = 'SISTEMA ...... _______________')]
     
     setter = [dict(name = 'cpf_input',
                    coords = dict(x = 1135, 
                                  y = 727)),
               dict(name = 'pass_input',
                    coords = dict(x = 1135,
                                  y = 753)),
               dict(name = 'system_year_input',
                    coords = dict(x = 1135, 
                                  y = 815))]
     
     def set_cpf(self, cpf):
         self._write('cpf_input', cpf)
         
     def set_pass(self, pass_):
         self._write('pass_input', pass_)
         
     def submit(self):
         self.scraper.enter()
         
     @poll_until_10_seconds    
     def wait_until_input_appears(self):
         string = self.scraper.swipe()
         is_input_showing = self._validate_other(string, 'input_that_appears_after_credentials')
         
         if is_input_showing:
             return True
         else:
             return None
         
     def set_system_year(self, system_year):
         self._write('system_year_input', system_year)
         
     def advance(self):
         self.scraper.enter()

######

class SiafiMenu(Page):
    validation = [dict(name       = 'main',
                       slice_      = slice(678, 714),
                       to_validate = 'ADMINISTRA ADMINISTRACAO  DO SISTEMA')]
    
    setter = [dict(name   = 'command_input', 
                   coords = dict(x = 577,
                                 y = 813))]
    
    def set_command(self, command):
        self._write('command_input', command)
        
    def advance(self):
        self.scraper.enter()
        
######
        
class ConlcEntrance(Page):
    validation = [dict(name        = 'main',
                       slice_      = slice(412, 448),
                       to_validate = 'NUMERO               : 2022LC ______')]
    
    setter = [dict(name   = 'lc_input',
                   coords = dict(x = 861,
                                 y = 344))]
    
    def set_lc_num(self, lc_num):
        self._write('lc_input', lc_num)
        
    def advance(self):
        self.scraper.enter()
        
######
        
class ConlcDataPage(Page):
    validation = [dict(name        = 'main', 
                       slice_      = slice(416, 490),
                       to_validate = 'NUMERO   ATUALIZADO EM QTD              VALOR TOTAL   NUMERO OB   SIT. OBS'),
                  
                  dict(name        = 'current_page',
                       slice_      = slice(228, 231), # assumes highest page is 100
                       to_validate = '1', # always start at page 1
                       processing  = strip_and_no_dots),
                  
                  dict(name        = 'last_page',
                       slice_      = slice(1739, 1753),
                       to_validate = 'TOTAL    .....')]
    
    getter = [dict(name   = 'last_lc_on_page',
                   slice_ = slice(1650, 1656))]
        
    def __init__(self, scraper, highest_lc_num_wanted):
        super().__init__(scraper)
        self.highest_lc_num_wanted = highest_lc_num_wanted
        
    def increment_page_num(self):
        mapping = self._get_mapping('current_page', 'validation')
        value = mapping['to_validate']
        value = int(value)
        value += 1
        value = str(value)
        mapping['to_validate'] = value
    
    def _is_next_page_irrelevant(self):
        last_lc_on_page = self._get(self.string, 'last_lc_on_page')
        is_next_page_irrelevant = last_lc_on_page >= self.highest_lc_num_wanted
        
        return is_next_page_irrelevant
    
    def _is_this_the_last_page(self):
        is_last_page = self._validate_other(self.string, 'last_page')
        return is_last_page
    
    def should_i_stop_advancing(self):
        #pdb.set_trace()
        should_i_stop = self._is_next_page_irrelevant() or self._is_this_the_last_page()
        return should_i_stop
    
    def advance(self):
        self.scraper.f8()
        
#==============================================================================
# HIGH-LEVEL FUNCTIONS
# They may be generalized, but they would get harder to read
# it is still hardcoded

def start_siafi(scraper):
    hod_name = 'Terminal 3270'
    scraper.set_window_to_foreground(hod_name)

def set_sf_at_siafi_initial_page(scraper):
    siafi_initial_page1 = SiafiInitialPage1(scraper)
    
    # read and validate
    if not siafi_initial_page1.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_initial_page1}')
    
    # set
    siafi_initial_page1.set_system_name('sf')
    
    # advance and validate
    siafi_initial_page1.advance()
    if not siafi_initial_page1.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {siafi_initial_page1}')
        
    # report
    print('Inserted "sf" at Siafi\'s Initial Page.')
    
def set_credentials_at_siafi_login(scraper):
    siafi_login = SiafiLogin(scraper)
    
    # read and validate
    if not siafi_login.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_login}')
    
    # set
    siafi_login.set_cpf('36912843883')
    siafi_login.set_pass('senha09')
    siafi_login.submit()
    
    if not siafi_login.wait_until_input_appears():
        raise Exception(f'Failed to find the input to type the system year. Maybe the password needs to change. Page object: {siafi_login}')
    siafi_login.set_system_year('siafi2022')
    
    # advance and validate
    siafi_login.advance()
    if not siafi_login.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {siafi_login}')
    
    # report
    print("Inserted credentials at Siafi\'s login page.")
    
def set_conlc_at_siafi_menu(scraper):
    siafi_menu = SiafiMenu(scraper)
    
    # read and validate
    if not siafi_menu.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {siafi_menu}')
    
    # set
    siafi_menu.set_command('>conlc')
    
    # advance and validate
    siafi_menu.advance()
    if not siafi_menu.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {siafi_menu}')
    
    # report
    print('Inserted ">conlc" at Siafi\'s menu.')
    
def set_first_conlc_num(scraper, first_conlc_num):
    conlc_entrance = ConlcEntrance(scraper)
    
    # read and validate
    if not conlc_entrance.swipe_until_it_matches_main():
        raise Exception(f'Failed to validate the page object {conlc_entrance}')
    
    # set
    conlc_entrance.set_lc_num(first_conlc_num)
    
    # advance and validate
    conlc_entrance.advance()
    if not conlc_entrance.wait_until_it_leaves_page('main'):
        raise Exception(f'Failed to move out of the page object {conlc_entrance}')
    
    # report
    print(f'Inserted {first_conlc_num} as the first LC num to search for')
    
def download_conlc_data_page_as_txt(scraper, last_conlc_num, raw_folder):
    # initialize
    counter = '0'
    
    # read and validate
    conlc_data_page = ConlcDataPage(scraper, last_conlc_num)
    if not conlc_data_page.swipe_until_it_matches_other('current_page'):
        raise Exception(f'Failed to validate the page object {conlc_data_page}')
    
    # iterate and save on disk
    while not conlc_data_page.should_i_stop_advancing():
        # prepare counter to be used as file name
        counter = str(int(counter) + 1)
        
        # save
        conlc_data_page.to_txt(raw_folder, counter)
        
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
        conlc_data_page.to_txt(raw_folder, counter)

    print(f'Downloaded {counter} LCs to {raw_folder}')
    

        
if __name__ == '__main__':
    # bug: it doesn't get the last page because it stops advancing 
    '''
    first_conlc_num = '420000'
    last_conlc_num =  '421029'
    raw_folder = RAW_FOLDER
    
    scraper = Scraper()
    
    start_siafi(scraper)
    
    set_sf_at_siafi_initial_page(scraper)
    
    set_credentials_at_siafi_login(scraper)
    
    set_conlc_at_siafi_menu(scraper)
    
    set_first_conlc_num(scraper, first_conlc_num)
    
    download_conlc_data_page_as_txt(scraper, last_conlc_num, raw_folder)
    '''
    
    
