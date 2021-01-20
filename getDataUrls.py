#createUrlCsv(group, title) to create a .csv with alle the links to the fish for a specific data group on fishbase.org
import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import codecs
from progressbar import ProgressBar
def getNumOfEntries(group):                                                                                 # gets the number of listed fish in a specific category to fix the scape for lists > 500 entries
    masterUrl = 'https://www.fishbase.de/Topic/List.php?group=' + group                                     # url to open the group
    page = requests.get(masterUrl)
    bs = BeautifulSoup(page.content, features='lxml')                                                       # load the page content to beautifulsoup
    div = bs.find('div', {'class': 'infonav'}).getText()                                                    # get the text of the infonav where the number of entries is listed
    if 'n' in div:                                                                                          # if there are less then 500 entries 'n' is present in the infonav
        div = div.replace('\t', '').replace('\n', '').replace(' ', '').replace('n=', '')                    # clean up the string to get the number
    else:                                                                                                   # else more then 500 entries
        div = div.replace('\t', '').replace(' ', '').replace(',', '')                                       # clean up the string to almost get the number
        start = 'f'
        end = ')'
        div = div[div.find(start)+len(start):div.rfind(end)]                                                # get he string between the chars 'f' and ')'
    return int(div)                                                                                         # return the number of entries as an int

def ScrapeFishbase(group, title): 
    numOfReps = getNumOfEntries(group) // 500
    links = []
    for rep in range(numOfReps + 1):
        masterUrl = 'https://www.fishbase.de/Topic/List.php?group=' + group + '&start=' + str(rep*500)
        page = requests.get(masterUrl)
        bs = BeautifulSoup(page.content, features='lxml')
    
        for link in bs.findAll('a'):
            for parent in link.parents:
                if parent.name == 'td':
                    if link.get('href') not in links:                                                       # making sure to leave out double values
                        links.append(link.get('href'))
    
    linkList = []
    for i in links:
        c = 'https://www.fishbase.de' + i[2:]
        linkList.append(c)
    df = pd.DataFrame(linkList)
    df.columns = [title]
    return(df)

def createUrlCsv(group, title):
    if int(group) < 10:                                                                             # calls ScrapeFishbase() with a  group and a title of the category and converts the returned dataframe to a correctly named csv
        ScrapeFishbase(group, title).to_csv('SavedData/00' + str(group) + '_' + title + '_Urls.csv')
    elif int(group) < 100:
        ScrapeFishbase(group, title).to_csv('SavedData/0' + str(group) + '_' + title + '_Urls.csv')
    else:
        ScrapeFishbase(group, title).to_csv('SavedData/' + str(group) + '_' + title + '_Urls.csv')


# Testing: 
#createUrlCsv('32', 'speed')
#createUrlCsv('34', 'brainSize')                                                                             # problem having more than 500 entrys fixed
#createUrlCsv('29', 'oxygenConsumption')


# groups range fro 1 to 35 with some odd exceptions


#print(getNumOfEntries('34'))
def getListOfGroups():
    pbar = ProgressBar()
    url = 'https://www.fishbase.de/Topic/List.php?group='
    nameDict = {}
    for i in pbar(range(1,36)):
        masterUrl = url + str(i)
        page = requests.get(masterUrl)
        bs = BeautifulSoup(page.content, features='lxml')
        try:
            div = bs.find('div', {'class': 'pheader'}).getText()
            div = div.strip().replace('\'', '').replace('.', '').replace('-', '_').replace(' ', '_')
            nameDict[i] = div
        except:
            continue
    return nameDict

def getDataUrls():
    pbar = ProgressBar()
    print('loading list of data groups...')
    d = getListOfGroups()
    print(d)
    print('creating .csv files...')
    for i in pbar(d):
        if i == 28:
            continue
        createUrlCsv(str(i), d[i])

getDataUrls()
#print(getNumOfEntries(str(34)))