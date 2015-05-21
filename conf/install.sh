#!/usr/bin/env bash
#
# Install the Origo Desktop Controller on an empty Ubuntu Server

if [ "$(id -u)" != "0" ]; then
    echo "ERROR! You must execute the script as the 'root' user."
    exit 1
fi

# NOTE: When run with vagrant this script is present in /tmp
echo '==> Copying configuration to /etc'
rsync -rlptv /vagrant/conf/etc/ /etc/
chmod 640 /etc/default/celeryd

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
ldap-utils
"
apt-get --yes install $PACKAGES

# NOTE: We don't need nodejs in production just the static files
# bower
DEV_PACKAGES="
nodejs
nodejs-legacy
npm
"
apt-get --yes install $DEV_PACKAGES

# Failed to execute "git ls-remote --tags --heads git://github.com/designmodo/Flat-UI.git", exit code of #128
git config --global url."https://".insteadOf git://
npm install -g bower

echo '==> Installing Webserver'
rm /etc/nginx/sites-enabled/default /etc/nginx/sites-available/default
ln -s /etc/nginx/sites-available/rds /etc/nginx/sites-enabled/rds

echo '==> Installing Webapp'
pip install -r /vagrant/conf/requirements.txt --src=$HOME

/vagrant/manage.py syncdb --noinput
su $SUDO_USER -c 'yes n | /vagrant/manage.py bower install'
/vagrant/manage.py collectstatic --noinput

echo '==> Installing Samba'
mkdir /srv/samba
chown -R www-data: /srv/samba

cat >> /etc/samba/smb.conf <<EOF
[share]
    comment = Software
    writable = yes
    path = /srv/samba
    browsable = yes
    guest ok = yes
    read only = no
    create mask = 0755

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
# Celery init script uses su => www-data must be able to login
# replace nologin
usermod -s '' www-data
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
