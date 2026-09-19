@echo off
setlocal
cd /d "%~dp0"
set "PYTHON="
where py >nul 2>nul
if %errorlevel%==0 set "PYTHON=py"
if not defined PYTHON (
 where python >nul 2>nul
 if %errorlevel%==0 set "PYTHON=python"
)
if not defined PYTHON (
 powershell -NoProfile -ExecutionPolicy Bypass -Command "$u=Join-Path $env:TEMP 'python-installer.exe'; Invoke-WebRequest -UseBasicParsing 'https://www.python.org/ftp/python/3.13.7/python-3.13.7-amd64.exe' -OutFile $u; Start-Process $u -ArgumentList '/quiet InstallAllUsers=0 PrependPath=1 Include_test=0' -Wait; Remove-Item $u -Force"
 if exist "%LocalAppData%\Programs\Python\Python313\python.exe" (set "PYTHON=%LocalAppData%\Programs\Python\Python313\python.exe") else exit /b 1
)
%PYTHON% -c "import psutil" >nul 2>nul
if not %errorlevel%==0 %PYTHON% -m pip install --disable-pip-version-check psutil >nul 2>nul
%PYTHON% "%~dp0kirma_automation_v032.py"
exit /b %errorlevel%
