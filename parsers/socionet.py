import requests
from bs4 import BeautifulSoup
from time import sleep
# https://socionet.ru/find.htm

import config
from parsers.download import download_file

base_url = 'https://socionet.ru/search/runsearch.cgi'


def author_and_title_problem(author, title, element):
    head = element.text.strip()
    try:
        author_list = author.split()
        author1 = author_list[0] + ' ' + author_list[1] + ' ' + author_list[2]
        author2 = author_list[0] + ' ' + author_list[1] + author_list[2]
        author3 = author_list[1] + author_list[2] + ' ' + author_list[0]
        author4 = author_list[1] + ' ' + author_list[2] + ' ' + author_list[0]
        if ((author1 == author1 in head)
            or (author2 == author2 in head)
            or (author3 == author3 in head)
            or (author4 == author4 in head))\
                and (title.lower() == title.lower() in head.lower()):
            return True
    except IndexError:
        if (author == author in head) and (title.lower() == title.lower() in head.lower()):
            return True
    return False


def get_urls(html, author='', title=''):
    urls = []
    soup = BeautifulSoup(html, 'lxml')
    tags = soup.find_all('a')
    for tag in tags:
        if author_and_title_problem(author, title, tag):
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


def socionet(author='', title='', keywords='', year1='', year2=''):

    config.debug('Socionet')
    config.write_log('Socionet: начал работу')

    if title:
        keywords = title + ' ' + keywords

    try:
        r = requests.post(base_url, data={
            'author-name': author,
            'justtext': keywords,  # ключевые слова
            'fulltext': 'fulltext',  # fulltext
            'tr1': year1,
            'tr2': year2,      # 14 марта 1971
            'accept-charset': 'utf-8',
        })
    except requests.exceptions.ConnectionError:
        config.write_log('Socionet: ошибка при выполнении запроса')
        return 0

    config.write_log('Socionet: запрос:' + str(r.url))
    config.to_json({
        'BaseUrlParser': {
            'url_socio': r.url
        }
    })
    html = r.text

    names_urls = get_urls(html, author, title)
    if names_urls:
        for name, url in names_urls:
            download_file(name, url, 'Socionet')
        config.write_log('Socionet: работа завершена')
    else:
        config.write_log('Socionet: материалы не найдены')


if __name__ == '__main__':
    socionet(author='Жуков В. Т.', title='метод', year1='2011', year2='2012')
