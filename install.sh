#!/usr/bin/env sh

# NOTE: When run with vagrant this script is present in /tmp
rsync -avp /vagrant/conf/ /

mkdir -p /srv/www
ln -s /vagrant /srv/www/rdps

apt-get --yes install python-pip samba nginx

# setup django
pip install django gunicorn django-crispy-forms django-bower

# setup webserver
mkdir /var/run/gunicorn
chown www-data: /var/run/gunicorn
rm /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
ln -s /etc/nginx/sites-available/rdps /etc/nginx/sites-enabled/rdps

# setup samba
mkdir -p /srv/samba
chown www-data: /srv/samba

service nmbd restart
service smbd restart

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
EOF

# winexe
ln -s /vagrant/windowsscripts/winexe /usr/local/bin


# setup rabbitmq-server
# apt-get --yes install rabbitmq-server
# # # add ghost user / group
# useradd -r ghost -U

# # # install ghost

# curl -L https://ghost.org/zip/ghost-latest.zip -o /tmp/ghost.zip
# unzip -uo /tmp/ghost.zip -d /srv/www/ghost
# cd /srv/www/ghost ; npm install --production



# start gunicorn on startup
update-rc.d gunicorn defaults
update-rc.d gunicorn enable

service gunicorn start
service nginx restart
