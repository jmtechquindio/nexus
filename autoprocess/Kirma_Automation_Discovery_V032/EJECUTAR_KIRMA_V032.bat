@echo off
setlocal
cd /d "%~dp0"
title Kirma Automation Discovery V0.3.2

echo ============================================================
echo KIRMA AUTOMATION DISCOVERY V0.3.2
echo ============================================================
echo.

where py >nul 2>nul
if %errorlevel%==0 (
    set "PYTHON=py"
) else (
    where python >nul 2>nul
    if %errorlevel%==0 (
        set "PYTHON=python"
    ) else (
        echo ERROR: Python no esta instalado o no esta en PATH.
        echo Instale Python desde https://www.python.org/downloads/
        echo Marque la opcion "Add Python to PATH" durante la instalacion.
        pause
        exit /b 1
    )
)

echo Comprobando dependencia psutil...
%PYTHON% -c "import psutil" >nul 2>nul
if not %errorlevel%==0 (
    echo psutil no esta instalado. Intentando instalarlo...
    %PYTHON% -m pip install psutil
    if not %errorlevel%==0 (
        echo.
        echo ERROR: No se pudo instalar psutil.
        echo Revise su conexion a Internet o ejecute el instalador de Python.
        pause
        exit /b 1
    )
)

echo.
echo Iniciando Kirma Automation Discovery...
echo.
%PYTHON% "%~dp0kirma_automation_v032.py"

if not %errorlevel%==0 (
    echo.
    echo El programa termino con un error.
    pause
    exit /b 1
)

echo.
echo Proceso finalizado. Revise el archivo registro_pc.txt.
pause
endlocal
