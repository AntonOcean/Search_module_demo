import os, sys
from datetime import datetime
from multiprocessing import Process
import time

from parsers.cyberleninka import cyberleninka
from parsers.scholar import scholar
from parsers.socionet import socionet


timestamp_dir = datetime.now().strftime('%Y-%m-%d-%H-%M')
base_dir = 'data' + '/' + timestamp_dir + '/' + 'documents'
if not os.path.exists(base_dir):
    os.makedirs(base_dir)


def main():
    p1 = Process(target=cyberleninka, args=(base_dir,))
    p2 = Process(target=scholar, args=(base_dir,))
    p3 = Process(target=socionet, args=(base_dir,))
    for p in (p1, p2, p3):
        p.start()
        p.join()
    for file in os.listdir(base_dir):
        file_name = base_dir + '/' + file
        if os.stat(file_name).st_size == 0:
            os.remove(file_name)
    log_data = {
        'Дата запроса: ': timestamp_dir,
        'Файлов загружено: ': len(os.listdir(base_dir)),


    }
    with open('data/log.txt', 'w', encoding='utf-8') as log:
        log.write(log_data)

def test():
    time_start = time.time()
    base_dir = 'data/2018-03-15-18-27/documents'
    time.sleep(5)
    time_end = time.time()
    print(time_end - time_start)


if __name__ == '__main__':
    #main()
    test()