set software=\\srvctxdc01.adm.aarhuskommune.dk\install\software

set logfile_msi=c:\cabo\logs\msiexec.log
set logfile_print=c:\cabo\logs\printdriver.log
set logfile_progress=c:\cabo\logs\progress-master.log
set logfile_srvmgr=c:\cabo\logs\srvmgr.log

mkdir c:\cabo\logs

ServerManagercmd.exe -install NET-Framework >> %logfile_srvmgr%
ServerManagercmd.exe -install NET-Framework-Core >> %logfile_srvmgr%

cmd.exe /C "%software%\office2007-aak\20_microsoft_.net_framework_3.5_full\dotnetfx35.exe /passive /norestart"
cmd.exe /C "%software%\office2007-aak\30_visual_studio_tools_for_the_office_system_3.0_runtime\vstor30.exe /q"
cmd.exe /C "%software%\office2007-aak\40_visual_studio_tools_for_the_office_system_4.0_runtime\vstor40_x64.exe /q"
msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\office2007-aak\50_microsoft_office_2007_primary_interop_assemblies\o2007pia.msi"
msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\office2007-aak\60_skabelonloesning\SkabelonAddIn.msi"
msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\office2007-aak\70_ciriusintegrator\CiriusIntegrator_11-04-2008_1.0.75_v2.1.0004.msi"

msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\booking\ResourceCentralAddin2007v3.09.0018.msi" ALLUSERS="1"
