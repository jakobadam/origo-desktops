# Run the dev server under www-data, so upload works.
echo 'vagrant' | sudo -S -u www-data `readlink -f manage.py` runserver 0.0.0.0:8000
