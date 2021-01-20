import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import codecs
from getNames import getnames
from progressbar import ProgressBar
import time

def getData(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content, parser = lh.HTMLParser(remove_comments = True))
    tr_elements = doc.xpath('//tr')

    col = []                                                    # create list of columns
    for t in tr_elements[0]:
        name=t.text_content()
        col.append((name,[]))
    col.insert(3,('Encephalization coefficients 2',[]))

    
    
    for j in range(2, len(tr_elements)):
        T = tr_elements[j]
        i = 0

        for t in T.iterchildren():
    
            data = str(t.text_content())
            data = data.strip().replace(',','')

            if data == '':
                data= np.nan
            else:
                data= float(data)
            

            col[i][1].append(data)
            i+=1

           
    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    df = df.mean().to_frame().transpose()
    return(df)


names = getnames('SavedData/034_Relationship_Between_Fish_Brain_Weights_And_Body_Weights_Urls.csv')
linklist = pd.read_csv('SavedData/034_Relationship_Between_Fish_Brain_Weights_And_Body_Weights_Urls.csv').iloc[:,1].values.tolist()

url = 'https://www.fishbase.de/physiology/BrainsDataList.php?ID=6652&GenusName=Abudefduf&SpeciesName=abdominalis&fc=350'





def main_frame(linklist= linklist):
    frames= []
    pbar = ProgressBar()
    j = 0
    for i in pbar(linklist):
        if j%100 == 0:
            time.sleep(20)
        frames.append(getData(i))
        j += 1
    result= pd.concat(frames)
    #result = result.mean().to_frame().transpose()
    return result

result = main_frame()
result['name'] = names
result.to_csv(path_or_buf = 'SavedData/034_Relationship_Between_Fish_Brain_Weights_And_Body_Weights.csv', index = False)
