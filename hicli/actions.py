import os
import sys
import importlib
import yaml

from .rules import DEFAULT_ARG_RULES, DEFAULT_HOST_RULES
from .group import presets
from .host import Host
from .log import logger
from . import exceptions

CONFIG_DIR = os.path.join(os.environ.get("HOME", ""), ".hi")


def load_hosts(file=None):
    hosts = []
    if file is None:
        file = os.path.join(CONFIG_DIR, "hosts")
    try:
        with open(file) as file:
            hosts = yaml.safe_load(file.read())
    except IOError:
        pass
    return hosts


def load_groups(file=None):
    groups = {}
    if file is None:
        file = os.path.join(CONFIG_DIR, "groups")
    try:
        with open(file) as file:
            groups = yaml.safe_load(file.read())
    except IOError:
        pass
    return groups


def load_rule(rule):
    last = rule.rfind(".")
    package = rule[:last]
    rule = rule[last + 1 :]

    try:
        module = importlib.import_module(package)
    except ImportError:
        if package[:3] == "hi.":
            package = package[3:]
            module = importlib.import_module(package)

    return (rule, getattr(module, rule))


def load_rules(rules, arg_rule, host_rule):
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

    return (arg_rules, host_rules)


def run(argv, hosts, groups, run=True, rules=True, arg_rule=(), host_rule=()):
    argv = list(argv)
    (arg_rules, host_rules) = load_rules(rules, arg_rule, host_rule)

    preset_groups = presets.copy()
    preset_groups.update(groups)
    groups = preset_groups

    try:
        if len(argv) == 0:
            matches = [Host(host_config) for host_config in hosts]
        else:
            matches = []
            for host_config in hosts:
                host = Host(host_config)

                if len(argv) == 1 and repr(host) == argv[0]:
                    matches = [host]
                    break

                if host.is_match(argv, arg_rules, host_rules):
                    matches.append(host)

        if len(matches) == 1:
            match = matches[0]
            match.collapse_groups(groups)
            command = str(match)

            if run:
                return match.run()
            else:
                logger.info(command)
        else:
            for match in matches:
                logger.info(repr(match))

        return 0

    except exceptions.HiException as exception:
        logger.error(str(exception))
        return 1
