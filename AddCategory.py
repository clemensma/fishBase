import pandas as pd
#==================================================================================================================
#Adds slected data to the main Frame
def AddCategory(fname):
    data = pd.DataFrame(pd.read_csv(fname))                                                 # load dataframe containing target value and coresponding name
    main = pd.DataFrame(pd.read_csv('SavedData/MainFrame.csv'))                             # load main Frame containing all fish and data added until now

    newMain = pd.merge(left=main, right=data, how='left', left_on='name', right_on='name')  # join target values on existing main Frame

    return newMain