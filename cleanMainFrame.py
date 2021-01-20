import pandas as pd

def removeColumn():
    pd.read_csv('SavedData/MainFrame.csv').drop(columns = ['Unnamed: 0']).to_csv('SavedData/MainFrame.csv', index = False)

removeColumn()    