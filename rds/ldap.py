#!/usr/bin/env python
import logging
import subprocess

log = logging.getLogger(__name__)

class LdapException(Exception):
    pass

def find_user(host, domain, user, auth=None):
    # dc=example,dc=com
    searchbase = ','.join(['dc={}'.format(d) for d in domain.split('.')])
    filter = "(sAMAccountName={})".format(user)
    return search(host, searchbase, filter, auth=auth, attrs='sAMAccountName')

def search(host, searchbase, filter, auth=None, attrs=""):
    command = (
        '/usr/bin/ldapsearch',
        '-h', host,
        '-D', auth[0],
        '-w', auth[1],
        '-b', searchbase,
        filter,
        attrs
        )
    try:
        log.info(' '.join(command))
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        return output
    except subprocess.CalledProcessError,e:
        raise LdapException(e.output)

def main():
    print find_user('192.168.123.158', 'example.com', 'Administrator', auth=('vagrant', 'V@grant'))

if __name__ == '__main__':
    main()

#ldapsearch -h srvdc22.adm.aarhuskommune.dk -D "adm\admincabojd" -W -b "dc=adm,dc=aarhuskommune,dc=dk" "(sAMAccountName=admincabojd)"

# no success with the python ldap libs:(

# import ldap3

# s = ldap3.Server('srvdc22.adm.aarhuskommune.dk')
# c = ldap3.Connection(s, user='adm\admincabojd', password='...', auto_bind=True)
# c.search(
#     search_base='dc=adm,dc=aarhuskommune,dc=dk',
#     search_filter='(sAMAccountName=admincabo)'
#     )

# print c.response

# import ldap
# l = ldap.initialize('ldap://srvdc22.adm.aarhuskommune.dk')
# # username = "uid=%s,ou=People,dc=mydotcom,dc=com" % username
# # password = "my password"
# username = 'adm\admincabojd'
# password = '...'

# try:
#     l.protocol_version = ldap.VERSION3
#     l.simple_bind_s(username, password)
#     valid = True
# except Exception, error:
#     print error
