@echo off

@TASKKILL>nul /FI "IMAGENAME eq NoxVMSVC.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq NoxVMHandle.exe"  /F /T
@TASKKILL>nul /FI "IMAGENAME eq Nox.exe"  /F /T






