import requests
from bs4 import BeautifulSoup
from time import sleep
import os, sys

base_dir = None
base_url = 'https://scholar.google.ru/scholar'
#base_dir = datetime.now().strftime('%Y-%m-%d-%H-%M')
# base_dir = 'data'
# if not os.path.exists(base_dir):
#     os.mkdir(base_dir)
# https://scholar.google.ru/scholar?hl=ru&q=
# https://scholar.google.ru/scholar?hl=ru&as_sdt=0,5&as_ylo=1996&as_yhi=1997&q=KeyWord+author%3AAuthor
# https://scholar.google.ru/scholar?as_q=key1+key2&as_epq=&as_oq=&as_eq=&as_occt=any&as_sauthors=Author&as_publication=&as_ylo=1996&as_yhi=1997&hl=ru&as_sdt=0%2C5
# По вашему запросу – KeyWord author:Author – не найдено статей, опубликованных с 1996 по 1997.

#https://scholar.google.ru/scholar?as_vis=1&q=author:черненький



def get_urls(html):
    soup = BeautifulSoup(html, 'lxml')
    resourses = soup.find('div', id='gs_res_ccl_mid').find_all('div', class_='gs_r gs_or gs_scl')
    name_urls = []
    for res in resourses:
        try:
            url = res.find('div', class_='gs_ggs gs_fl').find('a').get('href')
            name = res.find('div', class_='gs_ri').find('h3', class_='gs_rt').find('a').text
            if 'cyberleninka' not in url:
                name_urls.append((name, url))
        except:
            continue
    return name_urls

def download_file(name, url):
    print('Scholar: I am download.....')
    sleep(1)
    try:
        r = requests.get(url, stream=True)
    except:
        print('Scholar:', name, 'is not download')
        return 0
    postfix = url.split('.')[-1]
    if '#' in postfix:
        return 0
    if '/' in postfix:
        postfix = 'html'
    file_name = name.lower() + '.' + postfix
    if file_name not in os.listdir(base_dir):
        with open(base_dir + '/' + file_name, 'wb') as file:
            for chunk in r.iter_content(4096):
                file.write(chunk)
        print('Scholar:', file_name, 'is done')

def scholar(b_dir):
    global base_dir
    base_dir= b_dir
    sys.stdout = open('/'.join(base_dir.split('/')[:2]) + '/' + 'log_scholar.txt', 'a', encoding='utf-8')
    params = {
        'q': 'author:Черненький В.М.',
        'as_vis': 1,   # без цитат
        'start': 0,  # страницы 10 20 ...80
    }
    while True:
        print('Scholar: Беру страницу...')
        sleep(2)
        try:
            r = requests.get(base_url, params=params)
        except:
            print('Scholar: Проверьте соединение с сетью')
            break
        print(r.url)
        html = r.text
        name_urls = get_urls(html)
        if name_urls:
            for name, url in name_urls:
                download_file(name, url)
        else:
            print('Scholar: I finish')
            break
        params['start'] += 10

if __name__ == '__main__':
    scholar('data')