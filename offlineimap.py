#!/usr/bin/python

# python helpers for offlineimap:
# - get passwords from gnome-keyring
# - translate Gmail folder names to something sane

try:
    import gnomekeyring as gkey
except ImportError, e:
    pass

try:
    gkey.get_default_keyring_sync()
except:
    import netrc

gmail_mapping = {'INBOX': 'INBOX',
                 '[Gmail]/Drafts': 'Drafts',
                 '[Gmail]/Important': 'Important',
                 '[Gmail]/Sent Mail': 'Sent',
                 '[Gmail]/Spam': 'Spam',
                 '[Gmail]/Starred': 'Starred',
                 '[Gmail]/Trash': 'Trash',
                 '[Gmail]/All Mail': 'All Mail'
                 }

# reverse mapping for local nametrans
gmail_r_mapping = { val: key for key, val in gmail_mapping.items() }

# nametrans functions
def gmail_nt_remote(folder):
    try:
        return gmail_mapping[folder]
    except:
        return folder

def gmail_nt_local(folder):
    try:
        return gmail_r_mapping[folder]
    except:
        return folder

# exclude function for folderfilter
# folderfilter = exclude(['Folder 1', 'Folder 2', ... ])
def exclude(excludes):
    def inner(folder):
        try:
            excludes.index(folder)
            return False
        except:
            return True

    return inner

# fetch info from gnome-keyring
class Keyring(object):
    def __init__(self, name, server, protocol):
        self._name = name
        self._server = server
        self._protocol = protocol
        self._keyring = gkey.get_default_keyring_sync()

    def has_credentials(self):
        try:
            attrs = {"server": self._server, "protocol": self._protocol}
            items = gkey.find_items_sync(gkey.ITEM_NETWORK_PASSWORD, attrs)
            return len(items) > 0
        except gkey.DeniedError:
            return False

    def get_credentials(self):
        attrs = {"server": self._server, "protocol": self._protocol}
        items = gkey.find_items_sync(gkey.ITEM_NETWORK_PASSWORD, attrs)
        return (items[0].attributes["user"], items[0].secret)

    def set_credentials(self, (user, pw)):
        attrs = {
            "user": user,
            "server": self._server,
            "protocol": self._protocol,
            }
        gkey.item_create_sync(gkey.get_default_keyring_sync(),
                              bkey.ITEM_NETWORK_PASSWORD, self._name, attrs, pw, True)

def get_username(server):
    try:
        keyring = Keyring("offlineimap", server, "imap")
        (username, password) = keyring.get_credentials()
    except:
        info = netrc.netrc()
        username, account, password = info.authenticators(server)
    return username

def get_password(server):
    try:
        keyring = Keyring("offlineimap", server, "imap")
        (username, password) = keyring.get_credentials()
    except:
        info = netrc.netrc()
        username, account, password = info.authenticators(server)
    return password
