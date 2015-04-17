Import-Module RemoteDesktop

$collections = Get-RDSessionCollection
foreach($c in $collections){
    echo $c.CollectionName
}