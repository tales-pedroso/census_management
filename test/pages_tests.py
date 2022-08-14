# -*- coding: utf-8 -*-
from context import Conlc, ConlcInitialPage, ConlcDataPage
import unittest
from os.path import dirname
from os import sep
# external files path
'''
strings used are too long to type in here (length = 1966)
actual files from the system will be used for testing purposes 
'''
FOLDER = dirname(__file__)
PATHS = dict(conlc_initial_page = 'conlc_initial_page.txt',
             conlc_data_page_first_page = 'conlc_data_page_first_page.txt',
             conlc_data_page_last_page = 'conlc_data_page_last_page.txt',
             conlc_data_page_11th_page = 'conlc_data_page_11th_page.txt',
             siafi_initial_page = 'siafi_initial_page.txt')

# helper function

def get_file_as_string(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as f:
        return f.read()
    
# setting up strings for processing

STRINGS = {}

for key, path in PATHS.items():
    abs_path = FOLDER + sep + path
    PATHS[key] = abs_path
    
    STRINGS[key] = get_file_as_string(PATHS[key])

#==============================================================================


class ConlcTest(unittest.TestCase):
    def setUp(self):
        self.conlc = Conlc()
    
    # def test_returns_true_when_it_is_inside_conlc(self):
    #     string = STRINGS['conlc_initial_page']
        
    #     is_in_conlc = self.conlc.is_in_conlc(string)
        
    #     self.assertTrue(is_in_conlc)
    
    def test_returns_false_when_it_is_not_inside_conlc(self):
        string = STRINGS['siafi_initial_page']
        
        is_in_conlc = self.conlc.is_in_conlc(string)
        
        self.assertFalse(is_in_conlc)
        
class ConlcInitialPageTest(unittest.TestCase):
    def setUp(self):
        self.conlc_initial_page = ConlcInitialPage()
    
    # def test_returns_true_for_inherited_method_that_checks_if_it_is_inside_conlc_when_it_is(self):
    #     string = STRINGS['conlc_initial_page']
        
    #     is_in_conlc = self.conlc_initial_page.is_in_conlc(string)
        
    #     self.assertTrue(is_in_conlc)
    
    def test_returns_false_for_inherited_method_that_checks_if_it_is_inside_conlc_when_it_isnt(self):
        string = STRINGS['siafi_initial_page']
        
        is_in_conlc = self.conlc_initial_page.is_in_conlc(string)
        
        self.assertFalse(is_in_conlc)
    
class ConlcDataPageTest(unittest.TestCase):
    def setUp(self):
        self.conlc_data_page = ConlcDataPage()
    
    def test_returns_true_when_it_is_inside_conlc_data_page(self):
        string = STRINGS['conlc_data_page_first_page']
        
        is_in_conlc_data_page = self.conlc_data_page.is_in_conlc_data_page(string)
        
        self.assertTrue(is_in_conlc_data_page)
        
    def test_returns_false_when_it_is_not_inside_conlc_data_page(self):
        string = STRINGS['siafi_initial_page']
        
        is_in_conlc_data_page = self.conlc_data_page.is_in_conlc_data_page(string)
        
        self.assertFalse(is_in_conlc_data_page)
        
    def test_returns_true_for_inherited_method_that_checks_if_it_is_inside_conlc_when_it_is(self):
        string = STRINGS['conlc_data_page_first_page']
        
        is_in_conlc = self.conlc_data_page.is_in_conlc(string)
        
        self.assertTrue(is_in_conlc)
    
    def test_returns_false_for_inherited_method_that_checks_if_it_is_inside_conlc_when_it_isnt(self):
        string = STRINGS['siafi_initial_page']
        
        is_in_conlc = self.conlc_data_page.is_in_conlc(string)
        
        self.assertFalse(is_in_conlc)
        
    def test_returns_true_when_there_is_a_next_page(self):
        string = STRINGS['conlc_data_page_first_page']
        
        is_there_a_next_page = self.conlc_data_page.is_there_a_next_page(string)
        
        self.assertTrue(is_there_a_next_page)
    
    # def test_returns_false_when_there_is_not_a_next_page(self):
    #     string = STRINGS['conlc_data_page_last_page']
        
    #     is_there_a_next_page = self.conlc_data_page.is_there_a_next_page(string)
        
    #     self.assertFalse(is_there_a_next_page)

    def test_gets_right_page_number_from_string_when_it_is_the_first_page(self):
        string = STRINGS['conlc_data_page_first_page']
        
        page_number = self.conlc_data_page.get_current_page_from_string(string)
        
        self.assertEqual(page_number, '1')
    
    # def test_gets_right_page_number_from_string_when_it_is_a_2_digit_number(self):
    #     string = STRINGS['conlc_data_page_11th_page']
        
    #     page_number = self.conlc_data_page.get_current_page_from_string(string)
        
    #     self.assertEqual(page_number, '11')
    
    def test_gets_right_page_number_from_attribute(self):
        expected_page_number = '1' # starting value
        
        page_number = self.conlc_data_page.get_current_page_from_inner_attribute()
        
        self.assertEqual(page_number, expected_page_number)
    
    def test_sets_page_number_when_input_is_string_and_single_digit(self):
        input_page_number = '5'
        
        self.conlc_data_page.set_current_page(input_page_number)
        
        output_page_number = getattr(self.conlc_data_page, 'current_page_cue')['substring']
        self.assertEqual(input_page_number, output_page_number)
    
    def test_sets_page_number_when_input_is_string_and_double_digit(self):
        input_page_number = '99'
        
        self.conlc_data_page.set_current_page(input_page_number)
        
        output_page_number = getattr(self.conlc_data_page, 'current_page_cue')['substring']
        self.assertEqual(input_page_number, output_page_number)
    
    def test_sets_page_number_when_input_is_string_and_six_digits(self):
        input_page_number = '123456'
        
        self.conlc_data_page.set_current_page(input_page_number)
        
        output_page_number = getattr(self.conlc_data_page, 'current_page_cue')['substring']
        self.assertEqual(input_page_number, output_page_number)
    
    def test_throws_errors_when_trying_to_set_a_non_string_page_number(self):
        input_page_number = 1
        
        self.assertRaises(TypeError, 
                          self.conlc_data_page.set_current_page,
                          input_page_number)
    
    def test_throws_errors_when_trying_to_set_a_7_digit_page_number(self):
        input_page_number = '1234567'
        
        self.assertRaises(ValueError, 
                          self.conlc_data_page.set_current_page,
                          input_page_number)

if __name__ == '__main__':
    unittest.main()
    

