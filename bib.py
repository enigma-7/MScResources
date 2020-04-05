import os

def arxiv(file):
    digits = [str(i) for i in range(10)]
    if(file[0] in digits):
        return True
    else:
        return False

filenames = [name.split('.pdf')[:-1][0] for name in list(filter(arxiv, os.listdir()))]
filenames = [name.split('v')[0] for name in filenames]
filenames.sort()

import requests
import urllib.request
from bs4 import BeautifulSoup
import textwrap

def extract(response):
    soup     = BeautifulSoup(response.text, 'html.parser')
    url      = soup.find_all('span', class_="arxivid")[-1].find_all('a')[0].get('href')
    arxivid  = soup.find_all('span',class_="arxivid")[0].text.split(':')[-1].split(' [')[0]
    # title    = "// ".join(textwrap.wrap(soup.title.string.split('] ')[-1], 48))
    title = textwrap.wrap(soup.title.string.split('] ')[-1], 48)[0]
    authors  = soup.find_all('div', class_="authors")[0].text.split(':')[-1]
    abstract = soup.find_all('blockquote', class_="abstract mathjax")[0].text
    return ["\\href{%s}{%s}"%(url,arxivid), title, authors]

info = []
for file in filenames:
    url      = 'https://arxiv.org/abs/' + file
    response = requests.get(url)
    if response.status_code == 404:
        url      = 'https://arxiv.org/abs/hep-ph/' + file
        response = requests.get(url)
        if response.status_code == 404:
            url      = 'https://arxiv.org/abs/hep-th/' + file
            response = requests.get(url)
    print(file)
    info.append(extract(response))

info

import pandas as pd
info = pd.DataFrame(info, columns=["arXiv", "Title", "Authors"])
pd.set_option('display.max_colwidth', -1)
info.to_latex(buf='bib.tex')
