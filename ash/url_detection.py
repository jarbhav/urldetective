from functools import wraps
from flask import Flask
import pandas as pd
from flask import request, Response
from subprocess import call
from flask import render_template
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import os
from sklearn.linear_model import LogisticRegression
import math
from collections import Counter
import pickle
import whois
import re

import requests
from bs4 import BeautifulSoup

#df_1=pd.read_csv('domain.csv')
#dom=list(df_1['domain'])
from fuzzywuzzy import fuzz
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



    
def TL():
  allurlsdata = pd.DataFrame(df)
  
  allurlsdata = np.array(allurlsdata)
  
  random.shuffle(allurlsdata)
  y = [d[1] for d in allurlsdata]

  corpus = [d[0] for d in allurlsdata]
  vectorizer = TfidfVectorizer(tokenizer=getTokens)
  X = vectorizer.fit_transform(corpus)
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

  lgs = LogisticRegression(solver='lbfgs',max_iter=1000)
  lgs.fit(X_train, y_train)
#new
  pickle.dump(lgs, open('model.pkl', 'wb'))
#  print(lgs.score(X_test, y_test))
  return vectorizer, lgs



vectorizer, lgs = TL()
#print(vectorizer,lgs)
#file1=open("vect.txt","w")
#file2=open("lgs.txt","w")
#file1.write(vectorizer)
#file2.write(lgs)
#file1.close()
#file2.close()
"""
url='http://www.google.com'
X_predict = [url]
X_predict = vectorizer.transform(X_predict)
y_Predict = lgs.predict(X_predict)
print(y_Predict)
#if (y_Predict=='good'):
#model = pickle.load(open('model.pkl', 'rb'))
#url='http://www.wikipedia.com'

#y_Predict_1 = model.predict(X_predict)

#print(y_Predict_1)
viruses=['exe','stuxnet','vbs','vb','cmd','hta','scr','msi','msp','pif','htm','js','jar','bat','dli','tmp','py']      
def url_split(url):
    a=url.split('/')
    a.remove('')
    print(a)
    return a
def check_http(url):
    a=url.split('/')
    if a[0]=='http:': 
        return -1
    elif  a[0]=='https:':
        return 1
    else:
        return 0

def Validate_It(IP):
        regex = "(([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])\\.){3}"\
            "([0-9]|[1-9][0-9]|1[0-9][0-9]|"\
            "2[0-4][0-9]|25[0-5])"
        regex1="((([0-9a-fA-F]){1,4})\\:){7}"\
             "([0-9a-fA-F]){1,4}"
        p = re.compile(regex)
        p1 = re.compile(regex1)     
        if (re.search(p, IP)):
            return -3
        elif (re.search(p1, IP)):
            return -3
        return 1
def prefix_suffix_domain(domain):
    a=domain.split('/')
    if '' in a:
        a.remove('')
    if 'http:' in a:
        a.remove('http:')
    elif  'https:' in a:
        a.remove('https:')
    k=a[0].split('.')
    if 'www' in k:
        k.remove('www')
    b=str(k[0])
#    print(b)
    val=[]
    for i in dom:
        k=fuzz.ratio(b,str(i))
#        print(k,i)
        if (k>=75):
    #        print(k)
            return -3
   
#    print(max(val))
    return 0
        
    
    
def check_path(path):
    k=0
    string=''
    for j in range(2,len(path)):
        for i in range(0,len(viruses)):
            if viruses[i] in path[j]:
                k=-2
                break
        if (k!=0):
            break
    return 1

def url_length(url):
    if len(url)<54:
        return 1
    elif  len(url)>54 and len(url)<=75:
        return -1       
    else:
        return -2

def domain_age(domain):
    url = "https://www.ipvoid.com/domain-age-checker/"
    domain=domain.split('/')
    if '' in domain:
        domain.remove('')
    if 'http:' in domain:
        domain.remove('http:')
    elif 'https:' in domain:
        domain.remove('https:')
    domain=domain[0]
    try:
        r = requests.post(url, {'host': domain, 'submit': 'submit'})
        soup = BeautifulSoup(r.content, features="html.parser")
        for item in soup.find_all('textarea'):
            res = item.text
            crt_date = res.split('\n')[2].split(':')[1].strip().split(' ')[0]
            if int(crt_date) >= 6:
                return 2
            return -2
    except:
        return 0

def domain_check(domain):
    a=domain.split('/')
    if '' in a:
        a.remove('')
    if 'http:' in a:
        a.remove('http:')
    elif  'https:' in a:
        a.remove('https:')
    k=a[0].split('.')
    if 'www' in k:
        k.remove('www')
    if k[0] in dom:
        return 2
    else:
        return -2


def deepcheck(url):
    sum=0
    p=Validate_It(url)
    if(p==-3):
        sum=sum+p
        return -3
    else:
        q=domain_check(url)
        sum=sum+q
    if (q==-2):
        q=prefix_suffix_domain(url)
        sum=sum+q
        if (q==-3):
            q=domain_age(url)
            if(q==-2):
                sum=sum+q
                return sum
    else:
        q=url_length(url)
        if (q==-1 or q==-2):
            sum=sum+q
            q=check_path(url)
            sum=sum+q
            return sum


if (y_Predict=='good'):
    a=deepcheck(url)
    if (a<0 and a>=-2):
        print("Phishy")
    elif (a<-2):
        print("Malacious")
    else:
        print("Safe")
else:
    a=domain_check(url)
    print(a)
    if (a==2):
        q=check_path(url)
        if(q>0):
            print("Safe")
        else:
            print("Phishy")
    else:
        print("Malacious")
    
"""



    
   
    
    
























   
    
