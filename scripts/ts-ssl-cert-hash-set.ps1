#
# Set the SSLCertificateSHA1Hash of the Terminal Server
#

if($args.Count -eq 0){
    echo 'Error. Missing SSL Cert Hash'
    echo "Usage: powershell ts-ssl-cert-hash-set.ps1"
    exit 1
}


$thumbprint = $args[0]
wmic /namespace:\\root\cimv2\TerminalServices PATH Win32_TSGeneralSetting Set SSLCertificateSHA1Hash="$thumbprint"
