@echo off
setlocal enabledelayedexpansion

echo ========================================
echo  Flow Launcher Shortcuts - Release Packager
echo ========================================
echo.

set VERSION=1.0.0
set RELEASE_DIR=release_v%VERSION%

echo Creating release directory: %RELEASE_DIR%
if exist %RELEASE_DIR% rmdir /s /q %RELEASE_DIR%
mkdir %RELEASE_DIR%

echo.
echo ========================================
echo  Step 1: Building Standalone Editor
echo ========================================
echo.

cd ShortcutsEditor
call build_exe.bat
if errorlevel 1 (
    echo [ERROR] Editor build failed!
    cd ..
    pause
    exit /b 1
)
cd ..

echo.
echo ========================================
echo  Step 2: Copying Standalone Editor
echo ========================================
echo.

if exist ShortcutsEditor\dist\ShortcutsEditor.exe (
    copy ShortcutsEditor\dist\ShortcutsEditor.exe %RELEASE_DIR%\
    echo [OK] ShortcutsEditor.exe copied
) else (
    echo [ERROR] ShortcutsEditor.exe not found!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Step 3: Creating Plugin Package
echo ========================================
echo.

set PLUGIN_DIR=%RELEASE_DIR%\Flow.Launcher.Plugin.Shortcuts

mkdir %PLUGIN_DIR%
mkdir %PLUGIN_DIR%\Images

REM Copy plugin files
copy Flow.Launcher.Plugin.Shortcuts\main.py %PLUGIN_DIR%\
copy Flow.Launcher.Plugin.Shortcuts\plugin.json %PLUGIN_DIR%\
copy Flow.Launcher.Plugin.Shortcuts\requirements.txt %PLUGIN_DIR%\
copy Flow.Launcher.Plugin.Shortcuts\shortcuts.json %PLUGIN_DIR%\

REM Copy images (placeholder - user needs to add icons)
copy Flow.Launcher.Plugin.Shortcuts\Images\*.png %PLUGIN_DIR%\Images\ 2>NUL
copy Flow.Launcher.Plugin.Shortcuts\Images\*.ico %PLUGIN_DIR%\Images\ 2>NUL

echo [OK] Plugin files copied

echo.
echo ========================================
echo  Step 4: Creating ZIP Archive
echo ========================================
echo.

REM Create zip using PowerShell
powershell -command "Compress-Archive -Path '%PLUGIN_DIR%' -DestinationPath '%RELEASE_DIR%\Flow.Launcher.Plugin.Shortcuts.zip' -Force"

if exist %RELEASE_DIR%\Flow.Launcher.Plugin.Shortcuts.zip (
    echo [OK] Plugin ZIP created
) else (
    echo [WARNING] Could not create ZIP. Please create manually.
)

echo.
echo ========================================
echo  Step 5: Copying Documentation
echo ========================================
echo.

copy README.md %RELEASE_DIR%\README.md
copy LICENSE %RELEASE_DIR%\
copy CHANGELOG.md %RELEASE_DIR%\
copy QUICKSTART.md %RELEASE_DIR%\

echo [OK] Documentation copied

echo.
echo ========================================
echo  Release Package Created!
echo ========================================
echo.
echo Release directory: %RELEASE_DIR%
echo.
echo Contents:
dir /b %RELEASE_DIR%
echo.
echo ========================================
echo  Next Steps:
echo ========================================
echo.
echo 1. Test ShortcutsEditor.exe on a clean machine
echo 2. Test plugin installation from ZIP
echo 3. Create GitHub release
echo 4. Upload files:
echo    - ShortcutsEditor.exe
echo    - Flow.Launcher.Plugin.Shortcuts.zip
echo    - Source code (auto-generated)
echo.
pause
