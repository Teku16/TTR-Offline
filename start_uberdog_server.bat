@echo off

rem Define some constants for our UberDOG server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENTLOGGER_IP=127.0.0.1:7197
set BASE_CHANNEL=1000000
set /P PPYTHON_PATH=<config/PPYTHON_PATH
set /P MONGODB_PATH=<config/MONGODB_PATH

title UberDOG %BASE_CHANNEL%

echo ===============================
echo Starting Toontown Rewritten UberDOG server...
echo PPYTHON_PATH: %PPYTHON_PATH%
echo MONGODB_PATH: %MONGODB_PATH%
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATESERVER%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

:main
%PPYTHON_PATH% -m toontown.uberdog.ServiceStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATESERVER% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENTLOGGER_IP%
goto main
