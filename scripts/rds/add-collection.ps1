$pool = 'RDS Session Collection';
$desc = 'Created by the RDS App';
$fqdn = [System.Net.Dns]::GetHostByName($env:COMPUTERNAME).HostName

New-RDSessionCollection `
  -CollectionName $pool `
  -SessionHost $fqdn `
  -CollectionDescription $desc `
  -ConnectionBroker $fqdn
