import os
import json
import logging


base_path_to_timestamp = os.path.dirname(os.path.abspath(__file__)) + '/parsers/' + 'keep_time.txt'

def get_timestamp():
    with open(base_path_to_timestamp) as file:
        timestamp = file.read().strip()
    return timestamp


timestamp_dir = get_timestamp()
base_dir = os.path.dirname(os.path.abspath(__file__)) + '/data/' + timestamp_dir + '/' + 'documents'
path_document_dir = '/'.join(base_dir.split('/')[:3]) + '/'
path_timestamp_dir = '/'.join(base_dir.split('/')[:2]) + '/'


def config():
    global timestamp_dir, base_dir, path_timestamp_dir, path_document_dir
    timestamp_dir = get_timestamp()
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/data/' + timestamp_dir + '/' + 'documents'
    path_document_dir = '/'.join(base_dir.split('/')[:3]) + '/'
    path_timestamp_dir = '/'.join(base_dir.split('/')[:2]) + '/'


def clear_broken_file(name):
    if os.stat(name).st_size < 5:
        os.remove(name)
        raise RuntimeError


def to_json(data):
    pre_data = json.load(open(path_document_dir + 'temp.json', 'r', encoding='utf-8'))
    for key, value in data.items():
        if key == 'BaseUrlParser':
            pre_data[key].update(value)
        else:
            pre_data[key].append(value)
    with open(path_document_dir + 'temp.json', 'w', encoding='utf-8') as f:
        json.dump(pre_data, f, indent=2, ensure_ascii=False)


def debug(name_parser):
    logging.basicConfig(
        handlers=[logging.FileHandler(path_document_dir + name_parser + '.log', 'w', 'utf-8')],
        level=logging.INFO,
        format='%(message)s'
    )


def write_log(message):
    logging.info(message)
