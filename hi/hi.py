import os
import sys
import subprocess
import signal

CONFIG_DIR = os.path.join(os.environ.get('HOME', ''), '.hi')

def log(message):
    print(message)

def load_hosts(file=None):
    hosts = []
    if file is None:
        file = os.path.join(CONFIG_DIR, 'hosts')
    try:
        with open(file) as file:
            import yaml
            hosts = yaml.load(file.read())
    except IOError:
        pass
    return hosts

def load_groups(file=None):
    groups = {}
    if file is None:
        file = os.path.join(CONFIG_DIR, 'groups')
    try:
        with open(file) as file:
            import yaml
            groups = yaml.load(file.read())
    except IOError:
        pass
    return groups

def run(argv, hosts, groups, run=True, rules=True):
    argv = list(argv)

    if rules:
        arg_rules = {
            'prod': lambda host: 'stg' not in host and 'dev' not in host and '.' in host,
        }
        arg_rules['prd'] = arg_rules['prod']

        # Pad 1-digit searches to avoid matching multiple digit numbers
        # 1 should match 01 but not 10
        def generate_digit_rule(digit):
            return lambda host: '0' + digit in host
        for digit in range(1, 10):
            arg_rules[str(digit)] = generate_digit_rule(str(digit))

        host_rules = {
            'cron': lambda argv: next((arg for arg in argv if 'cron' in arg), None) is not None,
            'db': lambda argv: next((arg for arg in argv if 'db' in arg), None) is not None,
        }
    else:
        arg_rules = {}
        host_rules = {}

    if len(argv) == 0:
        matches = hosts
    else:
        matches = []
        for host_config in hosts:
            host = host_config['host']
            if len(argv) == 1 and host == argv[0]:
                matches = [host_config]
                break

            for rule_pattern, rule in host_rules.items():
                if rule_pattern in host and not rule(argv):
                    match = False
                    break
            else:
                match = True

                for arg in argv:
                    if arg in arg_rules:
                        match = arg_rules[arg](host)
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
            log(command)
    else:
        for match in matches:
            log(match['host'])

    return 0

