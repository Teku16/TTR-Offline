@echo off

rem Define some constants for our AI server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7199
set EVENTLOGGER_IP=127.0.0.1:7197
set /P PPYTHON_PATH=<config/PPYTHON_PATH
set /P MONGODB_PATH=<config/MONGODB_PATH

rem Get the user input:
set /P DISTRICT_NAME="District name (DEFAULT: Sillyville): " || ^
set DISTRICT_NAME=Sillyville
set /P BASE_CHANNEL="Base channel (DEFAULT: 401000000): " || ^
set BASE_CHANNEL=401000000

title %DISTRICT_NAME% %BASE_CHANNEL%

echo ===============================
echo Starting Toontown Rewritten AI server...
echo PPYTHON_PATH: %PPYTHON_PATH%
echo MONGODB_PATH: %MONGODB_PATH%
echo District name: %DISTRICT_NAME%
echo Base channel: %BASE_CHANNEL%
echo Max channels: %MAX_CHANNELS%
echo State Server: %STATESERVER%
echo Astron IP: %ASTRON_IP%
echo Event Logger IP: %EVENTLOGGER_IP%
echo ===============================

:main
%PPYTHON_PATH% -m toontown.ai.ServiceStart --base-channel %BASE_CHANNEL% ^
               --max-channels %MAX_CHANNELS% --stateserver %STATESERVER% ^
               --astron-ip %ASTRON_IP% --eventlogger-ip %EVENTLOGGER_IP% ^
               --district-name "%DISTRICT_NAME%"
goto main
