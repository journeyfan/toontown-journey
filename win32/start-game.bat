@echo off
cd ../

title Toontown Game Launcher

set TTI_GAMESERVER=localhost
set /P TTI_PLAYCOOKIE=Username:

echo Starting Toontown...

:main
C:/Panda3D-1.11.0-x64-py2/python/python.exe -m toontown.toonbase.ClientStart
pause
goto main