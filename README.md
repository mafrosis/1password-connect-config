1Password Connect
==========

A basic setup for 1password Connect following https://developer.1password.com/docs/connect/.


Authentication
----------

Using the v2 version of the `op` CLI tool, create a "server" and a token, which belongs to the
server. The "server" is any name which represents this particular Connect instance.

```
> op connect server create ringil
Set up a Connect server.
UUID: EZVRIQAW65C5BDGE5ZW3JZNTJU
Credentials file: /media/mnt/dev/1password-connect/1password-credentials.json
```

The `1password-credentials.json` file contains the credentials the connect services `api` & `sync`
use to authenticate with the 1password servers upstream.

Grant this connect server access to your vault:
```
> op connect vault grant --server ringil --vault Homelab
Connect server ringil (EZVRIQAW65C5BDGE5ZW3JZNTJU) has been successfully granted access to vault Homelab (b6hmle4xxxxxxxxxxxxx4lcwza).
```

The following command creates a token which a client application can use to auth to the `api`
service:
```
> op connect token create "$(hostname)-connect" --server ringil --vault Homelab
eyJhbGciOiJFUzI1...snip
```

You can visit the [integrations page](https://my.1password.com/integrations/active) to view your
new server and its token.

The containers run with user `opuser` which has `uid=999`. Update the `1password-credentials.json`
file to be readable inside the docker containers:

```
chgrp 999 1password-credentials.json
chmod g+r 1password-credentials.json
```


Running Connect
----------

1Password Connect requires two containers:

- `1password/connect-sync`: keeps secrets sync'd with 1Password.com
- `1password/connect-api`: serves the Connect REST API


Updating
----------

New docker tags can be checked at https://hub.docker.com/r/1password/connect-api/tags.

```
docker compose pull
docker compose up -d
```


Using as a Saltstack external pillar
----------

Users of Saltstack can leverage the
[external pillar](https://docs.saltproject.io/en/latest/topics/development/modules/external_pillars.html)
found at [`salt/ext_pillar/1password_connect.py`](./salt/ext_pillar/1password_connect.py), to feed
all secrets from a given vault into the Salt pillar data.


### Salt-master config

The `cdalvaro/docker-salt-master` docker image includes following config:
```
# The master will automatically include all config files from:
default_include: /home/salt/data/config/*.conf

# Directory for custom modules. This directory can contain subdirectories for
# each of Salt's module types such as "runners", "output", "wheel", "modules",
# "states", "returners", "engines", "utils", etc.
extension_modules: /var/cache/salt/master/extmods
```

Add following into `config/ext_pillar.conf`:
```
ext_pillar:
  - 1password:
      connect_host: http://example.com:8081
      connect_token: eyJhbGc .. snip .. 2YCkucw
      vault_id: b6hmle4xxxxxxxxxxxxy4lcwza
```

The bundled `docker-compose.yml` includes the following:
```
- ./config:/home/salt/data/config
- ./1password-connect/salt:/var/cache/salt/master/extmods
```
