#!/usr/bin/env bash

NAME=_ldap._tcp.dc.example.com. 
host -t SRV $NAME

NAME=_kerberos._udp.dc.example.com.
host -t SRV $NAME

NAME=$(hostname).dc.example.com.
host -t A $NAME

# When Windows tries to join computer to domain it fails
# it can't lookup the following
NAME=_ldap._tcp.dc._msdcs.example.com
host -t SRV $NAME

# The reason being this command failing:
samba_dnsupdate --verbose --all-names

# ; TSIG error with server: tsig verify failure
