#!/usr/bin/env python

import os
import sys
from os import listdir, path
from os.path import isfile, join
from os import system
from getpass import getuser
from datetime import datetime


now = datetime.now()
current_time = now.strftime('%H:%M:%S')
current_folder = os.path.abspath(os.getcwd())
user = getuser()
install_folder = '/Users/{0}/Library/Application Support/iTerm2/Scripts/AutoLaunch/'.format(user)
home = '/Users/' + user + '/'
segment_folder = '{0}{1}'.format(current_folder, '/segments')

onlyfiles = [f for f in listdir(segment_folder) if isfile(join(segment_folder, f))]

arrow = '====>'


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Log(Colors):
    user = getuser()

    def now(self):
        time = datetime.now()
        return time.strftime('%H:%M:%S')

    def buildLogString(self, kind, color):
        start = '{2} {0} ' + color + '{1}:' + kind + ' ' + self.ENDC
        attach = self.HEADER + ': {3}' + self.ENDC
        return start + attach

    def Success(self, string):
        st = self.buildLogString('SUCCESS', self.OKGREEN)
        print(st.format(self.now(), self.user, arrow, string))

    def Warning(self, string):
        st = self.buildLogString('WARNING', self.WARNING)
        print(st.format(self.now(), self.user, arrow, string))

    def Error(self, string):
        st = self.buildLogString('ERROR', self.FAIL)
        print(st.format(self.now(), self.user, arrow, string))

    def Critical(self, string):
        st = self.buildLogString('CRITICAL', self.FAIL)
        print(st.format(self.now(), self.user, arrow, string))

    def Info(self, string):
        st = self.buildLogString('INFO', self.OKBLUE)
        print(st.format(self.now(), self.user, arrow, string))


log = Log()


def Copy(source, dest):
    try:
        log.Info('Copy File {0}'.format(source))
        system('cp {0}/{1} {2}'.format(segment_folder, source, dest))
        log.Success('Success Copy File')
    except:
        log.Error('Failed to move file')


def Main():
    log.Info('Start Installation')
    if path.exists(install_folder):
        for file in onlyfiles:
            Copy(file, install_folder)
        log.Success('Finish Installation')
        log.Critical('If you like it pls leave a star on the repo :) https://github.com/danielnehrig/iTerm2segments')
        sys.exit(0)
    else:
        log.Error('{0} does not exist'.format(install_folder))
        log.Info('Creating Folder')
        os.makedirs(install_folder)
        for file in onlyfiles:
            Copy(file, install_folder)
        log.Success('Finish Installation')
        log.Critical('If you like it pls leave a star on the repo :) https://github.com/danielnehrig/iTerm2segments')
        sys.exit(0)


def Help():
    for option in sys.argv:
        if option == '--help' or option == '-h':
            print('./install.py')
            sys.exit(0)


if __name__ == '__main__':
    Help()
    if sys.platform == 'darwin':
        Main()
    else:
        log.Critical('Only Mac is Supported')
        sys.exit(1)
