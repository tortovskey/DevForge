#ifndef Edition
  #define Edition "IDE"
#endif
#ifndef AppSource
  #error AppSource is required
#endif
#ifndef OutputPath
  #error OutputPath is required
#endif
#ifndef BrandPath
  #error BrandPath is required
#endif
#if Edition == "IDE"
  #define ExeName "DevForgeIDE.exe"
#else
  #define ExeName "DevForge.exe"
#endif

[Setup]
AppId=DevForge.{#Edition}
AppName=DevForge {#Edition}
AppVersion=1.0.0
AppPublisher=DevForge
AppPublisherURL=https://github.com/tortovskey/DevForge
AppSupportURL=https://github.com/tortovskey/DevForge/issues
LicenseFile={#AppSource}\LICENSE
AppCopyright=DevForge
DefaultDirName={localappdata}\Programs\DevForge{#Edition}
DefaultGroupName=DevForge {#Edition}
DisableProgramGroupPage=yes
DisableDirPage=no
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0.17763
WizardStyle=modern
SetupIconFile={#BrandPath}\forge.ico
UninstallDisplayIcon={app}\forge.ico
UninstallDisplayName=DevForge {#Edition}
UninstallFilesDir={app}\Uninstall
OutputDir={#OutputPath}
OutputBaseFilename=Setup
Compression=lzma2/normal
SolidCompression=yes
LZMADictionarySize=8192
LZMANumBlockThreads=1
CloseApplications=yes
RestartApplications=no
SetupMutex=DevForge.Setup.{#Edition}
AppMutex=Local\DevForge.{#Edition}
VersionInfoVersion=1.0.0.0
VersionInfoProductName=DevForge {#Edition}
VersionInfoDescription=DevForge {#Edition} Setup
ChangesAssociations=no
UsePreviousAppDir=yes

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "{#AppSource}\{#ExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#AppSource}\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#BrandPath}\forge.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#AppSource}\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#AppSource}\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#AppSource}\licenses\*"; DestDir: "{app}\licenses"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#BrandPath}\prerequisites\WebView2Bootstrapper.exe"; DestDir: "{tmp}"; Flags: deleteafterinstall; Check: NeedsWebView2

[Icons]
Name: "{group}\DevForge {#Edition}"; Filename: "{app}\{#ExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\forge.ico"
Name: "{autodesktop}\DevForge {#Edition}"; Filename: "{app}\{#ExeName}"; WorkingDir: "{app}"; IconFilename: "{app}\forge.ico"; Tasks: desktopicon
Name: "{group}\{cm:UninstallProgram,DevForge {#Edition}}"; Filename: "{uninstallexe}"

[Run]
Filename: "{tmp}\WebView2Bootstrapper.exe"; Parameters: "/silent /install"; StatusMsg: "Microsoft Edge WebView2 Runtime…"; Flags: waituntilterminated runhidden; Check: NeedsWebView2
Filename: "{app}\{#ExeName}"; Description: "{cm:LaunchProgram,DevForge {#Edition}}"; Flags: nowait postinstall skipifsilent

[Code]
function NeedsWebView2(): Boolean;
var Version: String;
begin
  Result := not (RegQueryStringValue(HKLM32, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version) or
    RegQueryStringValue(HKCU, 'SOFTWARE\Microsoft\EdgeUpdate\Clients\{F3017226-FE2A-4295-8BDF-00C3A9A7E4C5}', 'pv', Version));
end;

