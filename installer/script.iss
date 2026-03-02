; Script otimizado para Ponto AMAN
#define MyAppName "Ponto AMAN"
#define MyAppVersion "1.0"
#define MyAppPublisher "ZeldrisMercy"
#define MyAppURL "https://www.example.com/"
#define MyAppExeName "Ponto AMAN.exe"
#define MyAppAssocName MyAppName + " File"
#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
AppId={{1853B4BA-C520-452B-9A85-59DC3652F67D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
ChangesAssociations=yes
DisableProgramGroupPage=yes
; Define o ícone do instalador (o arquivo .exe gerado pelo Inno)
SetupIconFile="C:\Users\icaro\OneDrive\Documentos\Python App\dist\app_ponto\_internal\logo.ico"
; Define o ícone que aparece no "Adicionar ou Remover Programas"
UninstallDisplayIcon={app}\_internal\logo.ico
OutputDir=C:\Users\icaro\OneDrive\Documentos\Python App\APP
OutputBaseFilename=mysetup
SolidCompression=yes
WizardStyle=modern dark windows11
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
; Recomendado para instalar em Program Files sem erros de permissão
PrivilegesRequired=admin

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; O executável principal
Source: "C:\Users\icaro\OneDrive\Documentos\Python App\dist\app_ponto\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; A pasta _internal e TODO o seu conteúdo (DLLs, PyDs, etc) mantendo a estrutura
Source: "C:\Users\icaro\OneDrive\Documentos\Python App\dist\app_ponto\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\_internal\logo.ico"
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\_internal\logo.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\_internal\logo.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
