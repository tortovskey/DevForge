param([string]$DistributionDirectory='', [string]$TestDirectory='')
$ErrorActionPreference='Stop'
$sourceRoot=Split-Path $PSScriptRoot -Parent
if(-not $DistributionDirectory){$DistributionDirectory=Join-Path $sourceRoot 'build/distribution'}
if(-not $TestDirectory){$TestDirectory=Join-Path $sourceRoot 'build/installer-verification'}
$TestDirectory=[IO.Path]::GetFullPath($TestDirectory)
if(-not $TestDirectory.StartsWith([IO.Path]::GetFullPath($sourceRoot)+[IO.Path]::DirectorySeparatorChar)){throw 'Test directory must stay inside the workspace'}
New-Item -ItemType Directory -Force -Path $TestDirectory | Out-Null
$results=@()
foreach($edition in @('IDE','Desktop')){
 $key="HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\DevForge.$($edition)_is1"
 if(Test-Path $key){throw "A registered $edition install already exists; its registration will not be touched."}
 $destination=Join-Path $TestDirectory $edition
 $setup=Join-Path $DistributionDirectory "$edition/Setup.exe"
 $exe=if($edition -eq 'IDE'){'DevForgeIDE.exe'}else{'DevForge.exe'}
 foreach($round in 1..2){
   $process=Start-Process -FilePath $setup -ArgumentList @('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART','/NOICONS','/TASKS=',('/DIR="'+$destination+'"'),('/LOG="'+(Join-Path $TestDirectory "$edition-install-$round.log")+'"')) -WindowStyle Hidden -PassThru -Wait
   if($process.ExitCode -ne 0){throw "Setup $edition returned $($process.ExitCode)"}
   if(-not (Test-Path -LiteralPath (Join-Path $destination $exe))){throw "$exe was not installed"}
 }
 $internal=Join-Path $destination '_internal/frontend/dist/forge.svg'
 if(-not (Test-Path -LiteralPath $internal)){throw 'Forge icon is missing in the installed app'}
 $uninstaller=Join-Path $destination 'Uninstall/unins000.exe'
 if(-not (Test-Path -LiteralPath $uninstaller)){throw 'Uninstaller was not created'}
 & (Join-Path $sourceRoot '.venv/Scripts/python.exe') (Join-Path $PSScriptRoot 'verify_native.py') --distribution $TestDirectory --edition $edition
 if($LASTEXITCODE){throw "Installed application did not pass startup verification: $edition"}
 $process=Start-Process -FilePath $uninstaller -ArgumentList @('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART',('/LOG="'+(Join-Path $TestDirectory "$edition-uninstall.log")+'"')) -WindowStyle Hidden -PassThru -Wait
 if($process.ExitCode -ne 0 -or (Test-Path -LiteralPath (Join-Path $destination $exe)) -or (Test-Path $key)){throw "Uninstall verification failed: $edition"}
 $results+=[pscustomobject]@{edition=$edition;install='passed';upgrade='passed';uninstall='passed'}
}
$results|ConvertTo-Json|Set-Content -LiteralPath (Join-Path $TestDirectory 'report.json') -Encoding UTF8
$results|Format-Table -AutoSize
