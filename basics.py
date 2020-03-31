#!/usr/bin/python3
# -*- coding: utf-8 -*-

try:
    from os import path
    from time import time
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
    import re, random
except ImportError as e:
    pass
    print('Python package error: ' + str(e).strip('Message: '))
    exit()

def unix_time():
    return int(round(time() * 1000))
            
def regex_match(pattern, string, group=0):
    try:
        return re.search(pattern, string).group(group)
    except:
        pass
        return None

def get_file(filename, split_by_lines=False):
    with open(path.abspath(filename), 'r', encoding='utf-8') as fh:
        file_contents = fh.read()
    if split_by_lines:
        file_contents = file_contents.strip().split('\n')
    return file_contents

def write_file(filename, data, append=False):
    mode = 'a' if append else 'w'
    with open(path.abspath(filename), mode, encoding='utf-8') as fh:
        fh.write(data)

def fetch_url(url):
    try:
        content = urlopen(url).read().decode('utf-8')
        return content
    except (URLError, HTTPError):
        pass
        return None
