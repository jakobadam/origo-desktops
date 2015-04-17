set software=\\srvctxdc01.adm.aarhuskommune.dk\install\software

set logfile_msi=c:\cabo\logs\msiexec.log
set logfile_print=c:\cabo\logs\printdriver.log
set logfile_progress=c:\cabo\logs\progress-master.log
set logfile_srvmgr=c:\cabo\logs\srvmgr.log

REM EDOC
REM INFO: Package: Edoc
REM INFO: Version: 4.17.3.8
REM INFO: Description: Edoc!
REM INFO: Updated: 20140220
REM INFO: Contact: tp@aarhus.dk

msiexec.exe /L*+ %logfile_msi% /i "%software%\edoc\20140220\360 Client\360 Client.msi" /qr /norestart ALLUSERS="1"
net stop SoftwareInnovationGlobeClient
msiexec.exe /L*+ %logfile_msi% /i "%software%\edoc\20140220\eDoc 4 Client 4.17.3.8\eDoc 4 Client 4.17.3.8.msi" /qr /norestart ALLUSERS="1"
:: Er denne relevant? regedit.exe /s "%software%\edoc\20140220\eDoc_Client64_CTX.reg"
