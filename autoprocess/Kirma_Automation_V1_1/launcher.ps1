$ErrorActionPreference = "Stop"
$BaseDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $BaseDir

function Find-Python {
    try {
        $cmd = Get-Command python -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    } catch {}
    try {
        $cmd = Get-Command py -ErrorAction SilentlyContinue
        if ($cmd) { return $cmd.Source }
    } catch {}
    return $null
}

$python = Find-Python
if (-not $python) {
    try {
        $winget = Get-Command winget -ErrorAction SilentlyContinue
        if ($winget) {
            Start-Process -FilePath $winget.Source -ArgumentList 'install --id Python.Python.3.13 -e --accept-source-agreements --accept-package-agreements --silent' -Wait -WindowStyle Hidden
        }
    } catch {}
    $python = Find-Python
}

if (-not $python) {
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show("KIRMA no encontró Python y Windows no permitió instalarlo automáticamente. Instala Python 3 y vuelve a ejecutar INICIAR_KIRMA.bat.", "KIRMA Automation", "OK", "Warning") | Out-Null
    exit 1
}

try {
    & $python -c "import psutil" 2>$null
    if ($LASTEXITCODE -ne 0) {
        & $python -m pip install --disable-pip-version-check --no-input -q psutil
    }
} catch {
    & $python -m pip install --disable-pip-version-check --no-input -q psutil
}

Start-Process -FilePath $python -ArgumentList "`"$BaseDir\kirma_automation_v11.py`"" -WorkingDirectory $BaseDir -WindowStyle Hidden
exit 0
