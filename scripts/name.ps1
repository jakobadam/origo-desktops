$name = $args[0]

function usage(){
    $path = $MyInvocation.ScriptName
    echo "Usage: powershell $path DNS"
}

function get_name(){
    echo $env:COMPUTERNAME
}

function set_name(){
    $computer = Get-WmiObject -Class Win32_ComputerSystem
    $computer.rename($name)
}

if(!$name){
    get_name
}
else{
    set_name
}
