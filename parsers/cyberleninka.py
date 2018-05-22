import requests
from bs4 import BeautifulSoup

import config
from parsers.download import download_file

base_url = 'https://cyberleninka.ru'


def count_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        pages = len(soup.find('ul', class_='paginator').find_all('li'))
    except AttributeError:
        return 1
    return pages


def author_problem(author, element):
    head_author = element.find_next('span').text.strip()
    try:
        author_list = author.split()
        author1 = author_list[0] + ' ' + author_list[1] + ' ' + author_list[2]
        author2 = author_list[0] + ' ' + author_list[1] + author_list[2]
        author3 = author_list[1] + author_list[2] + ' ' + author_list[0]
        author4 = author_list[1] + ' ' + author_list[2] + ' ' + author_list[0]
        if (author1 == author1 in head_author)\
                or (author2 == author2 in head_author)\
                or (author3 == author3 in head_author)\
                or (author4 == author4 in head_author):
            return True
    except IndexError:
        if author == author in head_author:
            return True
    return False


def get_urls(html, author=''):
    name_urls = []
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('h2', class_='title')
    for article in articles:
        if author_problem(author, article):
            url = base_url + article.find('a').get('href') + '.pdf'
            name = article.find('a').text.strip()
            name_urls.append((name, url))
    return name_urls


def get_data_fom_page(html, author=''):
    names_urls = get_urls(html, author)
    if names_urls:
        for name, url in names_urls:
            download_file(name, url, 'Cyberleninka')
    else:
        config.write_log('Cyberleninka: материалы не найдены')


def cyberleninka(author='', title='', keywords='', year1='', year2=''):

    config.debug('Cyberleninka')
    config.write_log('Cyberleninka: начал работу')

    query = {
        '@author': author,
        '@name': title,  # название статьи
        '@keywords': keywords,  # ключевые слова
        '@year': year1 or year2,  # поиск по году точный
    }
    params = {
        'q': ' '.join([k+' '+v for k, v in query.items() if v]),
        'page': 1
    }

    try:
        r = requests.get(base_url+'/search', params=params)
    except requests.exceptions.ConnectionError:
        config.write_log('Cyberleninka: ошибка при выполнении запроса')
        return 0

    config.write_log('Cyberleninka: запрос: ' + str(r.url))
    config.to_json({
        'BaseUrlParser': {
            'url_cyberleninka': r.url
        }
    })
    html = r.text
    pages = count_pages(html)
    if pages:
        get_data_fom_page(html, author)
        for i in range(2, pages+1):
            params['page'] = i

            try:
                html = requests.get(base_url+'/search', params=params).text
            except requests.exceptions.ConnectionError:
                config.write_log('Cyberleninka: ошибка при выполнении запроса')
                return 0

            get_data_fom_page(html)
        config.write_log('Cyberleninka: работа завершена')


if __name__ == '__main__':
    cyberleninka(author='Черненький В. М.', title='система')