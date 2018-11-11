import os
import pandas as pd

my_path = os.path.abspath(os.path.dirname(__file__))
input1 = os.path.join(my_path, './Kumpula_temps_May_Aug_2017.csv')


data = pd.read_csv(input1, sep=',', )
data['YRMODA']= data['YR--MODAHRMN'].astype(str).str.slice(0,8)
# print(data.head(30))
groupby = data.groupby('YRMODA')

ourDf= pd.DataFrame()
# ourDf['day', 'avg']=None
# print(ourDf)
day =[]
avgTemp=[]
for key, group in groupby:
    tempMean = group['TEMP'].mean()
    tempMin = group['TEMP'].min()
    tempMax = group['TEMP'].max()
    ourDf.loc[key,'day']=key
    ourDf.loc[key,'avg']=tempMean
    ourDf.loc[key,'max']=tempMax
    ourDf.loc[key,'min']=tempMin

print(ourDf.reset_index(drop=True))
# ourDf['day']=day
# ourDf['avg']=avgTemp
# ourDf.loc[0, 'day']=[5,3,5]
# print(ourDf)


# data=data.loc[0:1,]



# for i, rows in data.iterrows():
#     strR= str(rows['YR--MODAHRMN'])
#     print(strR[6:8])


# print(data1.loc[:,'YR--MODAHRMN'])