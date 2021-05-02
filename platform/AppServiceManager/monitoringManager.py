#!/usr/bin/env python3

import subprocess
from _thread import *
import time
import sys

components = ['deployment', 'logger', 'node_manager', 'comm_module',
              'scheduler', 'appManager', 'sensor_services', 'sensor_manager']

bash_restart_files = [
    'ENTER THE BASH SCRIPT NAMES FOR INDIVIDUAL COMPONENTS HERE']


def startMonitor():
    osType = 0
    if sys.platform.startswith('linux'):
        osType = 0
    elif sys.platform.startswith('darwin'):
        osType = 1
    elif sys.platform.startswith('win32'):
        osType = 2
    i = 0
    while True:
        cmd = [f'pgrep -f .*python.*{components[i]}.py']
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        my_pid, err = process.communicate()

        if len(my_pid.splitlines()) > 0:
            print('Service', components[i].upper(), 'running normally')
        else:
            print('ERROR! Service', components[i].upper(
            ), 'is not running. Attempting to resume...')
            # https://stackoverflow.com/questions/19308415/execute-terminal-command-from-python-in-new-terminal-window
            if osType == 0:
                subprocess.call(
                    ['gnome-terminal', '-x', f'{bash_restart_files[i]}'])
            elif osType == 1:
                subprocess.call(
                    ['open', '-W', '-a', 'Terminal.app', 'bash', '--args', bash_restart_files[i]])
            elif osType == 2:
                subprocess.call(
                    f'start /wait bash {bash_restart_files[i]}', shell=True)
            else:
                print('Unknown OS. Failed to restart service')
        i += 1
        if i >= len(components):
            i = 0
        time.sleep(10)


if __name__ == '__main__':
    start_new_thread(startMonitor, ())
    input('Hit ENTER to quit')
