import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from progressbar import ProgressBar
from getNames import getnames

def getData(url):
    page = requests.get(url)                                                            #load webpage
    doc = lh.fromstring(page.content, parser = lh.HTMLParser(remove_comments = True))   # take content and remove comments from page
    tr_elements = doc.xpath('//tr')                                                     # take elements of table rows

    col = []
    for t in tr_elements[0]:                                                            # create list of column titles
        name=t.text_content()
        col.append((name,[]))

    for element in tr_elements[1:]:                                                     # convert values to floats if possible
        i = 0
        for t in element.iterchildren():
            data = t.text_content()
            if i>0:
                try:
                    data = float(data)
                except:
                    pass
            col[i][1].append(data)
            i+=1

    Dict={title:column for (title,column) in col}                                       # translate Data from col to Data frame
    df=pd.DataFrame(Dict)
    
    return(df)
print(getData('https://www.fishbase.de/Physiology/SpeedList.php?ID=268&GenusName=Abramis&SpeciesName=brama'))
def get_mean_speed(frame):                                                              # get mean speed
    avspeed = frame['Speed (m/s)'].mean()
    return avspeed


'''
def get_avarage_fishspeed(main_url = 'https://www.fishbase.de/Topic/List.php?group=32'):
    links = getURL(main_url)
    all_speeds = []
    for i in links:
        frame = getData(i)
        all_speeds.append(get_mean_speed(frame))
    avarage_speed_in_knots = np.mean(all_speeds) * 1.94
    print('the avarage speed of a fish is',avarage_speed_in_knots,'knots')
'''   


def get_speed_data(url = 'https://www.fishbase.de/Topic/List.php?group=32'):
    links = pd.read_csv('SavedData/032_Speed_Measurements_Urls.csv')['Speed_Measurements'].values.tolist()
    
    all_speeds = []
    pbar = ProgressBar()
    
    for i in pbar(links):
        frame = getData(i)
        all_speeds.append(get_mean_speed(frame)) # all_speeds ist jetzt liste mit allen geschwindigkeitswerten
    df = pd.DataFrame()
    df['speed'] = all_speeds
    df['name'] = getnames()
    return df

result = get_speed_data()
result.to_csv(path_or_buf = 'SavedData/032_Speed_Measurements.csv', index = False)