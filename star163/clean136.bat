@echo off

@TASKKILL>nul /FI "IMAGENAME eq NemuBooter.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq NemuPlayer.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq NemuSVC.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq NemuHeadless.exe"  /F /T


rem @TASKKILL>nul /FI "IMAGENAME eq Appium.exe"  /F /T
rem @TASKKILL>nul /FI "IMAGENAME eq Node.exe"  /F /T
rem @TASKKILL>nul /FI "IMAGENAME eq adb.exe"  /F /T



rem for /f "tokens=2 " %%a in ('tasklist  /fi "imagename eq NemuSVC.exe" /nh') do taskkill /F /T /pid %a



