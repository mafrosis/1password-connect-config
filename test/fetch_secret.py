#! /usr/bin/env python3

import os

from onepasswordconnectsdk.client import new_client

CONNECT_HOST='http://ringil:8081'
VAULT_ID='b6hmle4wvz2gl4mv6j3y4lcwza'

def main():
    connect_token = os.environ.get('OP_CONNECT_TOKEN')
    if not connect_token:
        raise Exception('Must export OP_CONNECT_TOKEN')

    client = new_client(url=CONNECT_HOST, token=connect_token)

    data = {}

    for item in client.get_items(VAULT_ID):
        item = client.get_item(item.id, item.vault.id)

        title = item.title.lower().replace('.', '_').replace(' ', '_')
        password = next(iter([x.value for x in item.fields if x.id == 'password']))

        data[title] = password

    print(data)


if __name__ == '__main__':
    main()
