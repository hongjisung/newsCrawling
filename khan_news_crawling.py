# coding:'utf-8'

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

OUTPUT_FILE_NAME = 'new_crawl_khan.csv'
TODAY = '20170828'


url_firsts = ['http://news.khan.co.kr/kh_news/khan_art_list.html?code=910000&page=',\
             'http://biz.khan.co.kr/khan_art_list.html?page=',\
             'http://biz.khan.co.kr/khan_art_list.html?category=market&page=',\
             'http://biz.khan.co.kr/khan_art_list.html?category=life&page=',\
             'http://biz.khan.co.kr/khan_art_list.html?category=car&page=',\
             'http://biz.khan.co.kr/khan_art_list.html?category=tech&page=',\
             'http://biz.khan.co.kr/khan_art_list.html?category=realty&page=',\
             'http://news.khan.co.kr/kh_news/khan_art_list.html?code=940000&page=',\
             'http://news.khan.co.kr/kh_news/khan_art_list.html?code=62_local&page=',\
             'http://news.khan.co.kr/kh_news/khan_art_list.html?code=970000&page=',\
             'http://news.khan.co.kr/kh_news/khan_art_list.html?code=960000&page=',\
             'http://news.khan.co.kr/kh_news/khan_art_list.html?code=980000&page=',\
             'http://news.khan.co.kr/kh_news/khan_art_list.html?code=960801&page=']



def get_title_text(URL):
    req = urllib.request.Request(URL, None, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'})
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(req)
    soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')

    title = ''
    title = str(soup.find('h1', id='article_title'))
    title = re.sub('<[.\s\S]*?>', '', title)
    title = re.sub('\[[.\s\S]*?\]', '', title)

    text = ''
    for i in soup.find_all('p', class_='content_text'):
        text += str(i)
    text = re.sub('<[.\s\S]*?>', '', text)


    return (title, text)

def get_url_text(open_output_file):
    article_num = 0
    for url_first in url_firsts:
        page = 1
        while page:
            URL = url_first+ str(page)

            req = urllib.request.Request(URL, None, {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'})
            cj = CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            response = opener.open(req)
            soup = BeautifulSoup(response, 'html.parser', from_encoding='utf-8')

            article_urls =[]
            for soup3 in soup.find_all('strong'):
                if soup3.find('a'):
                    the_article_url = '' + str(soup3.find('a')['href'])
                    article_urls+=[the_article_url]
            if article_urls==[]:
                break
            page +=1

            for art_url in article_urls:
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

