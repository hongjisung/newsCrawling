from bs4 import BeautifulSoup
import re
import csv
import urllib
import urllib.request
import html.parser
import requests
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar

OUTPUT_FILE_NAME = 'new_crawl_hani.csv'
TODAY = '20170828'

url_firsts =['http://www.hani.co.kr/arti/politics/list',\
             'http://www.hani.co.kr/arti/society/list',\
             'http://www.hani.co.kr/arti/economy/list',\
             'http://www.hani.co.kr/arti/international/list',\
             'http://www.hani.co.kr/arti/culture/list',\
             'http://www.hani.co.kr/arti/sports/list',\
             'http://www.hani.co.kr/arti/science/list']
url_last = '.html'


def get_title_text(URL):
    req = urllib.request.urlopen(URL)
    soup = BeautifulSoup(req, 'html.parser', from_encoding='utf-8')
    title = ''
    text = ''
    title = str(soup.find('span', class_='title'))
    text = str(soup.find('div', class_='text'))
    title = re.sub('<[.\s\S]*?>', '', title)
    text = re.sub('<div[.\s\S]*?>', '', text)
    text = re.sub('<p[.\s\S]*?</p>', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('<[.\s\S]*?>', '', text)

    return (title, text)


def get_url_text(open_output_file):
    article_num = 0
    for url_first in url_firsts:
        page = 1
        while page<300:
            URL = url_first+ str(page) + url_last

            req = urllib.request.urlopen(URL)
            soup = BeautifulSoup(req, 'html.parser', from_encoding='utf-8')

            art_urls = []
            url_f = 'http://www.hani.co.kr'

            if re.search('2017-05-01', str(soup.find('span', class_='date'))):
                break

            for soup3 in soup.find_all('h4', class_='article-title'):
                art_urls += [url_f + soup3.find('a')['href']]
            if art_urls==[]:
                break
            page +=1

            for art_url in art_urls:
                article_num+=1
                output = get_title_text(art_url)
                print(article_num)
                print(output[0])
                print(output[1])
                open_output_file.writerow([article_num, output[0], output[1]])


def main():
    open_file = open(OUTPUT_FILE_NAME, 'w', encoding='utf-8')
    open_output_file = csv.writer(open_file,delimiter=',', quoting=csv.QUOTE_MINIMAL)

    get_url_text(open_output_file)
    open_file.close()


if __name__ == '__main__':
    main()

