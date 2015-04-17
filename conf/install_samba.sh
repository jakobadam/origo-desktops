echo '==> Installing Samba'
mkdir /srv/samba
chown -R www-data: /srv/samba

# FIXME: duing developement I want to be able to quick switch to the django dev server
cat >> /etc/samba/smb.conf <<EOF
[share]
    comment = Software
    writable = yes
    path = /srv/samba
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0755

[source]
    comment = Source
    writable = yes
    path = /vagrant
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0777

[scripts]
    comment = Scripts
    writable = yes
    path = /srv/www/rds/scripts
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0777
EOF
