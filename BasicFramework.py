import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from natsort import index_natsorted, order_by_index
from progressbar import ProgressBar
#===============================================================================================
# creating a dataframe containing all names listed on fishbase (https://www.fishbase.de/ComNames/searchResult.php?language=English&country=)

def list_of_names(fname = 'SavedData/searchResult.php'): 
    names = []
    ulist = []
    bs = BeautifulSoup(open(fname), features='lxml')
    pbar= ProgressBar()
    for species in pbar(bs.findAll('i')):
        for parents in species.parents:
            if parents.name == 'td':
                [names.append(name) for name in species.contents]
    
    [ulist.append(x) for x in names if x not in ulist] # deleting double values
    


    df = pd.DataFrame() # create dataframe 
    df['name'] = ulist

    df = df.reindex(index=order_by_index(df.index, index_natsorted(df['name'], reverse=False))) # sort alphabetically
    df = df.reset_index(drop=True)  # fix index
    return df

result = list_of_names()
result.to_csv(path_or_buf = 'SavedData/MainFrame.csv', index = False)

#Nicht mehr ausführen!