@echo off

echo ****** %date% %time%

echo ****** checkout latest code......

echo=

rem git checkout . && git clean -df

git pull origin

start cmd /k "cd C:/DevTools/my_blockchain && python.exe start_lenovo.py"

