@echo off
cd ../

title Toontown Game Launcher

set TTI_GAMESERVER=192.99.167.158
set /P username="Username:"
set /P password="Password:"
set TTI_PLAYCOOKIE=%username%:%password%
echo %TTI_PLAYCOOKIE%
echo Starting Toontown...

:main
C:/Panda3D-1.11.0-x64-py2/python/python.exe -m toontown.toonbase.ClientStart
pause
goto main