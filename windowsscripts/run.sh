[ "$USER" ]     || USER='vagrant'
[ "$PASSWORD" ] || PASSWORD='vagrant'
[ "$IP" ]       || IP='192.168.123.196'

usage() {
    echo "Usage: ${0} "
    echo
    echo "Available commands are:"
    echo -e "\tcmd\trun command with cmd.exe /c"
    echo -e "\tps\trun command as powershell"
    echo -e "\trun\trun command"
    echo
}

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

main(){

    echo "Main: ${1}"
    [ "$2" ] || usage || exit 1

    local scriptname='run.sh'
    local cmd_type="$1"
    local cmd_arg="$2"

    [ `basename $0` == $scriptname ] || return 1

    echo "$cmd_type"
    case "$cmd_type" in
        run)
            run $cmd_arg
            ;;
        cmd)
            cmd $cmd_arg
            ;;
        ps)
            ps $cmd_arg
            ;;
        *)
            usage
            exit 1
            ;;
    esac

    # OPTSTRING=h
    # while getopts ${OPTSTRING} OPT
    # do
    #     case ${OPT} in
    #         h) usage;;
    #     esac
    # done
}

main $*
