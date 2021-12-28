import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz

df_1=pd.read_csv('./data/domain.csv')
dom=list(df_1['domain'])

viruses=['exe','stuxnet','vbs','vb','cmd','hta','scr','msi','msp','pif','htm','js','jar','bat','dli','tmp','py']      
def url_split(url):
    a=url.split('/')
    a.remove('')
    #print(a)
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
    val=[]
    for i in dom:
        k=fuzz.ratio(b,str(i))
        if (k>=75):
            return -3
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
            if int(crt_date) >= 120:
                return 4
            elif int(crt_date) <= 6:
                return -2
            else:
                return 2
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
        return 1
    else:
        return -2

def deepcheck(url):
    sum=2
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
            if (q==4):
                return 4
            if(q==-2):
                sum=sum+q
                return sum
            elif(q==2):
                e=check_http(url)
                if(e==-1):
                    sum=sum+e
                    return sum
                else:
                    return sum
        return sum
    else:
        q=url_length(url)
        if (q==-1 or q==-2):
            sum=sum+q
            q=check_path(url)
            sum=sum+q
            return sum