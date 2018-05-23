@echo off

@TASKKILL>nul /FI "IMAGENAME eq python.exe"  /F /T
@TASKLIST>nul /FI "WINDOWTITLE eq OneChainCheck" /FI "IMAGENAME eq cmd.exe" ||exit
@TASKKILL>nul /FI "WINDOWTITLE eq OneChainCheck" /FI "IMAGENAME eq cmd.exe"  /F /T 

echo ****** %date% %time%
echo ****** kill process success.



