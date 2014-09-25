

New-RDRemoteApp `
    -Alias Wordpad `
    -DisplayName WordPad `
    -FilePath "C:\Program Files\Windows NT\Accessories\wordpad.exe" `
    -ShowInWebAccess 1 `
    -collectionname MySessionCollection `
    -ConnectionBroker LS01.CRFB.Local