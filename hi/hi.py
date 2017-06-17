from __future__ import absolute_import
import os
import sys
import subprocess
import signal
import importlib

from .rules import DEFAULT_ARG_RULES, DEFAULT_HOST_RULES

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

def load_rule(rule):
    last = rule.rfind('.')
    package = rule[:last]
    rule = rule[last + 1:]

    try:
        module = importlib.import_module(package)
    except ImportError:
        if package[:3] == 'hi.':
            package = package[3:]
            module = importlib.import_module(package)

    return (rule, getattr(module, rule))


def run(argv, hosts, groups, run=True, rules=True, arg_rule=(), host_rule=()):
    argv = list(argv)

    if rules:
        arg_rules = DEFAULT_ARG_RULES.copy()
        host_rules = DEFAULT_HOST_RULES.copy()
    else:
        arg_rules = {}
        host_rules = {}
    for rule in arg_rule:
        (rule_pattern, rule_match) = load_rule(rule)
        arg_rules[rule_pattern] = rule_match
    for rule in host_rule:
        (rule_pattern, rule_match) = load_rule(rule)
        host_rules[rule_pattern] = rule_match

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

