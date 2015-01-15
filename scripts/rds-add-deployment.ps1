﻿$name = $env:COMPUTERNAME
$domain = $env:USERDNSDOMAIN
$fqdn = "$name.$domain"

#Import-Module RemoteDesktop

New-RDSessionDeployment `
    -ConnectionBroker $fqdn `
    -WebAccessServer $fqdn `
    -SessionHost "sh1.example.com"
    
# New-RDSessionDeployment : Validation failed for the "RD Session Host" parameter.
# RDS.EXAMPLE.COM      You cannot restart the local server.
