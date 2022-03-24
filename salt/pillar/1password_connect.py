'''
Read secrets from a local 1Password Connect

Configuring the 1Password ext_pillar
===========

.. code-block:: yaml

  ext_pillar:
  - 1password:
      connect_host: http://example.com:8081
      connect_token: eyJhbGc .. snip .. 2YCkucw
      vault_id: b6hmle4xxxxxxxxxxxxy4lcwza
'''
import logging


log = logging.getLogger(__name__)


try:
    from onepasswordconnectsdk.client import new_client

    HAS_1PASS = True
except ImportError:
    HAS_1PASS = False


def __virtual__():
    if not HAS_1PASS:
        return False
    return '1password'


def ext_pillar(minion_id, pillar, connect_host='http://localhost:8081', connect_token='', vault_id=''):
    '''
    Query 1Password and feed the secret value into the pillar
    '''
    log.debug('Connecting to 1password external pillar at %s', connect_host)
    log.debug(__grains__)

    client = new_client(url=connect_host, token=connect_token)

    data = {}

    for item in client.get_items(vault_id):
        item = client.get_item(item.id, item.vault.id)

        title = item.title.lower().replace('.', '_').replace(' ', '_')
        password = next(iter([x.value for x in item.fields if x.id == 'password']))

        data[title] = password

    return data
