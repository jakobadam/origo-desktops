netREM ####################################################
REM THIS SCRIPT RUNS ON MASTER AND INSTALLS ALL SOFTWARE
REM ####################################################

set software=b:\software
set logfile_msi=c:\cabo\logs\msiexec.log
set logfile_print=c:\cabo\logs\printdriver.log
set logfile_progress=c:\cabo\logs\progress-master.log
set logfile_srvmgr=c:\cabo\logs\srvmgr.log
set syslog=logger -l 10.225.17.5

REM 'REM' the line below when ready to run on a weekly master. 
REM CAUTION CAUTION - _NEVER_ _EVER_ boot golden master with the line belov REM'ed!
REM goto :EOF

REM Just to show that we are running...
mkdir "c:\cabo\install\step1"
mkdir "c:\cabo\logs"

if exist "c:\cabo\install\masterok" goto :EOF

cmd.exe /C "copy %software%\cabo\logger.exe c:\windows\system32"
call:logger "Initiating script"

REM Windows Installer RDS Compatibility
call:log_execute change user /install
call:log_execute regedit /s "%software%\kmd_sap\TSMSI.reg"

if exist "c:\cabo\install\step6" goto step6
if exist "c:\cabo\install\step5" goto step5
if exist "c:\cabo\install\step4" goto step4
if exist "c:\cabo\install\step3" goto step3
if exist "c:\cabo\install\step2" goto step2
if exist "c:\cabo\install\step1" goto step1

:step1
REM Allow RDP in firewall (probably needs to be in correct OU to make sure we get linked to the licening server)
call:logger "Step1 - activating firewall rule (RDP)"
call:log_execute netsh advfirewall firewall set rule name="Fjernskrivebord (TCP-in)" new enable=yes 

REM Join server to domain and reboot
call:logger "Step1 - joining domain"
netdom join srvctxmaster /Domain:adm.aarhuskommune.dk /UserD:"adm\admincabo" /PasswordD:%1 
call:logger "Step1 - joining domain exited with errorlevel: %errorlevel%"
call:log_execute mkdir "c:\cabo\install\step2"
call:logger "Step1 - rebooting"
call:log_execute shutdown /r /t 0
goto :EOF

:step2
call:log_execute net time /domain:adm.aarhuskommune.dk /SET /Y
REM Install all packages
call:logger "Step2 - Installing server roles"
call:log_execute mkdir "c:\cabo\programs"

call:log_execute ServerManagercmd.exe -install GPMC >> %logfile_srvmgr%
call:log_execute ServerManagercmd.exe -install NET-Framework >> %logfile_srvmgr%
call:log_execute ServerManagercmd.exe -install NET-Framework-Core >> %logfile_srvmgr%
call:log_execute ServerManagercmd.exe -install Print-Server >> %logfile_srvmgr%
call:log_execute ServerManagercmd.exe -install AD-Domain-Services >> %logfile_srvmgr%
REM Desktop-Experience (requires restart)
call:log_execute ServerManagercmd.exe -install Desktop-Experience >> %logfile_srvmgr%

REM INFO: Package: Indbygget XPS Viewer 
REM INFO: Version: 1
REM INFO: Description: 
REM INFO: Updated: 20130730
REM INFO: Contact: stephen@cabo.dk
call:log_executeServerManagercmd.exe -install XPS-Viewer >> %logfile_srvmgr%

REM INFO: Package: Ny version af Citrix Receiver 
REM INFO: Description: 
REM INFO: Updated: 20130927
REM INFO: Contact: stephen@cabo.dk

call:log_execute cmd.exe /C "C:\ProgramData\Citrix\Citrix online plug-in\TrolleyExpress.exe" /uninstall /cleanup
call:log_execute cmd.exe /C "%software%\CitrixReceiver\CitrixReceiver.exe" /silent /noreboot


call:logger "Step2 - Importing print drivers"
call:log_execute cmd.exe /C "c:\windows\system32\spool\tools\PrintBrm.exe -r -O FORCE -NOACL -f %software%\printdrivers\Citrix-20140130.printerExport > %logfile_print%"
call:log_execute mkdir "c:\cabo\install\step3"
call:logger "Step2 - rebooting"
call:log_execute shutdown /r /t 0
goto :EOF

:step3
REM Install AAK Office 2007 Suite with all whistles and bells...

REM Install AAK Office 2007
call:logger "Step3 - Installing AAK Office 2007 Suite (and ready to reboot!)"

REM Office install will reboot, so we have to mark step3 now!
call:log_execute mkdir "c:\cabo\install\step4"
REM INFO: Package: Office 2007 Std
REM INFO: Version: SP3
REM INFO: Description: 
REM INFO: Updated: 20121025
REM INFO: Contact: tp@aarhus.dk
call:log_execute cmd.exe /C "%software%\office2007-aak\10_office2007std_citrix-201210\setup.exe"


REM INFO: Package: Access 2007 
REM INFO: Version: 
REM INFO: Description: 
REM INFO: Updated: 20130419
REM INFO: Contact: stephen@cabo.dk
call:log_execute cmd.exe /C "%software%\msaccess\setup.exe"



call:logger "Step3 - rebooting"
call:log_execute shutdown /r /t 0
goto :EOF

:step4
if not exist "c:\cabo\install\officeOK" goto :EOF

call:log_execute cmd.exe /C "%software%\office2007-aak\20_microsoft_.net_framework_3.5_full\dotnetfx35.exe /passive /norestart"
call:log_execute cmd.exe /C "%software%\office2007-aak\30_visual_studio_tools_for_the_office_system_3.0_runtime\vstor30.exe /q"
call:log_execute cmd.exe /C "%software%\office2007-aak\40_visual_studio_tools_for_the_office_system_4.0_runtime\vstor40_x64.exe /q"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\office2007-aak\50_microsoft_office_2007_primary_interop_assemblies\o2007pia.msi"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\office2007-aak\60_skabelonloesning\SkabelonAddIn.msi"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\office2007-aak\70_ciriusintegrator\CiriusIntegrator_11-04-2008_1.0.75_v2.1.0004.msi"

REM INFO: Package: SendDigitalt
REM INFO: Version: 3.13
REM INFO: Description: 
REM INFO: Updated: 20130116
REM INFO: Contact: tp@aarhus.dk

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\SendDigitalt_V313\Tieto_Send_Digitalt_v3.1.3.msi" 
call:log_execute copy /Y "%software%\SendDigitalt_V313\configuration.xml" "C:\Program Files (x86)\Tieto\Send Digitalt\configuration.xml"
call:log_execute regedit.exe /S "%software%\SendDigitalt_V313\RegSettings_CU_Localmachine.reg"
REM call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\sepo\Send_Sikkert_x64_2.0.msi" 
REM call:log_execute regedit /s "%software%\sepo\Send_Sikkert_Registry_Settings.reg"  



call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\office2007-aak\90_cirius_knap\JournalizeToCirius.msi" TRANSFORM="%software%\office2007-aak\90_cirius_knap\JournalizeToCirius.Mst"

REM Xenapp PCM
REM INFO: Updated: 20121123
call:log_execute msiexec.exe /L*+ %logfile_msi% /qn /i "%software%\xenapp\xenapppcmagent.msi" CTX_XAPCM_ACCEPT_EULA=yes

REM Install Office Viewers and wrappers
call:logger "Step4 - Installing Office Wrappers"
call:log_execute copy "%software%\officeviewers\Word.exe"       c:\cabo\programs\ /Y 
call:log_execute copy "%software%\officeviewers\Excel.exe"      c:\cabo\programs\ /Y 
call:log_execute copy "%software%\officeviewers\Powerpoint.exe" c:\cabo\programs\ /Y 

REM VB script use with Publish application 
call:log_execute copy "%software%\cabo\Deliveryconsol.vbs"	c:\cabo\programs\ /Y 
call:log_execute copy "%software%\cabo\DSA.vbs" 		c:\cabo\programs\ /Y 
call:log_execute copy "%software%\cabo\explorer.vbs" 		c:\cabo\programs\ /Y 
call:log_execute copy "%software%\cabo\GPO.vbs" 		c:\cabo\programs\ /Y 
call:log_execute copy "%software%\cabo\notes.vbs" 		c:\cabo\programs\ /Y 
call:log_execute copy "%software%\cabo\printer.vbs" 		c:\cabo\programs\ /Y 
call:log_execute copy "%software%\cabo\opdatering.cmd" 		c:\cabo\programs\ /Y 

REM Event2syslog
call:log_execute copy "%software%\cabo\evtsys.dll" 		c:\cabo\programs\ /Y 
call:log_execute copy "%software%\cabo\evtsys.exe" 		c:\cabo\programs\ /Y 

call:logger "Step4 - Installing Office Viewers"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\officeviewers\ppviewer.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\officeviewers\wordview.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\officeviewers\xlview.msi" 
call:log_execute icacls "C:\Program Files (x86)\Microsoft Office\Office12" /restore "%software%\officeviewers\office.acl" 

REM Change file extension for DOC DOCX XLS XLSX PPT PPTX
call:log_execute regedit /s "%software%\officeviewers\cabo.reg" 

call:log_execute mkdir "c:\cabo\install\step5"
call:logger "Step4 - rebooting"
call:log_execute shutdown /r /t 0
goto :EOF

:step5
call:logger "Step5 - Installing dotNet4.0"
call:log_execute mkdir "c:\cabo\install\step6"
call:log_execute cmd.exe /C "%software%\dotnetframework\dotnetframework-4.0.exe /q"  

call:logger "Step5 - rebooting"
call:log_execute shutdown /r /t 0
goto :EOF

:step6
call:logger "Step6 - Installing applications"
call:log_execute cmd.exe /C "%software%\cutewriter\gplghostscript-8.15.exe"  
call:log_execute cmd.exe /C "%software%\cutewriter\cutewriter.exe /verysilent /no3d"  
REM call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\office2007-aak\officeAddin.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\zsroer\kmd_zsroer-2.4.10.msi" 
REM call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\visio\2003\vispro.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\adobereader\11.0\AcroRead.msi" 

REM INFO: Package: Adobe flash til pluginbaserede browsere
REM INFO: Description: Plugin til visning af flash indhold
REM INFO: Updated: 20130419
REM INFO: Contact: stephen@cabo.dk
call:log_execute cmd.exe /C "%software%\flashplayer\install_flash_player_ax.exe -install"

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\lotusnotes\6.5.5\Lotus Notes 6.5.5 da.msi" 
REM call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\cirius\cirius_integrator-11-04-2008-1.0.75-v2.1.0004.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\caretaker\sqlncli_x64_caretaker.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\caretaker\caretaker-3.0.09.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_doc2archive\kmd_doc2archive-2.1.0.0.msi" 


REM INFO: Package: Firefox
REM INFO: Version: Firefox 18.0.1
REM INFO: Description: Firefox er en gratis internetbrowser
REM INFO: Updated: 20130128
REM INFO: Contact: toa@aarhus.dk

call:log_execute cmd.exe /C "%software%\firefox\firefox_setup_18_0_1.exe -ms"


REM INFO: Package: KMD Institution
REM INFO: Version: 9.3.1.0
REM INFO: Description: Dagplejen
REM INFO: Updated: 20130522
REM INFO: Contact: jsn@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_institution\kmd_institution_9.3.1.0.msi" 

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_eindkomst\kmd_eindkomst-2.0.0.msi" 

REM INFO: Package: KMD SAG Min arbejdsplads
REM INFO: Version: 1.3.0.0
REM INFO: Description: 
REM INFO: Updated: 20120501
REM INFO: Contact: helo@aarhus.dk

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sag_min_arbejdsplads\kmd_sag_min_arbejdsplads_1_3_0_0.msi" 


REM INFO: Package: KMD Social Pension Sagsdel
REM INFO: Version: 5.0.2.0
REM INFO: Description: 
REM INFO: Updated: 20130502
REM INFO: Contact: helo@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_social_pension_sagsdel\kmd_social_pension_sagsdel_5.0.2.0.msi" 

REM INFO: Package: KMD Social Pension Masseindberetning
REM INFO: Version: 2.2.4.0
REM INFO: Description: 
REM INFO: Updated: 20130212
REM INFO: Contact: helo@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_social_pension_masseindberetning\kmd_social_pension_masseindberetning-2.2.4.0.msi" 

REM INFO: Package: KMD Social Pension AIO
REM INFO: Version: 1.6.4.0
REM INFO: Description: 
REM INFO: Updated: 20130212
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_social_pension_aio\kmd_social_pension_aio-1.6.4.0.msi" 

REM INFO: Package: KMD Social Pension
REM INFO: Version: 4.0.2.0
REM INFO: Description: 
REM INFO: Updated: 20130502
REM INFO: Contact: helo@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_social_pension_kommunedel\kmd_social_pension_kommunedel-4.0.2.0.msi" 


call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_structura\kmd_structura-4.0.1.0.msi" 
call:log_execute cmd.exe /C "%software%\kmd_sag_edh_og_dagsorden\dependencies\vstor40_LP_x86_dan.exe /q"   
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sag_edh_og_dagsorden\dependencies\kmd_certifikat-1.0.0.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sag_edh_og_dagsorden\dependencies\kmd_logonweb2.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sag_edh_og_dagsorden\dependencies\kmd_sag_ocx_moduler-2.0.msi" 
REM call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sag_edh_og_dagsorden\dependencies\microsoft_office_2007_primary_interop_assemblies.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sag_edh_og_dagsorden\kmd_sag_admin-12.3.2.0-20120124.msi" 

REM INFO: Package: Kmd sag
REM INFO: Version: 13.4.1
REM INFO: Description: 
REM INFO: Updated: 20120501
REM INFO: Contact: helo@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sag\kmd_sag_13.4.msi" INSTALL=ABE INTGR=WE  DOKBIB="Q:\KMDSagData" /norestart 


REM INFO: Package: KMD Børn og Voksen
REM INFO: Version: 4.13.1
REM INFO: Description: 
REM INFO: Updated: 20130510
REM INFO: Contact: helo@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_born_og_voksne\kmd_born_og_voksne-4.13.1.msi"

REM INFO: Package: LARA
REM INFO: Version: ?
REM INFO: Description: 
REM INFO: Updated: 20130809
REM INFO: Contact: stephen@cabo.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\lara\setup_larahosting.msi" 

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\skolekom\skolekom-9126dk.msi" 

REM INFO: Package: KMD Indkomst
REM INFO: Version: 2.2.0.0
REM INFO: Description: 
REM INFO: Updated: 20121220
REM INFO: Contact: helo@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_indkomst\kmd_indkomst_2.2.0.0.msi" 

REM INFO: Package: ResourceCentral
REM INFO: Version: ResourceCentral 3.9.18
REM INFO: Description: Officeplugin til booking af lokaler
REM INFO: Updated: 20140327
REM INFO: Contact: tp@aarhus.dk

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\booking\ResourceCentralAddin2007v3.09.0018.msi" ALLUSERS="1"
REM call:log_execute regedit /s "%software%\booking\RCSetRegistry.reg"
REM call:log_execute regedit /s "%software%\booking\RCSetAddin.reg" 

REM INFO: Package: Digitsa Signatur
REM INFO: Version: 6.4.2.2
REM INFO: Description: Backup og restore af digital medarbejdersignatur
REM INFO: Updated: 20120630
REM INFO: Contact: tp@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\danid\csp-6.4.2.2.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_edagpenge_barsel\kmd_edagpenge_barsel-2.3.0.1.msi" 

REM INFO: Package: KMD eDagpenge-Sygdom
REM INFO: Version: 3.7.55.2
REM INFO: Description: 
REM INFO: Updated: 20130214
REM INFO: Contact: helo@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_edagpenge_sygdom\kmd_edagpenge_sygdom-3.7.55.2.msi" 

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\syslogagent\syslogagent_64b_v_1_2_0.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\opsview-agent\opsview-agent-3.9.0.5490-0.3.8-64bit.msi" 

REM Netblanket Klient
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\net_blanket_klient\NetBlanketklient_Citrix_2012.msi"
call:log_execute cmd.exe /C "regedit /s %software%\net_blanket_klient\REP.reg"
call:log_execute cmd.exe /C "regedit /s %software%\net_blanket_klient\HKCR.reg"
call:log_execute cmd.exe /C "regedit /s %software%\net_blanket_klient\HKCU.reg"
call:log_execute cmd.exe /C "regedit /s %software%\net_blanket_klient\HKLM.reg"

REM KMD_DOC2MAIL (requires acrobat-reader to be installed first and pdf-echnage after!)
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_doc2mail\kmd_doc2mail_x64-2.3.0.3.msi"

REM Installing PDFExchange
REM INFO: Package: PDFExchange
REM INFO: Version: ?
REM INFO: Description: PFDExchange - Alternative to Adope Acrobat Viewer
REM INFO: Updated: 20120525
REM INFO: Contact: tp@aarhus.dk
call:log_execute cmd.exe /C %software%\pdfexchange\20120525-pdfxc\PDFXVwer.exe /verysilent /norestart /components="pdfviewer, IEAddin, FFaddin, Languagess" /pdfvinbrowser /LANG=dk /Noinstask
call:log_execute cmd.exe /C "c:\Program Files\Tracker Software\PDF Viewer\PDFXCview.exe" /importp %software%\pdfexchange\20120525-pdfxc\settings.dat
call:log_execute cmd.exe /C del /Q "c:\Program Files\Tracker Software\PDF Viewer\Searchproviders\*.*"

REM LOS
call:log_execute cmd.exe /C "%software%\los\los-3.7.0.exe /s" 

REM Registring ocx files for KMD LOS and KMD BØRN OG VOKSNE
call:log_execute regsvr32.exe /S C:\Windows\SysWOW64\mhcmbo32.ocx
call:log_execute regsvr32.exe /S C:\Windows\SysWOW64\ssdock32.ocx
call:log_execute regsvr32.exe /S C:\Windows\SysWOW64\richtx32.ocx

REM EDOC
REM INFO: Package: Edoc
REM INFO: Version: 4.17.3.8
REM INFO: Description: Edoc!
REM INFO: Updated: 20140220
REM INFO: Contact: tp@aarhus.dk

call:log_execute msiexec.exe /L*+ %logfile_msi% /i "%software%\edoc\20140220\360 Client\360 Client.msi" /qr /norestart ALLUSERS="1"
call:log_execute net stop SoftwareInnovationGlobeClient 
call:log_execute msiexec.exe /L*+ %logfile_msi% /i "%software%\edoc\20140220\eDoc 4 Client 4.17.3.8\eDoc 4 Client 4.17.3.8.msi" /qr /norestart ALLUSERS="1"
call:log_execute regedit.exe /s "%software%\edoc\20140220\eDoc_Client64_CTX.reg"




REM KMD SAP
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sap\add-on\msxml.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sap\add-on\vc9_redist_x86.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_sap\add-on\vcredist_x86.msi" 
call:log_execute cmd.exe /C "%software%\kmd_sap\72008\program\720-08\setup\NwSAPsetup.exe /package:LokalMedBW /silent"
call:log_execute cmd.exe /C "copy %software%\kmd_sap\720-02\KMD\KMD-ini\saplogon.ini c:\windows\ /Y"
call:log_execute cmd.exe /C "%software%\kmd_sap\72008\program\720-08\KMD\Opdatini.exe /s

REM SAP
REM INFO: Package: SAP
REM INFO: Version: 7.30
REM INFO: Description: SAP
REM INFO: Updated: 20140406
REM INFO: Contact: tp@aarhus.dk

call:log_execute cmd.exe /C "%software%\SAP\20140406_SAP_7.30\Program\730-01\setup\NwSapSetup.exe /package:"LokalMedBW"" /silent
call:log_execute cmd.exe /C "%software%\SAP\20140406_SAP_7.30\Program\730-01\KMD\Opdatini.exe" /silent 
call:log_execute cmd.exe /C "%software%\SAP\20140406_SAP_7.30\Program\730-01\Patches\bw350gui730_2.exe /nodlg" /silent
call:log_execute regedit.exe /s "%software%\SAP\20140406_SAP_7.30\4. Add_CSV.reg"
call:log_execute regedit.exe /s "%software%\SAP\20140406_SAP_7.30\5. Add_MSG.reg"

REM INFO: Package: Microsoft Dynamics NAV
REM INFO: Version: 2009 SP1
REM INFO: Description:
REM INFO: Updated: 20120910
REM INFO: Contact: anbol@aarhus.dk

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\navisionaarhus-nvs\bizconnector3-0.msi" TRANSFORMS="%software%\navisionaarhus-nvs\bizconnector3-0.mst"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\navisionaarhus-nvs\microsoft-dynamics-nav-2009-sp1.msi" TRANSFORMS="%software%\navisionaarhus-nvs\microsoft-dynamics-nav-2009-sp1.mst"

REM INFO: Package: KMD Ejendomdecentral
REM INFO: Version: 3.7
REM INFO: Description:
REM INFO: Updated: 20130430
REM INFO: Contact: anbol@aarhus.dk (change by stephen@cabo.dk)

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_ejendomdecentral\emdbdatagateway2-0.msi" TRANSFORMS="%software%\kmd_ejendomdecentral\emdbdatagateway2-0.mst"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_ejendomdecentral\kmdejendomdecentral3-7.msi" TRANSFORMS="%software%\kmd_ejendomdecentral\kmdejendomdecentral3-7.mst"
call:log_execute cmd.exe /C regedit /S "%software%\kmd_ejendomdecentral\kmd_ejendomdecentral.reg"
call:log_execute cmd.exe /C cscript.exe /nologo "%software%\kmd_ejendomdecentral\createDSN.vbs"

REM INFO: Package: NetViewer
REM INFO: Version: SP3
REM INFO: Description:
REM INFO: Updated: 20131219
REM INFO: Contact: anbol@aarhus.dk (change by stephen@cabo.dk)

call:log_execute cmd.exe /C %windir%\Microsoft.NET\Framework\v2.0.50727\caspol -q -m -ag All_Code -strong -hex 002400000480000094000000060200000024000052534131000400000100010035334CEAF19B5D98CC522F75D9D6394FC9A0F301B0E0E80A2DC9EA1F5D2DEF601AA31EC7861F690023B751F2590363E95BA2DB3CDFC009A4865C47F3692A581A4D4D52F41298A60D6D91E070DCD64098772F0A6D8DB9BCA761709F5074CC1797F7D717558BF5EA38180B5F6008D2CE987E20037ADB8C069B08706C42D44823EE -noname -noversion FullTrust -n "IntergraphSetup_Strong_Name"

REM Install netviewer
call:log_execute cmd.exe /C %software%\Netviewer\10.01.0003.25001MR\Setup.exe /s GTechnology /n ADDLOCAL=NetViewerClient ACCEPT_EULA=1

REM CAB Module registration 
call:log_execute cmd.exe /C regedit /S "%software%\Netviewer\Client\CAB_registration_64bit.reg"

REM  Copy NetViewer config file to local folder
call:log_execute cmd.exe /C copy %software%\Netviewer\Client\IngrViewer.exe.config "C:\Program Files (x86)\Intergraph\GTechnology\Program\"

REM The following line of code enables the GTech application to execute dll's that are placed in common AddIn-folder on the application server
call:log_execute cmd.exe /C %windir%\Microsoft.NET\Framework\v2.0.50727\caspol -q -m -ag All_Code -url \\srvwebreg06\DDC\AddIn\* FullTrust -n "CustomAssemblyCodeGroupName"
call:log_execute cmd.exe /C %windir%\Microsoft.NET\Framework\v2.0.50727\caspol -q -m -ag All_Code -url \\srvwebreg06\DDC\AddIn\GDAL\* FullTrust -n "LPGDAL"

REM DKTrans that enables coordinate transformation within GTech needs to be install locally on the client machine

call:log_execute cmd.exe /C "%software%\Netviewer\Client\DKTrans\DKTrans-3.1-GT10.1.exe" /SP- /SILENT /NOCANCEL

REM GTech fonts are copied to the Windows Fonts-folder and registered
call:log_execute cmd.exe /C copy %software%\Netviewer\Client\FONTE C:\WINDOWS\Fonts\

call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "Afloeb (TrueType)" /t REG_SZ /d Afloeb.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "AKFJERNV (TrueType)" /t REG_SZ /d AKFJERNV.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "AKBygvaerk (TrueType)" /t REG_SZ /d AKBygvaerk.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "AKSpildevand (TrueType)" /t REG_SZ /d AKSpildevand.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "AKTransmission (TrueType)" /t REG_SZ /d AKTransmission.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "AKV (TrueType)" /t REG_SZ /d AKV.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "AKVand (TrueType)" /t REG_SZ /d AKVand.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "DANDAS_AKV (TrueType)" /t REG_SZ /d DANDAS_AKV.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "DONG Gas Symboler (TrueType)" /t REG_SZ /d DONG_Gas.TTF /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "ELDKSYMBOL (TrueType)" /t REG_SZ /d ELDKSYMBOL.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "G_COMMON (TrueType)" /t REG_SZ /d G_COMMON.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "G_DIM___ (TrueType)" /t REG_SZ /d G_DIM___.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "G_MapPins (TrueType)" /t REG_SZ /d G_MAPPIN.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "GeoMedia Coax (TrueType)" /t REG_SZ /d MGCOAX.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "GeoMedia GIS (TrueType)" /t REG_SZ /d MGGIS.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "GeoMedia Util (TrueType)" /t REG_SZ /d MGUTIL.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "GRUNDKORT (TrueType)" /t REG_SZ /d GRUNDKORT.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "MATR (TrueType)" /t REG_SZ /d MATR.ttf /f
call:log_execute cmd.exe /C reg add "HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts" /v "MKGT2 (TrueType)" /t REG_SZ /d MKGT2.ttf /f

REM Installation af Netviewer er færdig!!!

REM Sun Java

call:log_execute cmd.exe /C "%software%\java\jre-7u51-windows-i586 /s"
REM call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\java\java\jre1.6.0_30.msi" 

REM Silverlight
call:log_execute cmd.exe /C "%software%\Silverlight\Silverlight.exe /q" 

REM Install PDF wrappers
call:log_execute copy "%software%\reader\PDF.exe" c:\cabo\programs\ /Y
call:log_execute regedit /s "%software%\adobereader\cabo.reg" 

REM Install cabomon
call:log_execute cmd.exe /C "copy %software%\cabo\getdata.exe  c:\cabo\programs /Y"
call:log_execute cmd.exe /C "copy %software%\cabo\nssm.exe  c:\cabo\programs /Y"
call:log_execute cmd.exe /C "c:\cabo\programs\nssm.exe install cabomon c:\cabo\programs\getdata.exe"

REM Install Lotus Smartsuite
call:log_execute cmd.exe /C "%software%\lotussmartsuite\9.8\setup.exe /v"/passive RSP=\"%software%\lotussmartsuite\9.8\120220aakctx.rsp\"""

REM Install CiriusJournalisering
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\cirius\20120411\JournalizeToCirius.msi" ALLUSERS="1"
call:log_execute regedit.exe /s "%software%\cirius\20120411\regsettingsCU.reg /quiet"

REM Install SEP
REM INFO: Package: Symantec Endpoint Protection
REM INFO: Version: 12
REM INFO: Description: Symantec Endpoint Protection
REM INFO: Updated: 20120524
REM INFO: Contact: support-aak@cabo.dk
REM DISABLED 20120905 call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\sep\Sep64.msi"
REM DISABLED 20120905 call:log_execute regedit /s "%software%\sep\Citrix-symantec.reg"

REM Install 3270
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\ibm3270\20120412\5_Completed_MSI\CICS3270 1020003401.msi" TRANSFORMS="%software%\ibm3270\20120412\5_Completed_MSI\CICS3270 1020003401.mst"

REM Renomatic suite
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\renomatic\renomatic_akv_bi-2.0.msi"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\renomatic\renomatic-akv_emimport-2.5.13.msi"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\renomatic\renomatic_akv-2.34.2.msi"

REM INFO: Package: KMD Matrix
REM INFO: Version: 4.10.0 Opdaterer version 4.9.2, men kan installeres selvstændigt.
REM INFO: Description: Skolelærernes lønsystem. 
REM INFO: Updated: 20140127
REM INFO: Contact: jsn@aarhus.dk

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_matrix\kmd_matrix_4-10-1.msi"
call:log_execute cmd.exe /C del /q "C:\Users\Public\Desktop\KMDMAT~1.lnk" 
call:log_execute cmd.exe /C del /q "C:\Users\Public\Desktop\KMDMAT~1.lnk"


REM KMD Matrix Forvaltning
REM INFO: Package: KMD Matrix Forvaltning
REM INFO: Version:  2.9.0.
REM INFO: Description: Skolelærernes lønsystem
REM INFO: Updated: 20130313
REM INFO: Contact: jsn@aarhus.dk

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_matrix_forvaltning\kmd_matrix_forvaltning_2-9-0.msi" 
call:log_execute cmd.exe /C del /q "C:\Users\Public\Desktop\KMDMAT~1.lnk"
call:log_execute cmd.exe /C del /q "C:\Users\Public\Desktop\KMDMAT~2.lnk"
call:log_execute cmd.exe /C md "C:\Appl\KMD Matrix Forvaltning\excel"
call:log_execute cmd.exe /C move /y "c:\ArbejdstidskontiStatistik.xlt" "C:\Appl\KMD Matrix Forvaltning\excel"
call:log_execute cmd.exe /C move /y "c:\KlasseStatistik.xlt" "C:\Appl\KMD Matrix Forvaltning\excel"
call:log_execute cmd.exe /C move /y "c:\PersonaleStatistik.xlt" "C:\Appl\KMD Matrix Forvaltning\excel"
call:log_execute cmd.exe /C move /y "c:\TILLGG~1.xlt" "C:\Appl\KMD Matrix Forvaltning\excel"
call:log_execute cmd.exe /C move /y "c:\UndervisningstidStatistik.xlt" "C:\Appl\KMD Matrix Forvaltning\excel"

REM KMD ProKap
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_prokap\kmd_prokap-3.0.3.0.msi" 

REM KMD Dagpleje
REM INFO: Package: KMD Dagplejemodul
REM INFO: Version: 3.8.0.0
REM INFO: Description: Dagplejen
REM INFO: Updated: Ukendt
REM INFO: Contact: jsn@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_dagpleje\kmd_dagpleje-3.8.0.0.msi" 

REM INFO: Package: TM Sund
REM INFO: Version: 3.1.2.255
REM INFO: Description: Sundhedsplejen. 
REM INFO: Updated: 20140127
REM INFO: Contact: jsn@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\tmsund\CRRuntime_32bit_13_0_2.msi"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\tmsund\CRRuntime_64bit_13_0_2.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\tmsund\tmsund-3.1.2.255.msi"
call:log_execute cmd.exe /C copy /y "%software%\tmsund\config.xml" "C:\Program Files (x86)\TM Care\TM Sund"
call:log_execute cmd.exe /C copy /y "%software%\tmsund\boernelaege.rpt" "C:\Program Files (x86)\TM Care\TM Sund\Reports\Continuation\boernelaege.rpt"
call:log_execute cmd.exe /C cacls "C:\Program Files (x86)\TM Care\TM Sund" /T /E /C /G "adm\GG-DIST-APP-MBU-PAK-GRP-SUND:C"

REM INFO: Package: TM Tand
REM INFO: Version: 2.6.13.255 Opdaterer version 2.6.2.255, men kan installeres selvstændigt.
REM INFO: Description: Tandplejen. 
REM INFO: Updated: 20140423
REM INFO: Contact: jsn@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\tmtand\tmtand-2.6.13.255.msi"
call:log_execute cmd.exe /C copy /y "%software%\tmtand\TMTServerConfig.xml" "C:\Program Files (x86)\TM Care\TM Tand\Config"
call:log_execute cmd.exe /C cacls "C:\Program Files (x86)\TM Care\TM Tand" /T /E /C /G "adm\GG-DIST-APP-MBU-PAK-GRP-TAND:C"

REM TABULEX TEA
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\tabulex_tea\tabulex_tea-2.3.0.msi" 
call:log_execute cmd.exe /C del /q "C:\Users\Public\Desktop\Tabulex Tea.lnk"

REM KMD RAMMESTYRING
call:log_execute cmd.exe /C %software%\kmd_rammestyring\02.00.007\Setup_Rammestyring.exe /s

REM KMD BØPAS
call:log_execute cmd.exe /C %software%\kmd_boepas\4.0.16\Setup_BoepasCics2000.EXE /s
call:log_execute cmd.exe /C del /q "C:\Users\Public\Desktop\BPAS~1.LNK"


REM INFO: Package: Visio viewer til Internet Explorer
REM INFO: Version: 14.0.4730.1010
REM INFO: Description: 
REM INFO: Updated: 20120920
REM INFO: Contact: tp@aarhus.dk
call:log_execute cmd.exe /C "%software%\visio\visioviewer3.exe /quiet"

REM INFO: Package: OpenSSL til Kingo
REM INFO: Version: 1.0.0
REM INFO: Description: 
REM INFO: Updated: 20120524
REM INFO: Contact: jsn@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% INSTALLDIR="C:\Appl\OpenSSL-Win32\" /passive /i "%software%\kingo\OpenSSL_Light_1-0-0e.msi" 

REM Registrering af Citrix WMI MOF components
call:log_execute mofcomp "C:\Program Files (x86)\Citrix\system32\Citrix\WMI\citrix.XP10FR3.mof" 
call:log_execute mofcomp "C:\Program Files (x86)\Citrix\system32\Citrix\WMI\citrix.XP10FR3.mof" 
call:log_execute mofcomp "C:\Program Files (x86)\Citrix\system32\Citrix\WMI\citrixProv.XP10FR3.mof" 
call:log_execute mofcomp "C:\Program Files (x86)\Citrix\system32\Citrix\WMI\metaframe.XP10FR3.mof" 
call:log_execute mofcomp "C:\Program Files (x86)\Citrix\system32\Citrix\WMI\metaframeProv.XP10FR3.mof" 
call:log_execute mofcomp "C:\Program Files (x86)\Citrix\system32\Citrix\WMI\mgmt.XP10FR4.mof"

REM INFO: Package: ØRS1 Bestiller
REM INFO: Version: 7.2013
REM INFO: Description:ØRS1 Bestiller 
REM INFO: Updated: 20132506
REM INFO: Contact: krj@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\ors\ors1\ors1.msi"

REM INFO: Package: ØRS3
REM INFO: Version: 8.2013
REM INFO: Description:ØRS 3
REM INFO: Updated: 20130828
REM INFO: Contact: krj@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\ors\ors3\ors3.msi"

REM INFO: Package: Salto
REM INFO: Version: ?
REM INFO: Description: 
REM INFO: Updated: 20120719
REM INFO: Contact: kqj@aarhus.dk
call:log_execute cmd.exe /C %software%\salto\unzip.exe %software%\salto\rw_pro-access.zip -d "%ProgramFiles(x86)%\Salto"

REM INFO: Package: DDELibra
REM INFO: Version: 9.10.22
REM INFO: Description: DDElibra er bibliotekssystemet i Danmark, hvor folke- og skolebiblioteker kan indgå i et fælles samarbejde om bibliotekskatalog og system.
REM INFO: Updated: 20140509
REM INFO: Contact: toa@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\ddelibra\ddelibra_9.10.22.msi" 

REM INFO: Package: KMD Vagtplan
REM INFO: Version: 6.8.2.2
REM INFO: Description: 
REM INFO: Updated: 20120524
REM INFO: Contact: tp@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_vagtplan\20120522\Oracle_11-2-0-1_Klient_Aarhus\Oracle_11-2-0-1_Klient.msi" /t "%software%\Oracle_11-2-0-1_Klient_Aarhus\Oracle_11-2-0-1_Klient_Aarhus.mst"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\kmd_vagtplan\20120522\mag1\KMD_Vagtplan_6-8-2-2-mag1.msi" 

REM INFO: Package: VitaeSuiten
REM INFO: Version: 8.8.8.10
REM INFO: Type: SCRIPT
REM INFO: Description: Vitae, Disponeriring brio og Vitaestatistik (Borgerjournal for MSO)
REM INFO: Updated: 20130917
REM INFO: Contact: kqj@aarhus.dk
REM Microsoft Report Viewer 2010
call:log_execute cmd.exe /C "%software%\vitaesuiten\8.8.8.10\ReportViewer.exe /q"
REM Microsoft Chart Controls for Microsoft .NET Framework 3.5 software update
call:log_execute cmd.exe /C "%software%\vitaesuiten\8.8.8.10\MSChart.exe /q"
REM Microsoft Visual C++ 2008 (x86)
call:log_execute cmd.exe /C "%software%\vitaesuiten\8.8.8.10\vcredist_2008_x86.exe /Q"
REM Microsoft Visual C++ 2010 (x86)
call:log_execute cmd.exe /C "%software%\vitaesuiten\8.8.8.10\vcredist_2010_x86.exe /Q"
REM VITAE Journal Klienten
call:log_execute cmd.exe /C "%software%\vitaesuiten\8.8.8.10\vitae\VITAEJournalKlient.exe /S -U="%software%\vitaesuiten\8.8.8.10\vitae\UserSetup.ini" -NoRestart"
REM Brio Intelligence Navigator klientsoftwaren
call:log_execute cmd.exe /C "%software%\vitaesuiten\8.8.8.10\BRIO\Setup.exe -s -f1%software%\vitaesuiten\8.8.8.10\BRIO\CSC_BRIO.iss"
REM VITAE Disponering Klienten 
call:log_execute cmd.exe /C "%software%\vitaesuiten\8.8.8.10\Disp\VITAEDisponeringKlient.exe /S -U="%software%\vitaesuiten\8.8.8.10\Disp\UserSetup.ini" -NoRestart"
REM VITAE Statistik Klienten 
call:log_execute cmd.exe /C "%software%\vitaesuiten\8.8.8.10\Stat\VITAEStatistikKlient.exe /S -U="%software%\vitaesuiten\8.8.8.10\Stat\UserSetup.ini" -NoRestart"

REM INFO: Package: KingoKlient
REM INFO: Version: 1.0.1.286
REM INFO: Description: Kingo
REM INFO: Updated: 20120711
REM INFO: Contact: kqj@aarhus.dk, rj@aarhus.dk
call:log_execute cmd.exe /C md "C:\Program Files (x86)\kingo"
call:log_execute cmd.exe /C copy "%software%\kingo\1.0.1.286\*.*" "C:\Program Files (x86)\kingo\"

REM INFO: Package: UnikBolig4Win32KlientDrift.msi
REM INFO: Version: 4.30.306
REM INFO: Description:
REM INFO: Updated: 20121115
REM INFO: Contact: krj@aarhus.dk
call:log_execute cmd.exe /C %software%\unik\4.3.0306\vstor30sp1-KB949258-x86.exe /q /norestart
REM call:log_execute cmd.exe /C %software%\unik\4.3.0306\vjredist64.exe /Q
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i %software%\unik\4.3.0306\UnikBolig4Win32KlientDrift.msi
call:log_execute cmd.exe /C copy "%software%\unik\4.3.0306\UnikPdata.dll" "C:\Program Files (x86)\Unik System Design as\Bolig 4\Drift"
call:log_execute cmd.exe /C regsvr32 /S "C:\Program Files (x86)\Common Files\Unik System Design as\Common\midas.dll" 
call:log_execute cmd.exe /C regsvr32 /S "C:\Program Files (x86)\Unik System Design as\Bolig 4\Drift\UnikPdata.dll" 

REM INFO: Package: SAS_Graph_ActiveX_Control_9.3
REM INFO: Version: 9.3
REM INFO: Description: 
REM INFO: Updated: 20120815
REM INFO: Contact: helo@aarhus.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\sas_graph_activex_control\sas_graph_activex_control_9.3.msi" 

REM INFO: Package: Change filetype
REM INFO: Version: 0.1
REM INFO: Description:
REM INFO: Updated: 20120911
REM INFO: Contact: stephen@cabo.dk
call:log_execute cmd.exe /C "cscript /nologo %software%\cabo\filtype-script.vbs"

REM INFO: Package: DynamicTemplate
REM INFO: Version: 1.7.33
REM INFO: Description: Skabelonløsning til Office med P-data integration. Anvendes fra 1. okt 2013 som den nye skabelonløsning. Kræver .net 4 samt VS 2010.
REM INFO: Updated: 20130910
REM INFO: Contact: toa@aarhus.dk, chs@aarhus.dk

call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\dynamictemplate1733\Setup-Solution-1-7-33.msi" SYSTEMPATH="\\adm.aarhuskommune.dk\AAK\Hotel1\TDS\dynamictemplate"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\dynamictemplate1733\setup-PData-1-0-0.msi"

REM INFO: Package: Mapinfo
REM INFO: Version: 11.0.4
REM INFO: Description: 
REM INFO: Updated: 20121107
REM INFO: Contact: stephen@cabo.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\mapinfo\MapInfo Professional 11.0.msi" TRANSFORMS="%software%\mapinfo\MapInfo Professional 11.0.Mst" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\mapinfo\MapInfo Professional 11.0.4 Patch.msi" 
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\mapinfo\Geograf Certifikat 2.0.msi" TRANSFORMS="%software%\mapinfo\Geograf Certifikat 2.0.mst"

REM INFO: Package: G-tech
REM INFO: Version: 10.01.0002
REM INFO: Description: 
REM INFO: Updated: 20121107
REM INFO: Contact: stephen@cabo.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\g-tech\10.01.0002\GTechnology 10.01.0002.msi" TRANSFORMS="%software%\g-tech\10.01.0002\GTechnology 10.01.0002.Mst"

REM INFO: Package: GeoEnviron
REM INFO: Version: 8.0.1
REM INFO: Description: 
REM INFO: Updated: 20130715
REM INFO: Contact: stephen@cabo.dk
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\GeoEnviron\sqlncli.msi"
call:log_execute msiexec.exe /L*+ %logfile_msi% /passive /i "%software%\GeoEnviron\GeoEnviron-DK-8.0.1.msi" TRANSFORM="%software%\GeoEnviron\GeoEnviron-DK-8.0.1.mst"
call:log_execute regedit.exe /S "%software%\GeoEnviron\GeoEnviron.reg"
REM call:log_execute cmd.exe /C "cscript /nologo %software%\GeoEnviron\GeoEnviron.vbs"



call:logger "Step6 - Finished installing applications"

call:log_execute copy "%software%\_scripts\mac2ip.txt"       c:\cabo\scripts\mac2ip.txt /Y  
call:log_execute copy "%software%\_scripts\template.bat"     c:\cabo\scripts\template.bat /Y  

REM Clean up - remove autostart install job
call:logger "Step6 - Cleaning up"
call:log_execute schtasks /delete /tn citrix-bootstrap-master -f  
call:log_execute del /f "c:\cabo\scripts\_citrix-bootstrap-master.bat"  

REM Remove Print-server roles. (Requires restart)
call:log_execute ServerManagercmd.exe -remove Print-Server >> %logfile_srvmgr%

REM Unjoin from AD
call:logger "Step6 - Unjoin AD"
netdom remove srvctxmaster /Domain:adm.aarhuskommune.dk /UserD:"adm\admincabo" /PasswordD:%1
call:logger "Step6 - Unjoin AD exited with errorlevel: %errorlevel%"

call:log_execute mkdir "c:\cabo\install\masterok"  

REM call:log_execute regedit /s "%software%\cabo\enableUAC.reg" 
REM Re-enable UAC
call:logger "Step6 - Poweroff"
call:log_execute shutdown /s /t 0
goto :EOF

:log_execute
SET _pcmd=%*

echo "%date% %time% - Executing: %_pcmd%" >> %logfile_progress%
%_pcmd% >> %logfile_progress% 2>&1
echo "%date% %time% - StatusCode: %ErrorLevel%" >> %logfile_progress%
echo "Cmd: %_pcmd% _ StatusCode: %ErrorLevel%" | %syslog%

REM Wait 5s to make sure we are ready to install next msi.
ping -n 3 1.1.1.1 -w 1 > NUL
echo "--------------------" >> %logfile_progress%

goto :EOF
:logger
SET _msg=%*

echo "%date% %time% - %_msg%" >> %logfile_progress%
echo "Status: %_msg%" | %syslog%

:EOF
