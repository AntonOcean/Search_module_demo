from multiprocessing import Process

from parsers.cyberleninka import cyberleninka
from parsers.scholar import scholar
from parsers.socionet import socionet

import time


def parsing(author, title, keywords, year1, year2):
    time_start = time.time()
    p1 = Process(target=cyberleninka, args=(author, title, keywords, year1, year2))
    p2 = Process(target=scholar, args=(author, title, keywords, year1, year2))
    p3 = Process(target=socionet, args=(author, title, keywords, year1, year2))
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()
    time_end = time.time()
    return time_end - time_start
