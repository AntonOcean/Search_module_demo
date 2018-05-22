import os
import json


from parsers.parsing import parsing
import config


def write_json(data):
    with open(config.path_document_dir + 'temp.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main(author='', title='', keywords='', year1='', year2=''):
    config.config()
    if not os.path.exists(config.base_dir):
        os.makedirs(config.base_dir)

    data = {
        'UserQuery': {
            'timestamp': config.timestamp_dir,
            'author': author,
            'title': title,
            'keywords': keywords,
            'year1': year1,
            'year2': year2
        },
        'Document': [],
        'BaseUrlParser': {
            'url_cyberleninka': '',
            'url_scholar': '',
            'url_socio': ''
        }
    }
    write_json(data)

    time_parse = parsing(author, title, keywords, year1, year2)

    with open(config.path_timestamp_dir + 'log.log', 'a', encoding='utf-8') as log:
        log.write('Дата запроса: ' + config.timestamp_dir + '\n')
        log.write('Файлов загружено: ' + str(len(os.listdir(config.base_dir))) + '\n')
        log.write('Время затраченное: ' + str(int(time_parse)) + ' секунды' + '\n')
        log.write('-Автор: ' + author + '\n')
        log.write('-Название работы: ' + title + '\n')
        log.write('-Ключевые слова: ' + keywords + '\n')
        log.write('-Дата: ' + year1 + ' - ' + year2 + '\n')
        log.write('='*30 + '\n')
    result = json.load(open(config.path_document_dir + 'temp.json', 'r', encoding='utf-8'))
    return result


def test():
    author = 'Черненький В. М.'
    title = ''
    keywords = ''
    year1 = ''
    year2 = ''
    main(author, title, keywords, year1, year2)


if __name__ == '__main__':
    test()
