$alias = "notepad"
$name = "notepad"
$path = (gcm "$name").path
$collection = "Collection"
$fqdn = "$env:computername.$env:userdnsdomain"

new-rdremoteapp -Alias $alias -DisplayName $name -FilePath $path -ShowInWebAccess 1 -collectionname $collection -ConnectionBroker $fqdn