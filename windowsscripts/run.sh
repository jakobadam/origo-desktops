[ "$USER" ]     || USER='vagrant'
[ "$PASSWORD" ] || PASSWORD='vagrant'
[ "$IP" ]       || IP='192.168.123.196'

usage() {
    echo "Usage: ${0} "
    echo
    echo "Available commands are:"
    echo -e "\trun\trun command"
    echo -e "\tps\trun command as powershell"
    echo -e "\t<file>\tto execute"
    echo
    echo "Files with ps1 extension are executed with powershell"
}

error(){
    local msg="${1}"
    echo "${msg}"
    exit 1
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

run_file(){
    # Execute file
    local cmd_file=$cmd_type
    [ -x "$cmd_file" ] || usage

    # ${string##substring}: Deletes longest match of $substring from front of $string.

    # commands=$(<$cmd_file)
    local suffix=${cmd_file##*.}

    case "$suffix" in
        ps1)
            # strip comments and newlines
            # separate commands with ';'
            commands=`sed '/#/d' $cmd_file | tr '\n' '; '`
            ps "$commands"
            ;;
        *) cmd "$commands" ;;
    esac
}

main(){
    local scriptname='run.sh'
    [ `basename $0` == $scriptname ] || return 1

    local cmd_type="$1"
    local cmd_arg="$2"

    case "$cmd_type" in
        cmd)
            cmd $cmd_arg
            ;;
        ps)
            ps $cmd_arg
            ;;
        *)
            run_file $cmd_file
            ;;
    esac

}

main $*
