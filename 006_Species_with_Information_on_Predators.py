import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import codecs
from getNames import getnames
from progressbar import ProgressBar
import time
from AddCategory import AddCategory

def getData(url):
    page = requests.get(url)                                                            #load webpage
    doc = lh.fromstring(page.content, parser = lh.HTMLParser(remove_comments = True))   # take content and remove comments from page
    tr_elements = doc.xpath('//tr')                                                     # take elements of table rows

    col = []
    i = 0
    for t in tr_elements[0]:                                                            # create list of column titles
        name=t.text_content()
        col.append((name,[]))
        if i == 1:
            col.append((name + '1', []))
        i += 1

    

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

#print(getData('https://www.fishbase.de/TrophicEco/PredatorList.php?ID=972&GenusName=Ablennes&SpeciesName=hians'))

def getPredatorData(url = 'https://www.fishbase.de/Topic/List.php?group=6'):
    links = pd.read_csv('SavedData/006_Species_with_Information_on_Predators_Urls.csv')['Species_with_Information_on_Predators'].values.tolist()
    
    allPredators = {}
    names = getnames('SavedData/006_Species_with_Information_on_Predators_Urls.csv')
    pbar = ProgressBar()
    j = 1
    for i, k in pbar(zip(links, names)):
        if j % 50 == 0:
            time.sleep(20)
        frame = getData(i)['Name'].values.tolist()
        #print(frame['Name'].values.tolist())
        frame = [r[r.find(' \r\n\t\t\t') +  len(' \r\n\t\t\t'):r.rfind('\t\t\t')] for r in frame]
        print(frame)
        allPredators[k] = frame
        j += 1
    #print(allPredators)
    df = pd.DataFrame(list(allPredators.items()), columns = ['name', 'predators'])
    return df

#result = getPredatorData()

#result.to_csv(path_or_buf = 'SavedData/006_Species_with_Information_on_Predators.csv', index = False)

AddCategory('SavedData/006_Species_with_Information_on_Predators.csv').to_csv('SavedData/MainFrame.csv', index = False)