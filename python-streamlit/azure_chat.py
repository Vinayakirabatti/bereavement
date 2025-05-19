import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import nltk


# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

df=pd.read_csv('/kaggle/input/banking-chatbot/Dataset_Banking_chatbot.csv',encoding='latin')


from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

X= df['Query']+df['Response']
y=df['Response']+df['Response']

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
vec=TfidfVectorizer(stop_words='english')
xtr=vec.fit_transform(X)
model=SVC().fit(xtr,y)

def predict(inp):
    inp_vec=vec.transform([inp])
    res=model.predict(inp_vec)
    return res[0]

while True:
    inp=input('You: ')
    if inp.lower() in ['exit','quit','bye']:
        break
    res=predict(inp)
    linp=inp.split()
    ans='n'
    for word in linp:
        if word in res.split():
            print('Bot: ',res)
            ans='y'
            break
    if ans=='n': 
        print('Bot: I could not understand your query please write in other words')