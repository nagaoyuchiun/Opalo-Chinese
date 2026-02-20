@echo off
chcp 65001 >nul
echo ====================================================
echo   Pokémon Opalo 繁體中文化補丁 - 還原腳本
echo   版本: 2.11
echo ====================================================
echo.

setlocal EnableDelayedExpansion

:: 尋找遊戲目錄
set "GAME_DIR=%~dp0"
if "%GAME_DIR:~-1%"=="\" set "GAME_DIR=%GAME_DIR:~0,-1%"

:: 如果從 localization\installer 執行
if not exist "!GAME_DIR!\Game.exe" (
    if exist "%~dp0..\..\Game.exe" (
        pushd "%~dp0..\.."
        set "GAME_DIR=!CD!"
        popd
    )
)

:: 驗證遊戲目錄
if not exist "!GAME_DIR!\Game.exe" (
    echo [錯誤] 找不到 Game.exe
    echo 請將此腳本放在遊戲目錄中執行。
    echo.
    pause
    exit /b 1
)

set "DATA_DIR=!GAME_DIR!\Data"
set "BACKUP_DIR=!DATA_DIR!\backup"

:: 檢查備份目錄
if not exist "!BACKUP_DIR!" (
    echo [錯誤] 找不到備份目錄: !BACKUP_DIR!
    echo.
    echo 備份目錄不存在，無法還原。
    echo 可能原因：
    echo   - 尚未安裝過中文化補丁
    echo   - 備份目錄已被手動刪除
    echo.
    pause
    exit /b 1
)

:: 計算備份檔案數
set "FILE_COUNT=0"
for %%F in ("!BACKUP_DIR!\*") do (
    set /a "FILE_COUNT+=1"
)

if !FILE_COUNT!==0 (
    echo [錯誤] 備份目錄中沒有檔案。
    echo.
    pause
    exit /b 1
)

echo 遊戲目錄: !GAME_DIR!
echo 備份目錄: !BACKUP_DIR!
echo 備份檔案數: !FILE_COUNT!
echo.

:: 確認還原
echo [警告] 此操作將用備份檔案覆蓋 Data 資料夾中的對應檔案。
echo 中文化補丁將被移除，遊戲將恢復為原始語言。
echo.
set /p "CONFIRM=是否繼續還原？(Y/N): "
if /i not "!CONFIRM!"=="Y" (
    echo 還原已取消。
    pause
    exit /b 0
)

echo.
echo 正在還原原始檔案...
echo.

:: 還原備份檔案
set "RESTORE_COUNT=0"
for %%F in ("!BACKUP_DIR!\*") do (
    set "FNAME=%%~nxF"
    copy /y "%%F" "!DATA_DIR!\!FNAME!" >nul
    set /a "RESTORE_COUNT+=1"
    echo   已還原: !FNAME!
)

echo.
echo 已還原 !RESTORE_COUNT! 個檔案。

:: 詢問是否刪除備份
echo.
set /p "DEL_BACKUP=是否刪除備份目錄？(Y/N): "
if /i "!DEL_BACKUP!"=="Y" (
    rmdir /s /q "!BACKUP_DIR!"
    echo 備份目錄已刪除。
) else (
    echo 備份目錄已保留: !BACKUP_DIR!
)

echo.
echo ====================================================
echo   還原完成！
echo   遊戲已恢復為原始版本。
echo ====================================================
echo.
pause
