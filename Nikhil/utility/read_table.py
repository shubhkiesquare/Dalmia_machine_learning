import numpy as np 
import pandas as pd


def read_multiple_tables(directory):
    df = pd.DataFrame()
    for folder in os.listdir(directory):
        if folder not in ['.DS_Store', '.ipynb_checkpoints']:
            for file in os.listdir(os.path.join(directory , folder)):
                if file != '.ipynb_checkpoints':
                    files_dir = os.path.join(directory , folder , file)
                    df_1 = pd.read_excel(files_dir, engine='pyxlsb')
                df = pd.concat([df , df_1] , axis = 0)
    return df