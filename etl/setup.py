# create folder if they don't exist
# this could be generalized to deal with any number of categories

from pathlib import Path
from os import sep
from config import DATA_LAKE_FOLDER, LAYERS

def create_paths():
    paths = [DATA_LAKE_FOLDER + sep + layer for layer in LAYERS]
    return paths    
        
def get_folder_by_layer_name(name):
    if name not in LAYERS:
        raise ValueError(f'Input name is not valid. Got {name}. Expected one of these: {LAYERS}')
        
    folder = DATA_LAKE_FOLDER + sep + name
    return folder

def setup():
    paths = create_paths()
    
    print(f"Ready to create those paths, if they don't already exist: {paths}.")
    
    for path in paths:
        Path(path).mkdir(exist_ok = True)