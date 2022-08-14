# -*- coding: utf-8 -*-

# FOLDER
DATA_LAKE_FOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake'

# DATA LAKER LAYERS
LAYERS = ('raw', 'standardized', 'transformed')

# CATEGORIES
CAT_NAMES = ('420', '520', '620') # it is redundant with key name for now

# THIS WILL BE USED TO CREATE FOLDERS IN THE DATA LAKE
# AND TO SPECIFY WHICH DATA THE SYSTEM WILL GET
CATEGORIES = [dict(name         = '420',
                   first_lc_num = '420000',
                   last_lc_num  = '420999'),
              dict(name         = '520',
                   first_lc_num = '520000',
                   last_lc_num  = '520999'),
              dict(name         = '620',
                   first_lc_num = '620000',
                   last_lc_num  = '620999')]

# EXTRACT RELATED VALUES
SYSTEM_NAME   = 'sf'
SYSTEM_YEAR   = 'siafi2022'
CONLC_COMMAND = '>conlc'

#
CAT420RAWFOLDER   = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\420\\raw'
CAT520RAWFOLDER   = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\520\\raw'
CAT620RAWFOLDER   = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\620\\raw'

CAT420STANDFOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\420\\standardized'
CAT520STANDFOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\520\\standardized'
CAT620STANDFOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\620\\standardized'

CAT420TRANSFOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\420\\transformed'
CAT520TRANSFOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\520\\transformed'
CAT620TRANSFOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\620\\transformed'
