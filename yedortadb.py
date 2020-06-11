#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from platform import system as os_system
    from time import sleep
    from subprocess import run
except ImportError as e:
    pass
    print('Python package error: ' + str(e).strip('Message: '))
    exit()

class YedortADB():
    def __init__(self, adb):
        self.adb = adb if os_system().lower() == 'windows' else 'adb'
        run(self.adb + ' devices -l', shell=True)

    def reset_ip(self):
        new_public_ip = public_ip = fetch_url('https://bot.whatismyipaddress.com')
        while new_public_ip is None or new_public_ip == public_ip:
            run(self.adb + ' shell su -c \'settings put global airplane_mode_on 1\'', shell=True)
            run(self.adb + ' shell su -c \'am broadcast -a android.intent.action.AIRPLANE_MODE\'', shell=True)
            sleep(3)
            run(self.adb + ' shell su -c \'settings put global airplane_mode_on 0\'', shell=True)
            run(self.adb + ' shell su -c \'am broadcast -a android.intent.action.AIRPLANE_MODE\'', shell=True)
            sleep(3)
            new_public_ip = fetch_url('https://bot.whatismyipaddress.com')

    def quit(self):
        try:
            run(self.adb + ' kill-server', shell=True)
        except:
            pass
