#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from os.path import abspath
    from time import time
    from platform import system as os_system
    from glob import glob
    from tempfile import gettempdir
    from subprocess import run
    from urllib.request import urlopen
    from urllib.error import URLError, HTTPError
    from argparse import ArgumentParser
    from random import choice as rand_item, randint as rand_int
    import re
except ImportError as e:
    pass
    print('Python package error: ' + str(e).strip('Message: '))
    exit()

class YedortHelpers():
    @staticmethod
    def random(*args):
        if len(args) == 1 and isinstance(args[0], list):
            result = rand_item(args[0])
        elif len(args) == 2 and isinstance(args[0], int) and isinstance(args[1], int) and args[1] > args[0]:
            result = rand_int(args[0], args[1])
        else:
            return None
        return result.strip() if isinstance(result, str) else result

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
        with open(abspath(filename), 'r', encoding='utf-8') as fh:
            file_contents = fh.read()
        if split_by_lines:
            file_contents = file_contents.strip().split('\n')
        return file_contents

    @staticmethod
    def write_file(filename, data, binary=False, append=False):
        mode = 'a' if append else 'w'
        encoding = 'utf-8'
        if binary:
            mode += 'b'
            encoding = None
        with open(abspath(filename), mode, encoding=encoding) as fh:
            fh.write(data)

    @staticmethod
    def remove_from_file(filename, content, line=False):
        with open(abspath(filename), 'r+', encoding='utf-8') as fh:
            file_contents = fh.read()
            separator = '\n' if line else ''
            file_contents_replaced = file_contents.replace(separator + content, '')
            if file_contents == file_contents_replaced:
                file_contents_replaced = file_contents.replace(content + separator, '')
            fh.seek(0)
            fh.write(file_contents_replaced)
            fh.truncate()

    @staticmethod
    def fetch_url(url, decode=True):
        try:
            content = urlopen(url).read()
            if decode:
                content = content.decode('utf-8')
            return content
        except (URLError, HTTPError):
            pass
            return None

    @staticmethod
    def create_arguments(arguments):
        parser = ArgumentParser()
        for argument in arguments:
            action = None if 'options' in argument and argument['options'] else 'store_true'
            parser.add_argument('-' + argument['name_short'], '--' + argument['name'], action=action)
        options = parser.parse_args()
        input_appeared = False
        for argument in arguments:
            if 'options' in argument and argument['options']:
                chosen_option = getattr(options, argument['name'])
                while (argument['options'] != 'number' and not chosen_option in argument['options']) or (argument['options'] == 'number' and (chosen_option is None or not chosen_option.isdigit() or chosen_option == '0')):
                    if input_appeared:
                        print('___\n')
                    if argument['options'] == 'number':
                        chosen_option = input('Set a number for the ' + argument['name'] + ' option: ')
                    else:
                        print('Available options:')
                        i = 1
                        for option in argument['options']:
                            print('[' + str(i) + '] ' + option)
                            i += 1
                        chosen_option = input('Choose an available ' + argument['name'] + ' option: ')
                        if chosen_option.isdigit() and int(chosen_option) <= len(argument['options']):
                            chosen_option = argument['options'][int(chosen_option) - 1]
                    setattr(options, argument['name'], chosen_option)
                    input_appeared = True
        return options

    @staticmethod
    def delete_temp_files(dir):
        if os_system().lower() == 'windows':
            temp_dirs = glob(gettempdir() + '/' + dir)
            command = ';'.join(['rd /s /q ' + temp_dir for temp_dir in temp_dirs])
            run(command, shell=True)
