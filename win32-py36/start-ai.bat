@echo off
cd ..

rem Define some constants for our AI server:
set MAX_CHANNELS=999999
set STATESERVER=4002
set ASTRON_IP=127.0.0.1:7100
set EVENTLOGGER_IP=127.0.0.1:7198

rem Get the user input:
set /P DISTRICT_NAME="District name (DEFAULT: Nuttyboro): " || ^
set DISTRICT_NAME=Nuttyboro
set /P BASE_CHANNEL="Base channel (DEFAULT: 401000000): " || ^
set BASE_CHANNEL=401000000

echo Starting AI...

:main
C:/Panda3D-1.11.0-x64-py36/python/python.exe ^
	-m toontown.ai.ServiceStart ^
	--base-channel %BASE_CHANNEL% ^
	--max-channels %MAX_CHANNELS% ^
	--stateserver %STATESERVER% ^
	--astron-ip %ASTRON_IP% ^
	--eventlogger-ip %EVENTLOGGER_IP% ^
	--district-name "%DISTRICT_NAME%"
goto main