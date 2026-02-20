@echo off
chcp 65001 >nul
echo ====================================================
echo   Pokémon Opalo 繁體中文化補丁 - 安裝器編譯工具
echo ====================================================
echo.

:: 嘗試尋找 Inno Setup 編譯器
set "ISCC="

:: 檢查常見安裝路徑
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    set "ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)
if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    set "ISCC=C:\Program Files\Inno Setup 6\ISCC.exe"
)
if exist "C:\Program Files (x86)\Inno Setup 5\ISCC.exe" (
    set "ISCC=C:\Program Files (x86)\Inno Setup 5\ISCC.exe"
)
if exist "C:\Program Files\Inno Setup 5\ISCC.exe" (
    set "ISCC=C:\Program Files\Inno Setup 5\ISCC.exe"
)

:: 檢查 PATH 中是否有 ISCC
where ISCC.exe >nul 2>nul
if %errorlevel%==0 (
    set "ISCC=ISCC.exe"
)

if "%ISCC%"=="" (
    echo [錯誤] 找不到 Inno Setup 編譯器 (ISCC.exe)
    echo.
    echo 請先安裝 Inno Setup 6：
    echo   https://jrsoftware.org/isdl.php
    echo.
    echo 或將 ISCC.exe 加入系統 PATH 環境變數。
    echo.
    pause
    exit /b 1
)

echo 找到 Inno Setup: %ISCC%
echo.

:: 檢查 patches 目錄是否有檔案
set "PATCH_DIR=%~dp0..\..\patches"
dir /b "%PATCH_DIR%\*" 2>nul | findstr /v /i ".gitkeep" >nul
if %errorlevel% neq 0 (
    echo [警告] patches 目錄中沒有補丁檔案！
    echo 請先執行翻譯打包流程產生補丁檔案。
    echo.
    pause
    exit /b 1
)

:: 建立輸出目錄
if not exist "%~dp0output" mkdir "%~dp0output"

:: 編譯安裝器
echo 正在編譯安裝器...
echo.
"%ISCC%" "%~dp0setup.iss"

if %errorlevel%==0 (
    echo.
    echo ====================================================
    echo   編譯成功！
    echo   安裝器位於: %~dp0output\
    echo ====================================================
) else (
    echo.
    echo [錯誤] 編譯失敗，請檢查錯誤訊息。
)

echo.
pause
