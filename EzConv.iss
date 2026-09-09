; Inno Setup script for EzConv
; Currency Converter Application

[Setup]
; App identification
AppId={{EzConv-1A2B3C4D-5E6F-7G8H-9I0J-1K2L3M4N5O6P}
AppName=EzConv
AppVersion=0.1.0
AppPublisher=EzConv Team
AppPublisherURL=https://github.com/EzConv
AppSupportURL=https://github.com/EzConv/issues
AppUpdatesURL=https://github.com/EzConv/releases
VersionInfoVersion=0.1.0
VersionInfoCompany=EzConv Team
VersionInfoProductName=EzConv
VersionInfoProductVersion=0.1.0
VersionInfoLanguage=1033
VersionInfoCopyright=Copyright (C) 2026 EzConv Team
VersionInfoProductVersion=0.1.0

; Directories
DefaultDirName={pf}\EzConv
CreateAppDir=False
DisableProgramGroupPage=no

; Compression
Compression=lzma
SolidCompression=yes
OutputDir=Output
OutputExeName=EzConv_Setup.exe

; Architecture (64-bit only)
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=yes

; Icons
IconFile=bitcoin.ico

; Privileges
PrivilegesRequired=none

; Uninstall
Uninstallable=yes
UninstallIconIconFile={app}\EzConv.exe

; Languages
Languages=english

[Files]
Source: "dist\EzConv\EzConv.exe"; DestDir: "{app}"
Source: "dist\EzConv\_internal\*"; DestDir: "{app}\_internal"; Flags: recursedirs ignoreversion
Source: "bitcoin.ico"; DestDir: "{app}"

[Icons]
Name: "{group}\EzConv"; Filename: "{app}\EzConv.exe"; IconFilename: "{app}\EzConv.exe"
Name: "{commondesktop}\EzConv"; Filename: "{app}\EzConv.exe"; IconFilename: "{app}\EzConv.exe"; IconIndex:0; Tasks: desktopicon
Name: "{group}\Uninstall {AppName}"; Filename: "{uninstallexe}"; IconFilename: "{uninstallexe}"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Registry]
Root: HKCU; Subkey: "Software\EzConv"; ValueName: "Installed"; ValueData: "1"

[Code]
procedure InitializeWizard;
begin
  WizardForm.Caption := 'EzConv Setup';
  WizardForm.Description.Caption := 'EzConv - Currency Converter' + #13#10 + 'Version 0.1.0';
end;

function InitializeSetup: Boolean;
begin
  Result := True;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  if CurUninstallStep = usUninstall then
  begin
    DeleteFile('{app}\last_values.txt');
  end;
end;