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

def run(argv, hosts, groups, run=True):
    argv = list(argv)
    rules = {
        'prod': lambda host: 'stg' not in host and 'dev' not in host and '.' in host
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
            if len(argv) == 1 and host == argv[0]:
                matches = [host_config]
                break
            elif 'cron' in host and next((arg for arg in argv if 'cron' in arg), None) is None:
                match = False
            elif 'db' in host and next((arg for arg in argv if 'db' in arg), None) is None:
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

        if 'group' in match and match['group'] in groups:
            group = groups[match['group']]
            
            for key, value in group.items():
                if key not in match:
                    match[key] = value

        command = match['command'] + ' ' + match['host']
        if 'args' in match:
            command += ' ' + match['args']

        if run:
            child = subprocess.Popen(command, shell=True)
            try:
                child.communicate()
            except KeyboardInterrupt:
                child.send_signal(signal.SIGINT)
            return child.returncode
        else:
            print(command)
    else:
        for match in matches:
            print(match['host'])

    return 0

