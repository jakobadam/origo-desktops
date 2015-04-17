Import-Module RemoteDesktop

if($args.Count -eq 0){
    echo 'Error. Name of session collection must be supplied!'
    exit 1
}

$name = $args[0]

$applications = Get-RDAvailableApp -CollectionName $name
foreach($app in $applications){
    echo $app.DisplayName
}
