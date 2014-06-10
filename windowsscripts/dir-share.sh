# List contents of samba share
. ./run.sh


SHARE='\\ubuntu\share'

run "cmd.exe /c dir $SHARE"
