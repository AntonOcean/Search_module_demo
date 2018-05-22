import requests
import os
from time import sleep

from config import to_json, base_dir, write_log


def download_file(name, url, name_parser):
    sleep(1)
    try:
        r = requests.get(url, stream=True)

        postfix = url.split('.')[-1]
        if '#' in postfix:
            return 0
        if '/' in postfix:
            postfix = 'html'
        file_name = name.lower() + '.' + postfix

        write_log(name_parser + ': начинаю загрузку: ' + file_name)

        if file_name not in os.listdir(base_dir):
            with open(base_dir + '/' + file_name, 'wb') as file:
                for chunk in r.iter_content(4096):
                    file.write(chunk)

            file_name_clear = base_dir + '/' + file_name
            if os.stat(file_name_clear).st_size < 5:
                os.remove(file_name_clear)
                raise RuntimeError

            write_log(name_parser + ': ' + file_name + ' загружен')
            to_json({
                'Document':
                    {
                        'local_url': os.path.abspath(file_name_clear),
                        'net_url': url,
                        'title': file_name
                    }
            })
        else:
            write_log(name_parser + ': файл уже существует')
    except (requests.exceptions.ConnectionError, TimeoutError, RuntimeError):
        write_log(name_parser + ': ошибка загрузки')
