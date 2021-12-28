#Importing dependencies
from urllib.parse import urlparse
import re
import pandas as pd 
import requests
from bs4 import BeautifulSoup

## Functions
def digit_count(url):
    digits = 0
    for i in url:
        if i.isnumeric():
            digits = digits + 1
    return digits

def letter_count(url):
    letters = 0
    for i in url:
        if i.isalpha():
            letters = letters + 1
    return letters

def no_of_dir(url):
    urldir = urlparse(url).path
    return urldir.count('/')

#First Directory Length
def fd_length(url):
    urlpath= urlparse(url).path
    try:
        return len(urlpath.split('/')[1])
    except:
        return 0

#Length of Top Level Domain

def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1

def getdomainage(domain):
  '''
  Return 1 if domain age >= 6 months
  else returns 0
  '''  
  url = "https://www.ipvoid.com/domain-age-checker/"
  r = requests.post(url, {'host': domain, 'submit': 'submit'})
  soup = BeautifulSoup(r.content, features="html.parser")

  for item in soup.find_all('textarea'):
    res = item.text
    crt_date = res.split('\n')[2].split(':')[1].strip().split(' ')[0]
    if int(crt_date) >= 6:
        return 1
    return 0

def having_ip_address(url):
    match = re.search(
        '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
        '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
        '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
        '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}', url)  # Ipv6
    if match:
        # print match.group()
        return -1
    else:
        # print 'No matching pattern found'
        return 1

def shortening_service(url):
    match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                      'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                      'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                      'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                      'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                      'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                      'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|'
                      'tr\.im|link\.zip\.net',
                      url)
    if match:
        return -1
    else:
        return 1


def applyall(uri):
    data = {'url':[uri],
    'short_url':[shortening_service(uri)],
    'use_of_ip':[having_ip_address(uri)],
    'count-':[(lambda url : url.count('-') )(uri)], 
    'count@':[(lambda url : url.count('@') )(uri)], 
    'count?':[(lambda url : url.count('?') )(uri)],
    'count%':[(lambda url : url.count('%') )(uri)], 
    'count.':[(lambda url : url.count('.') )(uri)], 
    'count=':[(lambda url : url.count('=') )(uri)], 
    'count-http':[(lambda url : url.count('http') )(uri)], 
    'count-https':[(lambda url : url.count('https') )(uri)], 
    'count-www':[(lambda url : url.count('www') )(uri)], 
    'count-digits':[digit_count(uri)], 
    'count-letters':[letter_count(uri)], 
    'count_dir':[no_of_dir(uri)], 
    'url_length':[len(uri)], 
    'hostname_length':[len(urlparse(uri).netloc)], 
    'path_length':[len(urlparse(uri).path)], 
    'fd_length':[fd_length(uri)], 
    'tld_length':[tld_length(uri)]
    }
    df = pd.DataFrame(data)
    x = df[['short_url', 'use_of_ip', 'count-', 'count@', 'count?', 'count%', 'count.', 'count=', 'count-http', 'count-https', 'count-www', 'count-digits', 'count-letters', 'count_dir', 'url_length', 'hostname_length', 'path_length', 'fd_length', 'tld_length']]
    return x