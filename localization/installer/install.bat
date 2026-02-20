@echo off
chcp 65001 >nul
echo ====================================================
echo   Pokémon Opalo 繁體中文化補丁 - 安裝腳本
echo   版本: 2.11
echo ====================================================
echo.

:: 確認當前目錄或尋找遊戲目錄
set "GAME_DIR=%~dp0"
:: 移除末尾反斜線
if "%GAME_DIR:~-1%"=="\" set "GAME_DIR=%GAME_DIR:~0,-1%"

:: 判斷 patches 資料夾位置
set "PATCH_DIR="
if exist "%GAME_DIR%\patches" (
    set "PATCH_DIR=%GAME_DIR%\patches"
) else if exist "%~dp0..\..\patches" (
    set "PATCH_DIR=%~dp0..\..\patches"
    :: 如果從 localization\installer 執行，遊戲目錄是上兩層
    pushd "%~dp0..\.."
    set "GAME_DIR=!CD!"
    popd
)

:: 啟用延遲展開
setlocal EnableDelayedExpansion

:: 重新判斷路徑（延遲展開後）
set "GAME_DIR=%~dp0"
if "%GAME_DIR:~-1%"=="\" set "GAME_DIR=%GAME_DIR:~0,-1%"

set "PATCH_DIR="
if exist "%GAME_DIR%\patches" (
    set "PATCH_DIR=%GAME_DIR%\patches"
) else if exist "%~dp0..\..\patches" (
    set "PATCH_DIR=%~dp0..\..\patches"
    pushd "%~dp0..\.."
    set "GAME_DIR=!CD!"
    popd
)

:: 檢查 patches 資料夾
if not defined PATCH_DIR (
    echo [錯誤] 找不到 patches 資料夾！
    echo.
    echo 請確認以下其中一種方式：
    echo   1. 將此腳本放在遊戲目錄中，且 patches 資料夾也在同一目錄
    echo   2. 從專案的 localization\installer\ 目錄執行此腳本
    echo.
    pause
    exit /b 1
)

:: 驗證遊戲目錄
if not exist "!GAME_DIR!\Game.exe" (
    echo [錯誤] 在 !GAME_DIR! 中找不到 Game.exe
    echo 請確認此目錄是 Pokémon Opalo 的遊戲安裝目錄。
    echo.
    pause
    exit /b 1
)

:: 檢查 patches 目錄是否有檔案
dir /b "!PATCH_DIR!\*" 2>nul | findstr /v /i ".gitkeep" >nul
if !errorlevel! neq 0 (
    echo [錯誤] patches 資料夾中沒有補丁檔案！
    echo 請先執行翻譯打包流程產生補丁檔案。
    echo.
    pause
    exit /b 1
)

set "DATA_DIR=!GAME_DIR!\Data"
set "BACKUP_DIR=!DATA_DIR!\backup"

echo 遊戲目錄: !GAME_DIR!
echo 補丁來源: !PATCH_DIR!
echo.

:: 確認安裝
echo [警告] 此操作將修改遊戲的 Data 資料夾。
echo 原始檔案將備份至 Data\backup\ 資料夾。
echo.
set /p "CONFIRM=是否繼續安裝？(Y/N): "
if /i not "!CONFIRM!"=="Y" (
    echo 安裝已取消。
    pause
    exit /b 0
)

echo.
echo ── 步驟 1/3：建立備份 ──
echo.

:: 建立備份目錄
if not exist "!BACKUP_DIR!" (
    mkdir "!BACKUP_DIR!"
    echo 已建立備份目錄: !BACKUP_DIR!
)

:: 備份即將被覆蓋的檔案
set "BACKUP_COUNT=0"
for %%F in ("!PATCH_DIR!\*") do (
    set "FNAME=%%~nxF"
    if /i not "!FNAME!"==".gitkeep" (
        if exist "!DATA_DIR!\!FNAME!" (
            if not exist "!BACKUP_DIR!\!FNAME!" (
                copy /y "!DATA_DIR!\!FNAME!" "!BACKUP_DIR!\!FNAME!" >nul
                set /a "BACKUP_COUNT+=1"
            )
        )
    )
)
echo 已備份 !BACKUP_COUNT! 個檔案。

echo.
echo ── 步驟 2/3：安裝中文化補丁 ──
echo.

:: 複製補丁檔案
set "PATCH_COUNT=0"
for %%F in ("!PATCH_DIR!\*") do (
    set "FNAME=%%~nxF"
    if /i not "!FNAME!"==".gitkeep" (
        copy /y "%%F" "!DATA_DIR!\!FNAME!" >nul
        set /a "PATCH_COUNT+=1"
        echo   已安裝: !FNAME!
    )
)

:: 處理子目錄
for /d %%D in ("!PATCH_DIR!\*") do (
    set "DNAME=%%~nxD"
    if not exist "!DATA_DIR!\!DNAME!" mkdir "!DATA_DIR!\!DNAME!"
    xcopy /y /e /q "%%D\*" "!DATA_DIR!\!DNAME!\" >nul 2>nul
)

echo.
echo 已安裝 !PATCH_COUNT! 個補丁檔案。

echo.
echo ── 步驟 3/3：驗證安裝 ──
echo.

:: 簡單驗證
set "VERIFY_OK=1"
for %%F in ("!PATCH_DIR!\*") do (
    set "FNAME=%%~nxF"
    if /i not "!FNAME!"==".gitkeep" (
        if not exist "!DATA_DIR!\!FNAME!" (
            echo [警告] 檔案未成功安裝: !FNAME!
            set "VERIFY_OK=0"
        )
    )
)

if "!VERIFY_OK!"=="1" (
    echo 所有檔案驗證通過！
)

echo.
echo ====================================================
echo   安裝完成！
echo   您現在可以啟動遊戲體驗中文化內容。
echo.
echo   如需還原，請執行 uninstall.bat
echo   或將 Data\backup\ 中的檔案複製回 Data\
echo ====================================================
echo.
pause
