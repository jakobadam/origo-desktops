echo 'vagrant' | sudo -S -u www-data `readlink -f manage.py` test $@
