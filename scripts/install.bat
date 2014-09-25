@setlocal EnableDelayedExpansion

set TASK="RDS Install Task"
set STEP=1
set STEP_STATUS_DIR=%SystemRoot%\Temp\rds_install
set STEP_STATUS=%STEP_STATUS_DIR%\step%STEP%

echo %STEP_STATUS%

:next_loop
if exist "%STEP_STATUS%" (
  set /A STEP=!STEP! + 1
  set STEP_STATUS=%STEP_STATUS_DIR%\step!STEP!
  goto :next_loop
) else (
  mkdir %STEP_STATUS%
  goto :step!STEP!
)


:step1
schtasks /create /tn %TASK% /tr "%~dp0install.bat" /sc onlogon
powershell -File %~dp0install-ad.ps1
goto :reboot 

:step2
powershell -File %~dp0ad-add-forest.ps1
goto :reboot 

:step3

echo "RDS deployment doesn't work:-(. Go install RDS in server manager:-("
powershell -File %~dp0rds-add-deployment.ps1
pause
call :join
goto :finish

:step4
powershell -File %~dp0rds-add-collection.ps1

:join
:: Create scheduled task for reporting IP
:: Reports back every min, stops on first success
join-task.bat

:reboot
pause
shutdown /r /t 5 /f /c "Installing RDS - Step %STEP% Finished"
goto :eof

:finish
echo "Install Finished - Deleting Scheduled Task"
schtasks /delete /tn %TASK% -f
deltree %STEP_STATUS_DIR%
