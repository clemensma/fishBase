import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


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




    for j in range(1, len(tr_elements)):
        T = tr_elements[j]

        i = 0

        for t in T.iterchildren():
            data = t.text_content()
            if i>0:
                try:
                    data = float(data)
                except:
                    pass
            col[i][1].append(data)
            i+=1

    Dict={title:column for (title,column) in col}
    df=pd.DataFrame(Dict)
    return df


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
    return linkList


def getMeanSpeed(frame):
    avspeed = frame['Speed (m/s)'].mean()
    return avspeed

def getAverageFishSpeed(main_url = 'https://www.fishbase.de/Topic/List.php?group=32'):
    links = getURL(main_url)
    all_speeds = []
    for i in links:
        frame = getData(i)
        all_speeds.append(getMeanSpeed(frame))
    averageSpeed = np.mean(all_speeds)
    return averageSpeed

main_url = 'https://www.fishbase.de/Topic/List.php?group=34'
print(getData(main_url))
