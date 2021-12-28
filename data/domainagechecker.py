import requests
from bs4 import BeautifulSoup


def getdomain_age(domain):
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

#print(getdomain_age('google.com'))