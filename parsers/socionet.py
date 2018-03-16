import requests
from bs4 import BeautifulSoup
from time import sleep
import os, sys
from datetime import datetime
from transliterate import translit
# https://socionet.ru/find.html

base_dir = None
base_url = 'https://socionet.ru/search/runsearch.cgi'
#base_dir = datetime.now().strftime('%Y-%m-%d-%H-%M')
# base_dir = 'data'
# if not os.path.exists(base_dir):
#     os.mkdir(base_dir)


def get_urls(html):
    print('Socionet: Start getting urls')
    urls = []
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('a')
    for tag in tags:
        url = tag.get('href')
        urls.append(url)
    result_urls = []
    for url in urls:
        if 'cyberleninka' not in url:
            sleep(1)
            html_page = requests.get(url).text
            soup = BeautifulSoup(html_page, 'lxml')
            url_new = soup.find('table', id='m_content_tbl').find('td', class_='ar-on', bgcolor='gray')
            url_new = url_new.find('a').get('title')
            name = soup.find('table', id='m_content_tbl').find('table', class_='com_tbl').find('td', class_='ar-on')
            name = name.text.strip()
            name = name.split('//')[0][:-1].lower()
            result_urls.append((name, url_new))
    print('Socionet: Finish getting urls')
    return result_urls


def download_file(name, url):
    print('Socionet: I am download.....')
    sleep(1)
    r = requests.get(url, stream=True)
    file_name = name + '.' + url.split('.')[-1]
    if file_name not in os.listdir(base_dir):
        with open(base_dir + '/' + file_name, 'wb') as file:
            for chunk in r.iter_content(4096):
                file.write(chunk)
        print('Socionet:', file_name, 'is done')


def socionet(b_dir):
    global base_dir
    base_dir= b_dir
    sys.stdout = open('/'.join(base_dir.split('/')[:2]) + '/' + 'log_socionet.txt', 'a', encoding='utf-8')
    try:
        r = requests.post(base_url, data={
            'author-name': 'Черненький В.М.',
            'justtext': '',
            'fulltext': 'fulltext',  # fulltext
            'tr1': '',
            'tr2': '',      # 14 марта 1971
            'accept-charset': 'utf-8',
        })
    except requests.exceptions.ConnectionError:
        print('Socionet: Проверьте соединение с сетью')
        return 0
    html = r.text
    names_urls = get_urls(html)
    if names_urls:
        for name, url in names_urls:
            download_file(name, url)
    else:
        print('Socionet: Возникла ошибка, проверьте доступность запрашиваемых материалов')


if __name__ == '__main__':
    socionet('data')
