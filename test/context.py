# -*- coding: utf-8 -*-
from os.path import dirname
from os import sep, chdir

test_folder = dirname(__file__)
project_folder = dirname(test_folder)
etl_folder = project_folder + sep + 'etl'

chdir(etl_folder)

from pages import Conlc, ConlcInitialPage, ConlcDataPage