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

OUTPUT_FILE_NAME = 'new_crawl_ohmy.csv'
TODAY = '20170828'
url_first ='http://www.ohmynews.com/NWS_Web/Articlepage/Total_Article.aspx?PAGE_CD=N0120&pageno='

def get_title_text(URL):
    req = urllib.request.urlopen(URL)
    soup = BeautifulSoup(req, 'html.parser', from_encoding='utf-8')
    #print(soup)
    title = ''
    text = ''
    title = str(soup.find('h3', class_='tit_subject'))
    text = str(soup.find('div', class_='at_contents'))
    title = re.sub('<[.\s\S]*?>', '', title)
    text = re.sub('<script[.\s\S]*?</script>', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('<[.\s\S]*?>', '', text)

    return (title, text)

def get_title_text_star(URL):
    req = urllib.request.urlopen(URL)
    soup = BeautifulSoup(req, 'html.parser', from_encoding='utf-8')
    #print(soup)
    title = ''
    text = ''
    title = str(soup.find('h2', class_='tit').find('a')['href'])
    text = str(soup.find('div', class_='text'))
    title = re.sub('<[.\s\S]*?>', '', title)
    text = re.sub('<script[.\s\S]*?</script>', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('<[.\s\S]*?>', '', text)

    return (title, text)


def get_url_text(open_output_file):
    article_num = 0
    page = 1
    while page:
        URL = url_first + str(page)

        req = urllib.request.urlopen(URL)
        soup = BeautifulSoup(req, 'html.parser', from_encoding='utf-8')
        url_f = 'http://www.ohmynews.com/'
        art_urls = []
        for soup2 in soup.find_all('div', class_='cont'):
            if re.search('17.05.01', str(soup2.find('p', class_='source'))):
                break

            url = soup2.find('a')['href']
            if url[:4] == 'http':
                art_urls += [url]
            else:
                art_urls += [url_f + url]

        if art_urls == []:
            break
        page += 1

        for art_url in art_urls:
            article_num += 1
            ouput = ''
            if art_url[:11] == 'http://star':
                output = get_title_text_star(art_url)
            else:
                output = get_title_text(art_url)
            print(art_url)
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
