import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import codecs


main_frame = pd.read_pickle('main_frame')
speed_frame = pd.read_pickle('speed_frame')

def add_speed(main_frame = main_frame, speed_frame = speed_frame, title = 'speed'):

    main_frame[title] = [np.nan] * len(main_frame.index)

    new_df = pd.DataFrame(columns = main_frame.columns)
    new_df.loc[0] = [np.nan]*len(main_frame.columns)

    for i in range(len(speed_frame.index)):
        name = speed_frame['name'][i]
        if name in main_frame['name'].tolist():
            for k in range(len(main_frame.index)):
                if name == main_frame['name'][k]:
                    main_frame[title][k] = speed_frame[title][i]
        else:
            new_df1 = pd.DataFrame(columns = main_frame.columns)
            new_df1.loc[0] = [np.nan]*len(main_frame.columns)

            new_df1['name'][0] = speed_frame['name'][i]
            new_df1[title][0] = speed_frame[title][i]

            new_df= pd.concat([new_df, new_df1])

    main_frame = pd.concat([main_frame, new_df])
    print(main_frame.mean())



add_speed()
