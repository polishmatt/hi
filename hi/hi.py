import yaml
import os
import sys
import subprocess
import signal

CONFIG_DIR = os.path.join(os.environ.get('HOME', ''), '.hi')

def load_hosts():
    hosts = []
    try:
        with open(os.path.join(CONFIG_DIR, 'hosts')) as file:
            hosts = yaml.load(file.read())
    except IOError:
        pass
    return hosts

def load_groups():
    groups = {}
    try:
        with open(os.path.join(CONFIG_DIR, 'groups')) as file:
            groups = yaml.load(file.read())
    except IOError:
        pass
    return groups

def run(argv, hosts, groups):
    rules = {
        'prod': lambda host: 'stg' not in host and 'dev' not in host
    }
    rules['prd'] = rules['prod']

    for index, arg in enumerate(argv):
        # Pad 1-digit searches to avoid matching multiple digit numbers
        # 1 should match 01 but not 10
        if len(arg) == 1:
            try:
                int(arg)
                argv[index] = '0' + arg
            except ValueError:
                pass

    if len(argv) == 0:
        matches = hosts
    else:
        matches = []
        for host_config in hosts:
            host = host_config['host']
            if 'cron' in host and 'cron' not in argv:
                match = False
            else:
                match = True
                for arg in argv:
                    if arg in rules:
                        match = rules[arg](host)
                    elif arg not in host:
                        match = False
                    if not match:
                        break
            if match:
                matches.append(host_config)

    if len(matches) == 1:
        match = matches[0]
        command = match['command'] + ' ' + match['host']
        child = subprocess.Popen(command.split(' '))
        try:
            child.communicate()
        except KeyboardInterrupt:
            child.send_signal(signal.SIGINT)
        return child.returncode
    else:
        for match in matches:
            print(match['host'])
        return 0

