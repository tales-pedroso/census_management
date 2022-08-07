# -*- coding: utf-8 -*-       
from re import search

class Page():
    def _is_valid(self, string, slice_, substring):
        is_valid = string[slice_] == substring
        return is_valid

class Conlc(Page):
     conlc_cue = dict(slice_    = slice(15, 39),              # at indexes [15:39]
                      substring = 'DOCUMENTO-CONSULTA-CONLC') # you should match this text
     
     def is_in_conlc(self, string):
         '''
         Uses the function name given by Siafi HoD to assert that the scraper in in Conlc
         '''
         is_valid = self._is_valid(string, **self.conlc_cue)
        
         return is_valid
     
class ConlcInitialPage(Conlc):
    lc_num_input = dict(x = 861, # at (861, 344) you find the
                        y = 344) # input box for inserting an LC number

'''
think of class variables as services offered by the class
it enables you to check if it is conlc_data_page
to check if there is a next_page
to check if the scraped current_page matches the expected value
'''

class ConlcDataPage(Conlc):
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