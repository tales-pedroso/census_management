# -*- coding: utf-8 -*-


# FOLDER
DATA_LAKE_FOLDER = 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake'

# DATA LAKER LAYERS
LAYERS = ('raw', 'standardized', 'transformed')

# LC NUM 
FIRST_LC_NUM = '420000'
LAST_LC_NUM  = '620999'

# EXTRACT RELATED VALUES
SCREEN_NAME   = 'Terminal 3270'
SYSTEM_NAME   = 'sf'
SYSTEM_YEAR   = 'siafi2022'
CONLC_COMMAND = '>conlc'

# TRANSFORM RELATED VALUES
STAND_FILE_NAME = 'standardized'
TRANS_FILE_NAME = 'transformed'
COLUMNS_IN_CSV_FILES = ('LcYear', 'LcNum', 'LineCount', 'ObYear', 'ObNum', 'WasObCanceled')
CANCELED_VALUES = ('CANC.P', 'CANC.T')
WANTED_INTERVALS = (('420000', '420999'), # start, finish
                    ('520100', '520999'), # start, finish
                    ('620172', '620999')) # start, finish

## VALUES SPECIFIC TO CONLC DATA PAGE
ROWS_INDEXES = (slice(496, 571),  #1st row
                slice(578, 653),  #2nd row
                slice(660, 735),  #3rd row ...
                slice(742, 817),
                slice(824, 899),
                slice(906, 981),
                slice(988, 1063),
                slice(1070, 1145),
                slice(1152, 1227),
                slice(1234, 1309),
                slice(1316, 1391),
                slice(1398, 1473),
                slice(1480, 1555),
                slice(1562, 1637),
                slice(1644, 1719))

DATA_INDEXES = (slice(0, 4),    # lc year       --> 2022
               #slice(4, 6),    # "LC" constant --> LC   --> we don't want that info
                slice(6, 12),   # lc number     --> 520296
               #slice(13, 22),  # lc date       --> 01Fev2022 --> we don't want that info
                slice(23, 29),  # line count    --> 000537
               #slice(38, 52),  # value         --> 1.231.186,65 --> we don't want that info
                slice(54, 58),  # ob year       --> 2022
               #slice(58, 60),  # "OB" constant --> OB --> we don't want that info
                slice(60, 66),  # ob number     --> 831021
                slice(67, 73))  # was_canceled? --> CANC.P 
               #slice(74, 75))  # was_closed?   --> F --> we don't want that info

