import subprocess
import signal

from . import exceptions


class Host:
    def __init__(self, config):
        self.config = config

    def __repr__(self):
        return self.config["host"]

    def __str__(self):
        if "args" in self.config and self.config.get("alias", False):
            raise exceptions.InvalidConfigException(
                "'args' property is not allowed for alias '%s'" % (repr(self))
            )

        command = self.config["command"]

        if not self.config.get("alias", False):
            command += " {host}"

        if "args" in self.config and len(self.config["args"]) > 0:
            command += " " + self.config["args"]

        for variable, value in self.config.items():
            command = command.replace("{" + str(variable) + "}", str(value))

        return command

    def is_match(self, argv, arg_rules, host_rules):
        host = self.config["host"]

        for rule_pattern, rule in host_rules.items():
            if rule_pattern in host and not rule(argv):
                return False

        for arg in argv:
            if arg in arg_rules:
                match = arg_rules[arg](host)
            else:
                match = arg in host

            if not match:
                return False

        return True

    def collapse_groups(self, groups):
        group = self.config
        visited = {}
        while group is not None:
            if "group" in group:
                group_name = group["group"]

                if group_name not in groups:
                    raise exceptions.InvalidConfigException(
                        "Undefined group '%s'" % (group_name)
                    )
                elif group["group"] in visited:
                    raise exceptions.InvalidConfigException(
                        "Circular group reference for host '%s'" % (repr(self))
                    )
                else:
                    visited[group_name] = True
                    group = groups[group_name]

                    for key, value in group.items():
                        if key not in self.config:
                            self.config[key] = value
            else:
                group = None

    def run(self):
        child = subprocess.Popen(str(self), shell=True)
        try:
            child.communicate()
        except KeyboardInterrupt:
            child.send_signal(signal.SIGINT)
        return child.returncode
