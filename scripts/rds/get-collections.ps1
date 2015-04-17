Import-Module RemoteDesktop

# New-RDSessionDeployment -SessionHost rds-new.example.com -ConnectionBroker rds-new.example.com
# Get-RDSessionCollection -ConnectionBroker rds-new.example.com

$collections = Get-RDSessionCollection
foreach($c in $collections){
    echo $c.CollectionName
}
