# -*- coding: utf-8 -*-       
from re import search
import pyautogui as p

def twenty_times(func):
    def wrapper(*args, **kwargs):
        counter = 0
        
        while counter < 20:
            try:
                output = func(*args, **kwargs)
                return output
            except Exception as e:
                print(e)
                counter += 1
    
    return wrapper

def strip(string):
    return string.strip()

class Page():
    '''
    page always do the same 4 things:
        - check if we are in the right place
        - read something
        - write something
        - advance and check that it worked
        
    I can probably define the interface as:
        - swipe_validate
        - write everything
        - read_everything
        - advance_validate
        
    I could separate the logic with class Validator, class Getter, class Setter
    and class Advancer
    
    '''
    '''
    def _is_valid(self, string, slice_, substring):
        is_valid = string[slice_] == substring
        return is_valid
    '''
    def __init__(self, scraper):
        self.scraper = scraper
    
    def _is_valid(self, string):
        mapping   = self.validation
        substring = mapping['substring']
        slice_    = mapping['slice_']
        
        is_valid = string[slice_] == substring
        return is_valid
    
    def validate(self, string):
        return self._is_valid(string)
    
    def advance(self):
        '''
        override this with each specific method to advance to the next page
        '''
        pass
    
    def _get_coords(self, name):
        for dict_ in self.coords:           # iterate over the list of dicts
            if dict_['name'] == name:       # if key matches given name
                mapping = dict_['values'] # get the coordinates
            else:
                raise Exception(f'Wrong name to get coordinates. Got {name}')
        
        return (mapping['x'], mapping['y'])
    
    def write(self, name, text):
        (x, y) = self._get_coords(name)
        p.click(x, y)
        p.write(text)
        
    @twenty_times
    def swipe_validate(self, mode = 'in'):
        string = self.scraper.swipe()
        is_valid = self.validate(string)
        
        if mode == 'in':
            if not is_valid:
                raise Exception(f'Failed to validate {self}')
            else:
                # after validation, we want to keep this information to avoid reading the screen a second time
                # we can get specific data from it, or we can save it to disk
                self.string = string
                return
        
        elif mode == 'out':
            if is_valid:
                raise Exception(f'Failed to advance in {self.page_object}')
            else:
                return
            
    def advance_validate(self):
        self.advance()
        self.swipe_validate('out')
        
            
    def _get_mapping(self, name):
        '''
        this should be generalized to get both coords mapping and getter mapping
        '''
        for dict_ in self.getter:           # iterate over the list of dicts
            if dict_['name'] == name:       # if key matches given name
                mapping = dict_           # get the coordinates
            else:
                raise Exception(f'Wrong name to get value from. Got {name}')
        
        return mapping
        
    def _get_processed_data_from_mapping(mapping):
        # mapping has slice_, substring and processing keys
        slice_     = mapping['slice_']
        substring  = mapping['substring']
        processing = mapping['processing']
        
        raw_substring = ''
        
class SiafiInitialPage(Page):
    validation = dict(slice_    = slice(28, 52), # at this position
                      substring = '-  MENU  DE  SISTEMAS  -') # you find this substring and that is expected to be unique over the system
    
    coords = [dict(name = 'system_input',
                   values = dict(x = 642, 
                                 y = 816))]
    
    def set_system_name(self, system_name):
        self.write('system_input', system_name)
        
    def advance(self):
        self.scraper.enter()
    
class SiafiLogin(Page):
     validation = dict(slice_ = slice(776, 816),
                       substring = 'SSSSSSSS  III  AAA   AAA  FFF        III')
     
     coords = [dict(name = 'cpf_input',
                    values = dict(x = 1135, 
                                  y = 727)),
               dict(name = 'pass_input',
                    values = dict(x = 1135,
                                  y = 753)),
               dict(name = 'system_year_input',
                    values = dict(x = 1135, 
                                  y = 815))]
     
     def set_cpf(self, cpf):
         self.write('cpf_input', cpf)
         
     def set_pass(self, pass_):
         self.write('pass_input', pass_)
         
     def submit(self):
         self.scraper.enter()
         
     def set_system_year(self, system_year):
         self.write('system_year_input', system_year)
         
     def advance(self):
         self.scraper.enter()
                   
class SiafiMenu(Page):
    validation = dict(slice_ = slice(678, 714),
                      substring = 'ADMINISTRA ADMINISTRACAO  DO SISTEMA')
    
    coords = [dict(name = 'command_input', 
                   values = dict(x = 577,
                                 y = 813))]
    
    def set_command(self, command):
        self.write('command_input', command)
        
    def advance(self):
        self.scraper.enter()
    
class SiafiWarning(Page):
    pass
    
    
class SiafiInitialPageType2(Page):
    validation = dict(slice_ = slice(2, 10),
                      substring = 'TELA 001')
    
    coords = dict(name   = 'cpf_input',
                  values = dict(x = 587,
                                y = 634))
'''
class Conlc(Page):
    validation = dict(slice_    = slice(15, 39),              # at indexes [15:39]
                      substring = 'DOCUMENTO-CONSULTA-CONLC')
'''
'''
class Conlc(Page):
     conlc_cue = dict(slice_    = slice(15, 39),              # at indexes [15:39]
                      substring = 'DOCUMENTO-CONSULTA-CONLC') # you should match this text
     
     def is_in_conlc(self, string):
         '''
         #Uses the function name given by Siafi HoD to assert that the scraper in in Conlc
'''
         is_valid = self._is_valid(string, **self.conlc_cue)
        
         return is_valid
''' 
class ConlcInitialPage(Page):
    validation = dict(slice_ = slice(412, 448),
                      substring = 'NUMERO               : 2022LC ______')
    
    coords = [dict(name = 'lc_input',
                   values = dict(x = 861,
                                 y = 344))]
    
    def set_lc_num(self, lc_num):
        self.write('lc_input', lc_num)
        
    def advance(self):
        self.scraper.enter()
    
class ConlcDataPage(Page):
    '''
    getter is just a specific case of validation, that we need to process
    '''
    validation = [dict(name = 'main',
                       slice_ = slice(1784, 1802),
                       to_validate = 'CONTINUA...       ',),
                  
                  dict(name = 'page_num',
                       slice_ = slice(0, 0),
                       to_validate = '',     # this gets updated when instanciated
                       processing = strip)] 

    def __init__(self, scraper, page_num):
        super.__init__(scraper)
        self.getter.substring = page_num
        
    # the flow is:
    # swipe and validate main
    # if validated, save string
    # if not, swipe again until it does
    # validate the other stuff, if they exist
    # set stuff, if they exist
    # advance and validate using name
    
        
        
    
    
    
class ConlcLastPage(Page):
    validation = dict(slice_ = slice(0, 0),
                      substring = '')
    
    
    
    '''
    lc_num_input = dict(x = 861, # at (861, 344) you find the
                        y = 344) # input box for inserting an LC number'''

'''
think of class variables as services offered by the class
it enables you to check if it is conlc_data_page
to check if there is a next_page
to check if the scraped current_page matches the expected value
'''

class ConlcDataPage(Page):
    conlc_data_page_cue = dict(slice_    = slice(416, 490), # at indexes [416:490] you should match
                               substring = 'NUMERO   ATUALIZADO EM QTD              VALOR TOTAL   NUMERO OB   SIT. OBS') # this text
    
    next_page_cue = dict(slice_    = slice(1784, 1795), # at indexes [1784:1795]
                         substring = 'CONTINUA...')     # you should match this text
    
    current_page_cue = dict(slice_ = slice(225, 231), # at indexes [225:231]
                            substring = '1')          # you should match the number of the current page
                                                      # that starts at 1, but needs to be updated as we scrape more page
                                                   
    def is_in_conlc_data_page(self, string):
        '''
        uses column header to assert that the scraper in in Conlc data page
        '''
        is_valid = self._is_valid(string, **self.conlc_data_page_cue)
        return is_valid
    
    def is_there_a_next_page(self, string):
        is_valid = self._is_valid(string, **self.next_page_cue)
        return is_valid
        
    def get_current_page_from_string(self, string):
        current_page = string[self.current_page_cue['slice_']]
        current_page = current_page.strip()
        return current_page
    
    def get_current_page_from_inner_attribute(self):
        current_page = self.current_page_cue['substring']
        return current_page
    
    def set_current_page(self, value):
        if not isinstance(value, str):
            raise TypeError(f'Method set_current_page expects a string. Got {type(value)}')
            
        match = search(pattern = r'^\d{1,6}$', 
                       string = value)
        
        if match is None:
            raise ValueError(f'Method set_current_page expects a digit from 1 to 999999. Got {value}')
            
        self.current_page_cue['substring'] = value

if __name__ == '__main__':
   pass
    
    

### finding indexes the easy way
'''
path = 'C:\\Users\\Tales\\Desktop\\census_management\\test.txt'
with open(path, 'r', encoding = 'utf-8') as f:
    string = f.read()

path2 = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\raw\\1.txt'
with open(path2, 'r', encoding = 'utf-8') as f:
    string2 = f.read()
    
'''