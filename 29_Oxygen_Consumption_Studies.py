import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import codecs
from getNames import getnames, getname
from progressbar import ProgressBar
import time
from AddCategory import AddCategory
#===================================================================================================

url= 'https://www.fishbase.de/physiology/OxygenDataList.php?ID=268&GenusName=Abramis&SpeciesName=brama&fc=122&stockcode=282'

def getData(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content, parser = lh.HTMLParser(remove_comments = True))
    tr_elements = doc.xpath('//tr')

    col = []                                                    # create list of columns
    for t in tr_elements[0]:
        name=t.text_content()
        col.append((name,[]))
    col.insert(1,('Oxygen Consumption at 20°C',[]))
    

    for j in range(2, len(tr_elements)):
        T = tr_elements[j]
        i = 0
        
        for t in T.iterchildren():
            data = str(t.text_content())
            data = data.strip().replace(',','')
            try:
                if data == '':
                    data= np.nan
                elif i >= 5:
                    data= str(data)
                elif i < 5:
                    data =float(data)
            except: 
                data = np.nan
            col[i][1].append(data)
            i+=1


    Dict={title:column for (title,column) in col}
    fullFrame = pd.DataFrame(Dict)
    meanFrame = pd.DataFrame()
    for i in [col[i][0]for i in range(0,5)]:
        meanFrame[i] = [fullFrame[i].mean()]
    for i in [col[i][0]for i in range(5,7)]:
        if len(fullFrame[i].unique()) == 1:
            meanFrame[i] = [fullFrame[i][0]]  
        else:
            try: 
                meanFrame[i] = [fullFrame[i][0]+ '*']  
            except:
                pass
    meanFrame['name'] = getname(url)

    return(meanFrame)


def main_frame(fname = 'SavedData/029_Oxygen_Consumption_Studies_Urls.csv'):
    linklist = pd.read_csv(fname).iloc[:,1].values.tolist()
    mainFrame = pd.DataFrame()
    pbar = ProgressBar()
    for i in pbar(linklist):
        df = getData(i)
        mainFrame = pd.concat([mainFrame,df])

    return mainFrame

def concatRight(fname = 'SavedData/029_Oxygen_Consumption_Studies.csv'):
    newMain = AddCategory(fname)
    weight = pd.DataFrame(newMain['Weight'])
    body_weight = pd.DataFrame(newMain['Body weight (g)'])
    newMain = newMain.drop(columns =['Salinity','Temperature','Applied stress','Activity','Oxygen consumption','Body weight (g)','Weight'])
    
    for i in range(1,len(weight)):
        if body_weight['Body weight (g)'][i] != np.nan:
            weight['Weight'][i]= body_weight['Body weight (g)'][i]
        else: 
            pass 
    newMain['Weight']= weight
    return newMain
result = concatRight()
result.to_csv(path_or_buf = 'SavedData/MainFrame.csv', index = False)