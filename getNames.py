import requests
import lxml.html as lh
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
from progressbar import ProgressBar



def getnames(fname = 'SavedData/032_Speed_Measurements_Urls.csv'):
    links = pd.read_csv(fname).iloc[:,1].values.tolist()
    listofNames = []

    for url in links:
        name = url[url.find('GenusName=')+len('GenusName='):url.rfind('&SpeciesName')] + ' ' + url[url.find('&SpeciesName=')+len('&SpeciesName='):]
        if '&' in name:
            name = name[: name.rfind('&')]
        listofNames.append(name)

    return(listofNames)

def getname(url):
    name = url[url.find('GenusName=')+len('GenusName='):url.rfind('&SpeciesName')] + ' ' + url[url.find('&SpeciesName=')+len('&SpeciesName='):]
    if '&' in name:
            name = name[: name.rfind('&fc')]
    return name