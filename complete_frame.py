import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import codecs


main_frame = pd.read_pickle('main_frame')
speed_frame = pd.read_pickle('speed_frame')

def add_speed(main_frame = main_frame, speed_frame = speed_frame, title = 'speed'):
    length = len(main_frame.index)
    empty_list = [np.nan] * length
    main_frame[title] = empty_list
    print(main_frame)
    for i in range(len(speed_frame.index)):
        name = speed_frame['name'][i]
        for k in range(len(main_frame.index)):
            if name == main_frame['name'][k]:
                main_frame[title][k] = speed_frame[title][i]
    print(main_frame[title])




add_speed()
