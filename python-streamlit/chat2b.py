import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import os
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

df=pd.read_csv('D:/Vinayak/fullstack/bereavement/bereavement/python-streamlit/bereavement_train.csv',encoding='utf8')

X= df['Query']+df['Response']
y=df['Response']+df['Response']

vec=TfidfVectorizer(stop_words='english')
xtr=vec.fit_transform(X)
model=SVC().fit(xtr,y)

def predict(inp):
    inp_vec=vec.transform([inp])
    res=model.predict(inp_vec)
    return res[0]

# while True:
#     inp=input('You: ')
#     if inp.lower() in ['exit','quit','bye']:
#         break
#     res=predict(inp)
#     linp=inp.split()
#     ans='n'
#     for word in linp:
#         if word in res.split():
#             print('Bot: ',res)
#             ans='y'
#             break
#     if ans=='n': 
#         print('Bot: I could not understand your query please write in other words')

inp = input('')
if inp.lower() in ['exit','quit','bye']:
    print("byeee")

res = predict(inp)
linp = inp.split()

for word in linp:
    if word in res.split():
        print('Bot: ',res)
        ans = 'y'