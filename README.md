# One-Click RDP Services

## Quick Start

```
$ vagrant up ubuntu
```

Point browser to http://host:8000

## Winexe

There is a winexe wrapper available in the bin directory

I recommend putting this somewhere in your path:

```
ln -s PATH/wexe.py /usr/local/bin/wexe.py
```

Now you can run winexe command like this:
```
wexe.py -u vagrant -p vagrant -i 192.168.123.191 file whoami.bat
```


**Note:** I've had no luck accessing a share through winexe mounted
  with:
```
net use b: \\ubuntu\share
```
Instead I specify the fully qualified path.
