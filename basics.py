#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from os import path
    from time import time
    from platform import system as os_system
    from glob import glob
    from tempfile import gettempdir
    from subprocess import run
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
    import re
except ImportError as e:
    pass
    print('Python package error: ' + str(e).strip('Message: '))
    exit()

class YedortHelper():
    @staticmethod
    def unix_time():
        return int(round(time() * 1000))
    
    @staticmethod
    def regex_match(pattern, string, group=0):
        try:
            return re.search(pattern, string).group(group)
        except:
            pass
            return None

    @staticmethod
    def get_file(filename, split_by_lines=False):
        with open(path.abspath(filename), 'r', encoding='utf-8') as fh:
            file_contents = fh.read()
        if split_by_lines:
            file_contents = file_contents.strip().split('\n')
        return file_contents

    @staticmethod
    def write_file(filename, data, append=False):
        mode = 'a' if append else 'w'
        with open(path.abspath(filename), mode, encoding='utf-8') as fh:
            fh.write(data)

    @staticmethod
    def fetch_url(url):
        try:
            content = urlopen(url).read().decode('utf-8')
            return content
        except (URLError, HTTPError):
            pass
            return None

    @staticmethod
    def delete_temp_files(dir):
        if os_system().lower() == 'windows':
            temp_dirs = glob(gettempdir() + '/' + dir)
            command = ';'.join(['rd /s /q ' + temp_dir for temp_dir in temp_dirs])
            run(command, shell=True)
