from datetime import datetime

def set_timestamp():
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    with open('parsers/parser_engine/keep_time.txt', 'w') as file:
        file.write(timestamp)
    return timestamp