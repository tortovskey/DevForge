param([string]$OutputDirectory='', [string]$InnoCompiler='', [switch]$SkipFrontend, [ValidateSet('IDE','Desktop')][string[]]$Editions=@('IDE','Desktop'))
$ErrorActionPreference='Stop'
$sourceRoot=Split-Path $PSScriptRoot -Parent
if(-not $OutputDirectory){$OutputDirectory=Join-Path $sourceRoot 'build/distribution'}
if(-not $InnoCompiler){$InnoCompiler=Join-Path $sourceRoot 'build/tools/inno/ISCC.exe'}
if(-not (Test-Path -LiteralPath $InnoCompiler)){throw 'Inno Setup compiler not found. Install Inno Setup and pass -InnoCompiler with the full path to ISCC.exe.'}
$OutputDirectory=[IO.Path]::GetFullPath($OutputDirectory)
$pythonExe=Join-Path $sourceRoot '.venv/Scripts/python.exe'
Push-Location -LiteralPath $sourceRoot
try{
 $bootstrap=Join-Path $sourceRoot 'assets/prerequisites/WebView2Bootstrapper.exe'
 if(-not (Test-Path -LiteralPath $bootstrap)){
   New-Item -ItemType Directory -Force (Split-Path $bootstrap -Parent) | Out-Null
   Invoke-WebRequest 'https://go.microsoft.com/fwlink/p/?LinkId=2124703' -OutFile $bootstrap
 }
 $signature=Get-AuthenticodeSignature -LiteralPath $bootstrap
 if($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'O=Microsoft Corporation'){
   throw 'WebView2 prerequisite must have a valid Microsoft signature.'
 }
 if(-not $SkipFrontend){Push-Location frontend;try{npm run build;if($LASTEXITCODE){throw 'Frontend build failed'}}finally{Pop-Location}}
 & $pythonExe scripts/generate_brand.py
 if($LASTEXITCODE){throw 'Brand assets failed'}
 New-Item -ItemType Directory -Force $OutputDirectory | Out-Null
 $common=@('--noconfirm','--onedir','--distpath',(Join-Path $sourceRoot 'build/native'),'--workpath',(Join-Path $sourceRoot 'build/native-work'),'--specpath',(Join-Path $sourceRoot 'build/native-spec'),'--paths',(Join-Path $sourceRoot 'backend'),'--add-data',((Join-Path $sourceRoot 'content')+';content'),'--add-data',((Join-Path $sourceRoot 'frontend/dist')+';frontend/dist'),'--add-data',((Join-Path $sourceRoot 'assets')+';assets'),'--icon',(Join-Path $sourceRoot 'assets/forge.ico'),'--version-file',(Join-Path $sourceRoot 'assets/windows-version.txt'),'--collect-submodules','uvicorn')
 $guiBuilt=$false
 foreach($edition in $Editions){
   $name=if($edition -eq 'IDE'){'DevForgeIDE'}else{'DevForge'}
   $binary='DevForgeGUI'
   if(-not $guiBuilt){
     & $pythonExe -m PyInstaller @common --windowed --name $binary backend/gui_launcher.py
     if($LASTEXITCODE){throw "Native build failed: $edition"}
     $guiBuilt=$true
   }
   $destination=Join-Path $OutputDirectory $edition
   New-Item -ItemType Directory -Force $destination | Out-Null
   Copy-Item -LiteralPath (Join-Path $sourceRoot "build/native/$binary/_internal") -Destination $destination -Recurse -Force
   Copy-Item -LiteralPath (Join-Path $sourceRoot "build/native/$binary/$binary.exe") -Destination (Join-Path $destination "$name.exe") -Force
   Copy-Item -LiteralPath (Join-Path $sourceRoot 'assets/forge.ico') -Destination $destination -Force
   Copy-Item -LiteralPath (Join-Path $sourceRoot 'licenses') -Destination $destination -Recurse -Force
   $description=if($edition -eq 'IDE'){'Редактор кода без учебных разделов. Запуск: DevForgeIDE.exe. Установка: Setup.exe.'}else{'Обучение и IDE в отдельном окне. Запуск: DevForge.exe. Установка: Setup.exe.'}
   Set-Content -LiteralPath (Join-Path $destination 'README.md') -Encoding UTF8 -Value "# DevForge $edition 1.0.1`n`n$description`n`nWindows 10/11 x64. Данные хранятся в LocalAppData отдельно от программы и сохраняются при удалении.`n`nЛицензия MIT; исходники: https://github.com/tortovskey/DevForge`n"
   Copy-Item -LiteralPath (Join-Path $sourceRoot '../../LICENSE') -Destination $destination -Force
   & $InnoCompiler "/DEdition=$edition" "/DAppSource=$destination" "/DOutputPath=$destination" "/DBrandPath=$(Join-Path $sourceRoot 'assets')" (Join-Path $PSScriptRoot 'windows-setup.iss')
   if($LASTEXITCODE){throw "Setup compilation failed: $edition"}
 }
 Write-Host "Deliverables ready: $OutputDirectory"
}finally{Pop-Location}
