#!/usr/bin/env bash

if [ "$(id -u)" != "0" ]; then
    echo "ERROR! You must execute the script as the 'root' user."
    exit 1
fi

# NOTE: When run with vagrant this script is present in /tmp
echo '==> Copying configuration to /etc'
rsync -rlptv /vagrant/conf/etc/ /etc/

mkdir -p /srv/www
ln -s /vagrant /srv/www/rds

echo '==> Installing apt packages'
apt-get update

PACKAGES="
git
ipython
nginx
python-pip
python-dev
rabbitmq-server
samba
sqlite3 
"
apt-get --yes install $PACKAGES 

# NOTE: We don't need this in production just the files
# bower
DEV_PACKAGES="
nodejs 
nodejs-legacy
npm
"
apt-get --yes install $DEV_PACKAGES 

npm install -g bower

echo '==> Installing Webserver'
mkdir /var/run/gunicorn
chown www-data: /var/run/gunicorn
rm /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
ln -s /etc/nginx/sites-available/rds /etc/nginx/sites-enabled/rds

echo '==> Installing Webapp'
pip install -r /vagrant/conf/requirements.txt

/vagrant/manage.py syncdb --noinput
su vagrant -c 'yes n | /vagrant/manage.py bower install'
/vagrant/manage.py collectstatic --noinput

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

echo '==> Enable Celery Service'
useradd celery
update-rc.d celeryd defaults 
update-rc.d celeryd enable
 
echo '==> Enable Gunicorn Service'
update-rc.d gunicorn defaults
update-rc.d gunicorn enable

echo '==> Restarting services'
service nmbd restart
service smbd restart
service nginx restart
service gunicorn restart
service celeryd restart
