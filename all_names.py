import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from natsort import index_natsorted, order_by_index
from progressbar import ProgressBar

main_frame = pd.read_pickle('main_frame2')
name_frame = pd.read_pickle('list_of_names')

# creating a dataframe containing all names listed on fishbase (https://www.fishbase.de/ComNames/searchResult.php?language=English&country=)
def list_of_names(fname = 'searchResult.php'): 
    names = []
    ulist = []
    bs = BeautifulSoup(open(fname), features='lxml')
    for species in bs.findAll('i'):
        for parents in species.parents:
            if parents.name == 'td':
                names.append(str(species.contents))
    
    [ulist.append(x) for x in names if x not in ulist] # deleting double values
    
    df = pd.DataFrame() # create dataframe 
    df['name'] = ulist

    df = df.reindex(index=order_by_index(df.index, index_natsorted(df['name'], reverse=False))) # sort alphabetically
    df = df.reset_index(drop=True)  # fix index
    return df


def add_data_to_frame(names1 = name_frame, data = main_frame, title = 'speed'):
    names = names1
    names[title] = [np.nan] * len(names.index)
    pbar = ProgressBar()
    
    for i in pbar(range(len(data.index))):
        name = str(data['name'][i])
        if name in names['name'].tolist():
            for k in range(len(names.index)):
                if name == names['name'][k]:
                    var = data.loc[i, 'speed']
                    names.loc[k, 'speed'] = var
                    #print(names['speed'][k], data['speed'][i]) 
                else:
                    pass
    return names
    
result = add_data_to_frame()
result.to_pickle('main_frame3')




