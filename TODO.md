## Problems installing MS Access

It return with an error but suceeds in installing?

Maybe WinRM timeout?


## Probblems installing samba

Tryout the newest version on debian7.7. Without success still same
issue.

Tried compiling and installing 4.2 Gave up on a DNS error

## Installing RDS

AD:
* install 'Active Directory Domain Services'
* promote server to domain controller. Root domain: example.com
* Directory Services Restore Mode password: ......
* NetBIOS name: EXAMPLE

RDS:
* Quick start installation guide
* Unable to create the session collection!!! The initiator can't
  restart itself!?!
* Creating a new session collection worked:)

## AD error when joing

Duplicate SID

C:\windows\system32\sysprep\sysprep.exe
* Tick generalize

## Remote RDS calls fails with

```
Get-RDAvailableApp : A Remote Desktop Services deployment does not exist on windows-2012-r2.example.com. This 
operation can be performed after creating a deployment. For information about creating a deployment, run "Get-Help 
New-RDVirtualDesktopDeployment" or "Get-Help New-RDSessionDeployment".
At line:1 char:1
+ Get-RDAvailableApp -CollectionName "RDS Session Collection"
+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    + CategoryInfo          : NotSpecified: (:) [Write-Error], WriteErrorException
    + FullyQualifiedErrorId : Microsoft.PowerShell.Commands.WriteErrorException,Get-RDAvailableApp
```


Also with the authoritative protocol:

```
$cred = Get-Credential
Enter-PSSession -ComputerName windows-2012-r2.example.com -Credential
Set-Item WSMan:\localhost\Client\TrustedHosts -Value * -Force
Get-RDSessionCollection
```

Can only be run from the controlling computer:
```
Get-RDRemoteApp
```


