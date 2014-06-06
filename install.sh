#!/usr/bin/env sh
HERE=$(dirname $(readlink -f $0))

apt-get --yes install python-pip samba nginx

# setup django
pip install django gunicorn django-crispy-forms django-bower

# setup webserver
mkdir /var/run/gunicorn
chown www-data: /var/run/gunicorn
rm /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
mkdir -p /srv/www

# setup samba
mkdir -p /srv/samba
chown www-data: /srv/samba

service nmbd restart
service smbd restart

cat >> /etc/samba/smb.conf <<EOF
[share]
    comment = Software
    path = /srv/samba
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0755
EOF

rsync -avp conf/ /
# setup rabbitmq-server
# apt-get --yes install rabbitmq-server
# # # add ghost user / group
# useradd -r ghost -U

# # # install ghost

# curl -L https://ghost.org/zip/ghost-latest.zip -o /tmp/ghost.zip
# unzip -uo /tmp/ghost.zip -d /srv/www/ghost
# cd /srv/www/ghost ; npm install --production

# rsync -av $HERE/conf/ /

# # start ghost service on startup
update-rc.d gunicorn defaults
update-rc.d gunicorn enable

service ghost start
service nginx restart
