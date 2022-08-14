# create folder if they don't exist
# this could be generalized to deal with any number of categories

from pathlib import Path
from os import sep
from os.path import dirname
from config import DATA_LAKE_FOLDER, CATEGORIES, LAYERS, CAT_NAMES

paths_str = []

'''
class PathManager:
    def __init__(self, categories = CATEGORIES, data_lake_folder = DATA_LAKE_FOLDER,
                 layers = LAYERS):
        
        self.categories        = categories
        self.data_lake_folder  = data_lake_folder
        self.layers            = layers
        
        self.paths_list = self._create_paths_list()
        
    def _create_paths_list(self):
        folder = self.data_lake_folder
        categories = self.categories
        layers = self.layers
        
        paths = [folder + sep + cat['name'] + sep + l for l in layers for cat in categories]
        return paths
        
    def create_folders():
        for one_path in self.paths_str:
            Path(one_path).mkdir(parents = True, exist_ok = True)
'''
def create_paths_str(categories = CATEGORIES, folder = DATA_LAKE_FOLDER,
                     layers = LAYERS):
    
    # gets folder/category/layer for every category and layer combination
    paths = [folder + sep + cat['name'] + sep + l for l in layers for cat in categories]
    # e.g. 'C:\\Users\\Tales\\Desktop\\census_management\\data_lake\\420\\raw'
    
    return paths


def setup():
    global paths_str 
    paths_str = create_paths_str()
    
    for one_path in paths_str:
        Path(one_path).mkdir(parents = True, exist_ok = True)
        


if __name__ == '__main__':
    setup()

        
