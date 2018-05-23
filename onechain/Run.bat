@echo off

:start

@TASKKILL>nul /FI "IMAGENAME eq python.exe"  /F /T
@TASKLIST>nul /FI "WINDOWTITLE eq OneChainCheck" /FI "IMAGENAME eq cmd.exe" ||exit
@TASKKILL>nul /FI "WINDOWTITLE eq OneChainCheck" /FI "IMAGENAME eq cmd.exe"  /F /T 

echo ****** %date% %time%
echo ****** kill process success.

call OneChainCheck.bat
echo ****** start OneChainCheck

echo=

choice /t 9999 /d y /n >nul
goto start

