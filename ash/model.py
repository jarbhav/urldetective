from functools import wraps
from flask import Flask
import pandas as pd
from flask import request, Response
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import math
from collections import Counter
import pickle
import requests
from bs4 import BeautifulSoup

df_1=pd.read_csv('domain.csv')
dom=list(df_1['domain'])
#from fuzzywuzzy import fuzz
df=pd.read_csv("data.csv")

def entropy(s):
    p,lns=Counter(s),float(len(s))
    return -sum( count/lns * math.log(count/lns, 2) for count in p.values())

def getTokens(input):
     tokensBySlash = str(input.encode('utf-8')).split('/')  #get tokens after splitting by slash
     allTokens = []
     for i in tokensBySlash:
          tokens = str(i).split('-')    #get tokens after splitting by dash
          tokensByDot = []
          for j in range(0,len(tokens)):
               tempTokens = str(tokens[j]).split('.')  #get tokens after splitting by dot
               tokensByDot = tokensByDot + tempTokens
          allTokens = allTokens + tokens + tokensByDot
     allTokens = list(set(allTokens))   #remove redundant tokens
     if 'com' in allTokens:
          allTokens.remove('com')  #removing .com since it occurs a lot of times and it should not be included in our features
     
     return allTokens

allurlsdata = pd.DataFrame(df)

allurlsdata = np.array(allurlsdata)

random.shuffle(allurlsdata)
y = [d[1] for d in allurlsdata]
corpus = [d[0] for d in allurlsdata]
#corpus = df['url']
#y = df['label']
vectorizer = TfidfVectorizer(tokenizer=getTokens)
X = vectorizer.fit_transform(corpus)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)
lgs = LogisticRegression(solver='lbfgs',max_iter=1000)
lgs.fit(X_train, y_train)

pickle.dump(lgs, open('LOGmodel.pkl', 'wb'))
print(lgs.score(X_test, y_test))
