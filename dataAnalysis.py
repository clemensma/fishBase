import pandas as pd
import numpy as np
def importFrame(fname):
    return pd.read_csv(fname)

def listColumns(df):
    return df.head()

def getCategoryWithName(df, category):
    return df[['name', category]]

def getDataCoverage(df, category):
    return np.sum(df[category].count()) / len(df[category]) * 100

df = importFrame('SavedData/MainFrame.csv')

print(getDataCoverage(df,'SL (cm)'))

#print(getCategoryWithName(importFrame('SavedData/MainFrame.csv'), 'speed'))