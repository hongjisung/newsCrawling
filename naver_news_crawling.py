# coding:'utf-8'

from bs4 import BeautifulSoup
import urllib.request
import re
import csv


OUTPUT_FILE_NAME = 'new_crawl.csv'
TODAY = '20170828'

URL_first = 'http://news.naver.com/main/list.nhn?'
URL_sid2 = 'sid2='
URL_sid1 = '&sid1='
URL_date = '&mid=shm&mode=LS2D&date='
URL_page = '&page='



sid1_sid2 = [('100', '264'),('100','265'),('100','268'),('100','266'),('100','267'),('100', '269')]\
    +[('101','259'),('101','258'),('101','261'), ('101','771'),('101','260'),('101','262')\
                ,('101','310'),('101','263')]\
    +[('102','249'),('102','250'),('102','251'),('102','254'),('102','252'), ('102','59b')\
                ,('102','255'),('102','256'),('102','276'),('102','257')]\
    +[('103','241'),('103','239'), ('103','240'),('103','237'),('103','238'),('103','376'),('103','242')\
                ,('103','242'),('103','243'),('103','244'),('103','248'),('103','245')]\
    +[('104','231'),('104','232'),('104','233'),('104','234'),('104','322')]\
    +[('105','731'),('105','226'),('105','227'),('105','230'),('105','732')\
                ,('105','283'),('105','229'),('105','228')]

year = ['2017','2016','2015']
month = ['0'+str(i) for i in range(1,10)] +['10','11','12']
day = ['0'+str(i) for i in range(1,10)]+[str(i) for i in range(10,32)]
month.reverse()
day.reverse()

def get_title(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser', from_encoding='utf-8')
    title = ''
    for item in soup.find_all(id='articleTitle'):
        title = title + str(item.find(text=True))
    if title == '':
        title = title +str(soup.find('title').find(text=True))

    title = re.sub('\[[.\s\S]*?\]', '', title)
    title = re.sub('[\n\t\r\v>,]*', '', title)
    return title


def get_text(URL):
    source_code_from_URL = urllib.request.urlopen(URL)
    soup = BeautifulSoup(source_code_from_URL, 'html.parser', from_encoding='utf-8')
    text = ''
    rm_useless = re.compile('<[.\s\S]*?>')

    for item in soup.find_all('div', id='articleBodyContents'):
        text = text + str(item.find_all)

    if text == '':
        for item in soup.find_all('div', id='newsEndContents'):
            text = text + str(item.find_all)
    if text == '':
        for item in soup.find_all('div', id='articeBody'):
            text = text + str(item.find_all)

    text = re.sub(rm_useless, '', text)
    text = re.sub('\[[.\s\S]*?\]', '', text)
    text = re.sub('[\n\t\r\v>,]*', '', text)
    text = re.sub('\/\/ flash 오류를 우회하기 위한 함수 추가function _flash_removeCallback\(\) \{\}'\
                  , '', text)
    text = re.sub('\([.\s\S]*?\)', '', text)

    return text

def get_url_text(open_output_file):
    URL1 = URL_first
    for y in year:
        for m in month:
            for d in day:
                ymd = y + m + d
                if ymd > TODAY:
                    continue
                for sid_tuple in sid1_sid2:
                    URL2 = URL1 + URL_sid2 + sid_tuple[1] + URL_sid1 + sid_tuple[0] + URL_date

                    URL3 = URL2 + ymd + URL_page

                    check_page = ''
                    push_article_to_file = []
                    for page_num in range(1, 100):
                        page_article_data = []
                        the_article_url = ''
                        URL4 = URL3 + str(page_num)
                        source_url = urllib.request.urlopen(URL4)

                        soup = BeautifulSoup(source_url, 'html.parser', from_encoding='utf-8')
                        for soup2 in soup.find_all('div', id='main_content'):
                            for soup3 in soup2.find_all('dt'):
                                if soup3.find('img'):
                                    continue
                                the_article_url = '' + str(soup3.find('a')['href'])

                                page_article_data +=[[str(ymd), sid_tuple, get_title(the_article_url), \
                                                      get_text(the_article_url)]]
                            if page_num == 100:
                                break
                        if check_page != the_article_url:
                            check_page = '' + the_article_url
                        else:
                            break
                        push_article_to_file+=page_article_data

                        if page_num == 100:
                            break
                    for i in push_article_to_file:
                        print (sid_tuple)
                        open_output_file.writerow(i)

                if ymd == TODAY:
                    return



def main():
    open_file = open(OUTPUT_FILE_NAME, 'w', encoding='utf-8')
    open_output_file = csv.writer(open_file,delimiter=',', quoting=csv.QUOTE_MINIMAL)

    get_url_text(open_output_file)
    open_file.close()


if __name__ == '__main__':
    main()

