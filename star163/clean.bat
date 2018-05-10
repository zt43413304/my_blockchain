@echo off




@TASKKILL>nul /FI "IMAGENAME eq NemuBooter.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq NemuPlayer.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq NemuSVC.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq NemuHeadless.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq Appium.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq Node.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq adb.exe"  /F /T

echo ****** %date% %time%
echo ****** kill process success.


for /f "tokens=2 " %%a in ('tasklist  /fi "imagename eq NemuSVC.exe" /nh') do taskkill /F /T /pid %a
for /f "tokens=2 " %%a in ('tasklist  /fi "imagename eq NemuHeadless.exe" /nh') do taskkill /F /T /pid %a
for /f "tokens=2 " %%a in ('tasklist  /fi "imagename eq NemuBooter.exe" /nh') do taskkill /F /T /pid %a
for /f "tokens=2 " %%a in ('tasklist  /fi "imagename eq NemuPlayer.exe" /nh') do taskkill /F /T /pid %a
for /f "tokens=2 " %%a in ('tasklist  /fi "imagename eq Appium.exe" /nh') do taskkill /F /T /pid %a
for /f "tokens=2 " %%a in ('tasklist  /fi "imagename eq Node.exe" /nh') do taskkill /F /T /pid %a
for /f "tokens=2 " %%a in ('tasklist  /fi "imagename eq adb.exe" /nh') do taskkill /F /T /pid %a


