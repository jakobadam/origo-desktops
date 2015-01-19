$applications = Get-RDAvailableApp -Debug -Verbose -CollectionName 'RDS Session Collection'
foreach($app in $applications){
    echo $app.DisplayName
}
