import re
import requests
import pandas as pd
from bs4 import BeautifulSoup


def parse_html_re(html):
    obj = re.compile(r'<div class="info">.*?<span class="title">(?P<name>.*?)</span>.*?<span class="rating_num" .*?>'
                     r'(?P<rate>.*?)</span>', re.S)
    res = obj.finditer(html)
    movies = []
    for r in res:
        movies.append((r.group('name'), r.group('rate')))
    return movies


def parse_html_bs(html):
    bs = BeautifulSoup(html, "html.parser")
    res = bs.find_all('div', attrs={"class": "info"})
    movies = []
    for r in res:
        name = r.find_all('span', attrs={"class": "title"})
        rate = r.find_all('span', attrs={"class": "rating_num"})
        movies.append((name[0].text, rate[0].text))
    return movies


def query(start):
    url = 'https://movie.douban.com/top250'
    params = {
        "start": start,
    }
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url, params=params, headers=headers)

    page = res.text
    res.close()
    return parse_html_bs(page)


def main():
    movies = []
    for i in range(10):
        movies.extend(query(start=25*i))
    pd.DataFrame.from_records(movies).to_csv('top250.csv', header=['name', 'score'])


if __name__ == '__main__':
    main()