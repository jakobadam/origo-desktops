USER='vagrant'
PASSWORD='vagrant'

IP='192.168.123.196'

run(){
    local cmd="${1}"
    echo ./winexe -U $USER%$PASSWORD //$IP "$cmd"
    ./winexe -U $USER%$PASSWORD //$IP "$cmd"
}

if_main(){
    local scriptname='run.sh'
    [ `basename $0` == $scriptname ]
}

if_main && run "$1"
