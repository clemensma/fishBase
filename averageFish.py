import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import codecs

def getData(url):
    page = requests.get(url)
    doc = lh.fromstring(page.content, parser = lh.HTMLParser(remove_comments = True))
    tr_elements = doc.xpath('//tr')

    col = []
    i = 0

    for t in tr_elements[0]:
        i+=1
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
    print(type(df))
    return(df)


def getURL(url):
    links = []

    page = requests.get(url)
    bs = BeautifulSoup(page.content, features='lxml')

    for link in bs.findAll('a'):
        for parent in link.parents:
            if parent.name == 'td':
                links.append(link.get('href'))
    linkList = []
    for i in links:
        c = 'https://www.fishbase.de' + i[2:]
        linkList.append(c)
    return(linkList)



def getURL_local(fname = 'List.php'):
    links = []
    bs = BeautifulSoup(open(fname), features='lxml')
    for link in bs.findAll('a'):
        for parent in link.parents:
            if parent.name == 'td':
                links.append(link.get('href'))
    linkList = []
    for i in links:
        c = 'https://www.fishbase.de' + i[2:]
        linkList.append(c)
    return(linkList)

def list_of_names(fname = 'List.php'):
    names = []
    bs = BeautifulSoup(open(fname), features='lxml')
    for species in bs.findAll('a'):
        for parent in species.parents:
            if parent.name == 'td':
                names.append(species.contents)

    return names



links = getURL_local()
#print(links)
#print(list_of_names())
for i in links[:10]:
    print(getData(i))
