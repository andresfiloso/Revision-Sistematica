arg = "data"
from bs4 import BeautifulSoup
import requests
import re

urlScience = "https://www.sciencedirect.com/search?qs=" + arg + "&show=100&sortBy=relevance"
req = requests.get(urlScience)
statusCode = req.status_code
html = BeautifulSoup(req.text, "html.parser")
rawScience = html.findAll('div', {'class': 'result-item-content'})

for link in rawScience:
    result = "https://www.sciencedirect.com" + link.a['href']

    req = requests.get(result)
    statusCode = req.status_code
    html = BeautifulSoup(req.text, "html.parser")
    title = html.find_all('span', {'class': 'title-text'})
    abstract = html.find_all('div', {'class': 'abstract author'})

    print title
    print result
    print abstract
