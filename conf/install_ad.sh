#!/usr/bin/env bash

# https://wiki.samba.org/index.php/Samba_AD_DC_HOWTO

error() {
    local msg="${1}"
    echo "==> ${msg}"
    exit 1
}

if [ "$(id -u)" != "0" ]; then
    error "ERROR! You must execute the script as the 'root' user."
fi

apt-get --yes install samba 
#apt-get --yes install samba-tools samba4-common-bin


#service samba stop
service smbd stop
service nmbd stop

rm /etc/samba/smb.conf

samba-tool domain provision \
    --domain=example.com \
    --realm=dc.example.com \
    --adminpass=V@grant

# A Kerberos configuration suitable for Samba 4 has been generated at /var/lib/samba/private/krb5.conf

# Setup DNS
IP=$(ifconfig eth0 | grep 'inet addr' | cut -d":" -f2 | cut -d" " -f1)

sed -i "s/nameserver.*/nameserver ${IP}/" /etc/resolv.conf
echo 'domain dc.example.com' >> /etc/resolv.conf

# deny updates to it
chattr +i /etc/resolv.conf

# run manually, TODO: service
samba

check_ad.sh
# kerberos

# /var/lib/samba

# ; TSIG error with server: tsig verify failure
# Point DNS on the windows server on this one
