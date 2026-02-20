; ============================================================
; Pokémon Opalo 繁體中文化補丁 - Inno Setup 安裝腳本
; 版本: 2.11
; ============================================================

#define MyAppName "Pokémon Opalo 繁體中文化補丁"
#define MyAppVersion "2.11"
#define MyAppPublisher "Pokémon Opalo 中文化專案"
#define MyAppURL "https://github.com/nagaoyuchiun/pokemon-opalo-zh-tw"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppSupportURL={#MyAppURL}
DefaultDirName={autopf}\Pokemon Opalo
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
DisableStartupPrompt=yes
; 不建立程式群組或桌面捷徑
CreateAppDir=no
LicenseFile=LICENSE.txt
InfoAfterFile=README.txt
OutputDir=output
OutputBaseFilename=PokemonOpalo_zhTW_Patch_v{#MyAppVersion}
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
; 以管理員權限執行（避免權限問題）
PrivilegesRequired=lowest

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Messages]
; 自訂繁體中文訊息（覆蓋簡體中文翻譯）
WelcomeLabel1=歡迎使用 {#MyAppName} 安裝精靈
WelcomeLabel2=本程式將安裝 Pokémon Opalo V{#MyAppVersion} 的繁體中文化補丁。%n%n請在下一步選擇您的遊戲安裝目錄。%n%n建議在安裝前關閉遊戲。
SelectDirLabel3=請選擇 Pokémon Opalo 的遊戲安裝目錄（包含 Game.exe 的資料夾）：
SelectDirBrowseLabel=點擊「瀏覽」選擇遊戲目錄，然後點擊「下一步」繼續。
FinishedHeadingLabel=安裝完成
FinishedLabel={#MyAppName} 已成功安裝。%n%n您現在可以啟動遊戲體驗中文化內容。%n%n如需還原，請執行遊戲目錄中 Data\backup 資料夾的還原操作。

[Types]
Name: "full"; Description: "完整安裝（推薦）"

[Components]
Name: "patch"; Description: "中文化補丁檔案"; Types: full; Flags: fixed

[Files]
; 安裝中文化補丁檔案到遊戲的 Data 目錄
Source: "..\..\patches\*"; DestDir: "{app}\Data"; Components: patch; Flags: ignoreversion recursesubdirs createallsubdirs

[Code]
var
  GameDirPage: TInputDirWizardPage;

// 驗證使用者選擇的目錄是否為有效的遊戲目錄
function IsValidGameDir(Path: String): Boolean;
begin
  Result := FileExists(Path + '\Game.exe') or FileExists(Path + '\game.exe');
end;

procedure InitializeWizard;
begin
  // 建立自訂遊戲目錄選擇頁面
  GameDirPage := CreateInputDirPage(wpWelcome,
    '選擇遊戲目錄',
    '請選擇 Pokémon Opalo 的安裝目錄',
    '請選擇包含 Game.exe 的遊戲資料夾，然後點擊「下一步」。',
    False, '');
  GameDirPage.Add('');
  GameDirPage.Values[0] := ExpandConstant('{src}');
end;

function NextButtonClick(CurPageID: Integer): Boolean;
var
  GameDir: String;
begin
  Result := True;
  if CurPageID = GameDirPage.ID then
  begin
    GameDir := GameDirPage.Values[0];
    if not IsValidGameDir(GameDir) then
    begin
      MsgBox('在指定的目錄中找不到 Game.exe。' + #13#10 +
             '請選擇包含 Game.exe 的 Pokémon Opalo 遊戲目錄。',
             mbError, MB_OK);
      Result := False;
    end;
  end;
end;

// 取得使用者選擇的遊戲目錄
function GetGameDir(Param: String): String;
begin
  Result := GameDirPage.Values[0];
end;

// 備份原始 Data 目錄
procedure BackupOriginalFiles;
var
  GameDir, DataDir, BackupDir: String;
  FindRec: TFindRec;
begin
  GameDir := GameDirPage.Values[0];
  DataDir := GameDir + '\Data';
  BackupDir := DataDir + '\backup';

  // 建立備份目錄
  if not DirExists(BackupDir) then
    ForceDirectories(BackupDir);

  // 備份 Data 目錄中的檔案
  if FindFirst(DataDir + '\*', FindRec) then
  begin
    try
      repeat
        // 跳過目錄和備份資料夾本身
        if (FindRec.Name <> '.') and (FindRec.Name <> '..') and
           (FindRec.Name <> 'backup') and
           (FindRec.Attributes and FILE_ATTRIBUTE_DIRECTORY = 0) then
        begin
          FileCopy(DataDir + '\' + FindRec.Name,
                   BackupDir + '\' + FindRec.Name, False);
        end;
      until not FindNext(FindRec);
    finally
      FindClose(FindRec);
    end;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssInstall then
  begin
    // 安裝前備份原始檔案
    BackupOriginalFiles;
  end;
end;

// 覆蓋安裝目錄為使用者選擇的遊戲目錄
function UpdateReadyMemo(Space, NewLine, MemoUserInfoInfo, MemoDirInfo,
  MemoTypeInfo, MemoComponentsInfo, MemoGroupInfo, MemoTasksInfo: String): String;
begin
  Result := '遊戲目錄：' + NewLine +
            Space + GameDirPage.Values[0] + NewLine + NewLine +
            '將執行以下操作：' + NewLine +
            Space + '1. 備份原始 Data 資料夾至 Data\backup\' + NewLine +
            Space + '2. 安裝繁體中文化補丁至 Data\' + NewLine;
end;
