import requests
from bs4 import BeautifulSoup

url = 'https://www.indeed.com/jobs?'
result = requests.get(url)
# result = result.text.find('span', {'class':'icl-u-lg-block icl-Heading3 icl-u-lg-my--none'})
print(result.text)