$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
Set-Location -LiteralPath $projectRoot
New-Item -ItemType Directory -Force -Path 'data/tmp' | Out-Null
$env:TEMP = Join-Path $projectRoot 'data/tmp'
$env:TMP = $env:TEMP
try {
    if (-not (Get-Command node -ErrorAction SilentlyContinue)) { throw 'Install Node.js 22.12+ (or 24 LTS) from https://nodejs.org/ and run setup again.' }
    $nodeVersion = [version]((& node --version).Trim().TrimStart('v'))
    if ($nodeVersion -lt [version]'22.12.0') { throw 'Node.js 22.12+ is required.' }
    $pythonCommand = if (Test-Path '.venv/Scripts/python.exe') { (Resolve-Path '.venv/Scripts/python.exe').Path } elseif (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Install Python 3.12+ from https://www.python.org/downloads/windows/ and enable Add to PATH.' }
    [string[]]$pythonArgs = @()
    if ($pythonCommand -eq 'py') { $pythonArgs = @('-3') }
    & $pythonCommand @pythonArgs -c 'import sys; sys.exit(0 if sys.version_info >= (3,12) else 1)'
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.12+ is required.' }
    if (-not (Test-Path '.venv/Scripts/python.exe')) {
        & $pythonCommand @pythonArgs -m venv .venv
        if ($LASTEXITCODE -ne 0) { throw 'Could not create Python virtual environment.' }
    }
    & '.\.venv\Scripts\python.exe' -m pip install --upgrade 'pip>=26.2,<27'
    if ($LASTEXITCODE -ne 0) { throw 'pip update failed.' }
    & '.\.venv\Scripts\python.exe' -m pip install -r backend/requirements.txt -r desktop/requirements.txt
    if ($LASTEXITCODE -ne 0) { throw 'Python dependencies installation failed.' }
    Push-Location frontend
    try {
        & npm.cmd ci
        if ($LASTEXITCODE -ne 0) { throw 'npm ci failed. Check your internet connection.' }
        & npm.cmd run build
        if ($LASTEXITCODE -ne 0) { throw 'Frontend build failed.' }
    } finally { Pop-Location }
    Write-Host 'DevForge is ready. All required runtime assets are local.' -ForegroundColor Green
} catch {
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
