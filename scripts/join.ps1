$log = "Application"
$source = "RDS"
$hostname = "RDS"
$schtask = "RDS Join Task"

Function CreateLog(){
  if(!(Get-EventLog -LogName $log -Source $source)){
    New-EventLog -LogName $log -Source $source   
  }
}

Function LogInfo($message){
  CreateLog
  Write-EventLog -LogName $log -Source $source -EntryType Information -EventId 1 -Message $message
}

Function LogError($message){
  CreateLog
  Write-EventLog -LogName $log -Source $source -EntryType Error -EventId 1 -Message $message
}

# Make sure the information is in the cache table
nbtstat.exe -a "$hostname"

# Cut the ip out of the table
$output = (nbtstat.exe -c | ?{$_ -match "$hostname"})
$ubuntu_ip = ($output -replace '\s+', ' ').Split()[4]
$windows_ip = (ipconfig.exe | ?{$_ -match "Ipv4"}).Split(':')[1].Trim()

$hostname = HOSTNAME
$domain = $env:USERDNSDOMAIN
if($domain){
    $domain = $domain.ToLower()
}

# UseBasicParsing, otherwise IE must have been run?!?
try{
    $url = "http://$ubuntu_ip/api/server/create/?ip=$windows_ip&name=$hostname&domain=$domain&roles=session_host"
    $msg = "Reporting IP back to $url"
    LogInfo($msg)
    echo $msg
    Invoke-WebRequest -UseBasicParsing -Method Post -Uri $url
    schtasks.exe /delete /tn $schtask -f
}
catch{
    $err = "Error calling $url $_.Exception"
    LogError($err)
    echo $err
}