#!/usr/bin/env sh

# NOTE: When run with vagrant this script is present in /tmp
rsync -avp /vagrant/conf/etc/ /etc/

mkdir -p /srv/www
ln -s /vagrant /srv/www/rds

apt-get update
apt-get --yes install python-pip samba nginx sqlite3 git ipython rabbitmq-server

# NOTE: We don't need this in production just the files
# bower
apt-get --yes install nodejs nodejs-legacy npm

npm install -g bower

# setup django
pip install -r /vagrant/conf/requirements.txt
pip install django gunicorn django-crispy-forms django-bower

/vagrant/manage.py syncdb --noinput
su vagrant -c 'yes n | /vagrant/manage.py bower install'
/vagrant/manage.py collectstatic --noinput

# setup webserver
mkdir /var/run/gunicorn
chown www-data: /var/run/gunicorn
rm /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
ln -s /etc/nginx/sites-available/rds /etc/nginx/sites-enabled/rds

# setup samba
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

service nmbd restart
service smbd restart

# winexe
ln -s /home/vagrant/src/winexe/bin/winexe /usr/local/bin

# start gunicorn on startup
update-rc.d gunicorn defaults
update-rc.d gunicorn enable

service gunicorn start
service nginx restart
