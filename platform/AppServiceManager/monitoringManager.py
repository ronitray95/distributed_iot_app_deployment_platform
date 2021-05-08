#!/usr/bin/env python3

import subprocess
from _thread import *
import time
import sys

components = ['appService', 'logger', 'node_manager','scheduler', 'appManager', 'sensor_services', 'init']

bash_restart_files = ['startDeployer.sh', 'startLogger.sh', 'startNM.sh','start.sh', 'start.sh', 'startService.sh', 'startINIT.sh']

folder_names = ['/AppServiceManager/', '/AppServiceManager/', '/AppServiceManager/', '/scheduler/', '/AppManager/', '/SensorManager/', '/SensorManager/']

ignored_components = []

def startMonitor():
    basePath = sys.path[0][:sys.path[0].rindex('/')]
    print(basePath)
    osType = 0
    if sys.platform.startswith('linux'):
        osType = 0
    elif sys.platform.startswith('darwin'):
        osType = 1
    elif sys.platform.startswith('win32'):
        osType = 2
    i = 0
    while True:
        result = subprocess.run(
            ['pgrep', '-f', '.*python.*'+components[i]+'.py'], stdout=subprocess.PIPE)
        x = result.stdout.decode('utf-8')
        x = x.strip()
        cmd = [f'pgrep -f .*python.*{components[i]}.py']
        process = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        my_pid, err = process.communicate()

        if components[i] in ignored_components:
            continue

        if len(x) != 0:  # len(my_pid.splitlines()) > 0:
            print('Service', components[i].upper(), 'running normally')
        else:
            print('ERROR! Service', components[i].upper(
            ), 'is not running. Attempting to resume...')
            # https://stackoverflow.com/questions/19308415/execute-terminal-command-from-python-in-new-terminal-window
            if osType == 0:
                subprocess.call(
                    ['gnome-terminal', '-x', '.' + basePath + folder_names[i] + bash_restart_files[i]])
            elif osType == 1:
                subprocess.call(
                    ['open', '-W', '-a', 'Terminal.app', 'bash', '--args', bash_restart_files[i]])
            elif osType == 2:
                subprocess.call('start /wait bash ' +
                                bash_restart_files[i], shell=True)
            else:
                print('Unknown OS. Failed to restart service')
        i += 1
        if i >= len(components):
            i = 0
        time.sleep(10)


if __name__ == '__main__':
    start_new_thread(startMonitor, ())
    input('MONITORING MANAGER is running. Hit ENTER to quit\n')
