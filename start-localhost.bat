@echo off

rem Read the contents of PPYTHON_PATH into %PPYTHON_PATH%:
set /P PPYTHON_PATH=<config/PPYTHON_PATH

rem Get the user input:
set /P ttrUsername="Username: "

rem Export the environment variables:
set ttrPassword=password
set TTR_PLAYCOOKIE=%ttrUsername%
set TTR_GAMESERVER=127.0.0.1

echo ===============================
echo Starting Toontown Rewritten...
echo ppython: %PPYTHON_PATH%
echo Username: %ttrUsername%
echo Gameserver: %TTR_GAMESERVER%
echo ===============================

%PPYTHON_PATH% -m toontown.toonbase.ToontownStart
pause
