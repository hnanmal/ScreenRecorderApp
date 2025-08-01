[Setup]
AppName=크롭영역녹화기
AppVersion=1.0
DefaultDirName={pf}\크롭영역녹화기
DefaultGroupName=크롭영역녹화기
OutputDir=installer
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
; SetupIconFile=resources\app_icon.ico  ; ← 스크립트 파일 기준 상대경로 확인 필요

[Files]
Source: "dist\main\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "resources\*"; DestDir: "{app}\resources"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\main\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\크롭영역녹화기"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
Name: "{group}\프로그램 제거"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\main.exe"; Description: "크롭영역녹화기 실행"; Flags: nowait postinstall skipifsilent
