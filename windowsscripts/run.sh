USER='vagrant'
PASSWORD='vagrant'

IP='192.168.123.196'

run(){
    local cmd="${1}"
    echo -e ./winexe -U $USER%$PASSWORD //$IP "'$cmd'"
    ./winexe -U $USER%$PASSWORD //$IP "$cmd"
}

cmd(){
    local cmd="${1}"
    run "cmd.exe /c $cmd"
}

ps(){
    local cmd="${1}"
    run "powershell $cmd"
}

if_main(){
    local scriptname='run.sh'
    [ `basename $0` == $scriptname ]
}

if_main && run "$1"
