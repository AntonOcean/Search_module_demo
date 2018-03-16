import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import os, sys

base_dir = None
base_url = 'https://cyberleninka.ru'
#base_dir = datetime.now().strftime('%Y-%m-%d-%H-%M')
# base_dir = 'data'
# if not os.path.exists(base_dir):
#     os.mkdir(base_dir)
#  https://cyberleninka.ru/article/n/elektronnaya-interaktivnaya-doska-programmnoe-obespechenie-i-tehnicheskie-harakteristiki-vliyayuschie-na-effektivnost-obucheniya.pdf
#  https://cyberleninka.ru/article/n/elektronnaya-interaktivnaya-doska-programmnoe-obespechenie-i-tehnicheskie-harakteristiki-vliyayuschie-na-effektivnost-obucheniya


def count_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        pages = len(soup.find('ul', class_='paginator').find_all('li'))
    except AttributeError:
        return 1
    return pages


def get_urls(html):
    name_urls = []
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('h2', class_='title')
    for article in articles:
        url = base_url + article.find('a').get('href') + '.pdf'
        name = article.find('a').text.strip()
        name_urls.append((name, url))
    return name_urls


def download_file(name, url):
    print('Cyberleninka: I am download.....')
    sleep(1)
    r = requests.get(url, stream=True)
    postfix = '.' + url.split('.')[-1]
    file_name = name.lower() + postfix
    if file_name not in os.listdir(base_dir):
        with open(base_dir + '/' + file_name, 'wb') as file:
            for chunk in r.iter_content(4096):
                file.write(chunk)
        print('Cyberleninka:', file_name, 'is done')


def get_data_fom_page(html):
    names_urls = get_urls(html)
    if names_urls:
        for name, url in names_urls:
            download_file(name, url)
    else:
        print('Cyberleninka:', 'Возникла ошибка, проверьте доступность запрашиваемых материалов')


def cyberleninka(b_dir):
    global base_dir
    base_dir = b_dir
    sys.stdout = open('/'.join(base_dir.split('/')[:2]) + '/' + 'log_cyberleninka.txt', 'a', encoding='utf-8')
    query = {
        '@author': 'Черненький В.М.',
        '@name': '',
        '@keywords': '',
        '@year': ''
    }
    params = {
        'q': ' '.join([k+' '+v for k, v in query.items() if v]),
        'page': 1
    }
    try:
        html = requests.get(base_url+'/search', params=params).text
    except requests.exceptions.ConnectionError:
        print('Cyberleninka:', 'Проверьте соединение с сетью')
        return 0
    pages = count_pages(html)
    if pages:
        get_data_fom_page(html)
        for i in range(2, pages+1):
            params['page'] = i
            html = requests.get(base_url+'/search', params=params).text
            get_data_fom_page(html)


if __name__ == '__main__':
    cyberleninka('data')
