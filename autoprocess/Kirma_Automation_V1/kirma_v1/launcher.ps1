$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $base

function Find-Python {
    $candidates = @('python','py')
    foreach ($c in $candidates) {
        try {
            $cmd = Get-Command $c -ErrorAction Stop
            if ($cmd) { return $c }
        } catch {}
    }
    return $null
}

$python = Find-Python
if (-not $python) {
    try {
        $winget = Get-Command winget -ErrorAction Stop
        & winget install --id Python.Python.3.13 -e --accept-source-agreements --accept-package-agreements --silent
        Start-Sleep -Seconds 3
        $python = Find-Python
    } catch {}
}

if (-not $python) {
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show('No se encontró Python y Windows no permitió instalarlo automáticamente. Instale Python 3 y vuelva a ejecutar INICIAR_KIRMA.bat.', 'KIRMA Automation') | Out-Null
    exit 1
}

& $python -m pip install --disable-pip-version-check --no-warn-script-location -q psutil
if ($LASTEXITCODE -ne 0) {
    Add-Type -AssemblyName PresentationFramework
    [System.Windows.MessageBox]::Show('No fue posible preparar la dependencia psutil.', 'KIRMA Automation') | Out-Null
    exit 2
}

Start-Process -FilePath $python -ArgumentList ('"' + (Join-Path $base 'kirma_automation_v1.py') + '"') -WorkingDirectory $base -WindowStyle Hidden
exit 0
