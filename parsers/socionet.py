import requests
from bs4 import BeautifulSoup
from time import sleep
import os, sys
# https://socionet.ru/find.html


base_dir = None
base_url = 'https://socionet.ru/search/runsearch.cgi'


def get_urls(html):
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
    return result_urls


def download_file(name, url):
    try:
        sleep(1)
        r = requests.get(url, stream=True)
        postfix = url.split('.')[-1]
        if '#' in postfix:
            return 0
        if '/' in postfix:
            postfix = 'html'
        file_name = name + '.' + postfix
        print('Socionet: начинаю загрузку:', file_name)
        if file_name not in os.listdir(base_dir):
            with open(base_dir + '/' + file_name, 'wb') as file:
                for chunk in r.iter_content(4096):
                    file.write(chunk)
            print('Socionet:', file_name, ' загружен')
        else:
            print('Socionet: файл уже существует')
    except:
        print('Socionet: ошибка загрузки')


def socionet(b_dir, author='', title='', keywords='', year1='', year2=''):
    global base_dir
    base_dir= b_dir
    #sys.stdout = open('/'.join(base_dir.split('/')[:2]) + '/' + 'log_socionet.txt', 'a', encoding='utf-8')
    print('Socionet: начал работу')
    if title:
        return 0
    try:
        r = requests.post(base_url, data={
            'author-name': author,
            'justtext': keywords, # ключевые слова
            'fulltext': 'fulltext',  # fulltext
            'tr1': year1,
            'tr2': year2,      # 14 марта 1971
            'accept-charset': 'utf-8',
        })
        print('Socionet: запрос:', r.url)
    except requests.exceptions.ConnectionError:
        print('Socionet: проверьте соединение с сетью')
        return 0
    html = r.text
    names_urls = get_urls(html)
    if names_urls:
        for name, url in names_urls:
            download_file(name, url)
        print('Socionet: загрузка завершена')
    else:
        print('Socionet: проверьте доступность запрашиваемых материалов')


if __name__ == '__main__':
    socionet('data')
