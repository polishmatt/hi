presets = {
    "ssh": {
        "command": "ssh -t",
        "args": "'cd {workdir}; bash -l'",
        "workdir": "$HOME",
    },
    "mysql": {
        "command": "mysql -u{user} -p{password} -P{port} -h",
        "args": "-A",
        "user": "$USER",
        "password": "",
        "port": "3306",
    },
}
