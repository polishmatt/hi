# hi

[![Build Status](https://travis-ci.org/polishmatt/hi.svg?branch=master)](https://travis-ci.org/polishmatt/hi)

A generic CLI for connecting humans to host interfaces.

Why remember or write an alias for

```
mysql -hmaster-service-db.example.com -ume -p -A
ssh -t api.example.com 'cd /logs; bash -l'
```

when you can type

```
hi master db
hi api
```

* [Getting started](#getting-started)
* [Advanced configuration](#advanced-configuration)

## Why should I use this?

* You find yourself frequently interacting with a relatively small set of static hosts.

## Why shouldn't I use this?

* You want to interact with auto-scaling or otherwise frequently changing hosts.
  Use existing solutions for centralizing your data (like [logstash](https://github.com/elastic/logstash)) and incident management across multiple hosts at once.

## Getting started

This project is available on PyPI.

```
pip install hicli
```

By default the hi CLI looks for configuration files at `$HOME/.hi`. Edit `$HOME/.hi/hosts` to add hosts using the [YAML](http://yaml.org) format.

```
- host: api.example.com
  command: ssh
```

## Advanced configuration

### Groups

Hosts may be assigned to groups which run the same command. By default the hi CLI looks for group configuration at `$HOME/.hi/groups`.

```
mysql:
  command: mysql -ume -p -A -h
```

And in the hosts file:

```
- host: master-db.example.com
  group: mysql
- host: slave-db.example.com
  group: mysql
```

### Complex commands

To add on to the end of the command being run, use the args property in your hosts or groups config.

```
- host: api.example.com
  command: ssh -t 
  args: '''cd /logs; bash -l'''
```

