import yaml
import os
import sys

hosts = None
with open(os.path.join(os.environ.get('HOME', ''), '.hihosts')) as file:
    hosts = file.read()
hosts = yaml.load(hosts)

rules = {
    'prod': lambda host: 'stg' not in host and 'dev' not in host
}
rules['prd'] = rules['prod']

argv = sys.argv[1:]

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
    print(command)
else:
    for match in matches:
        print(match['host'])

