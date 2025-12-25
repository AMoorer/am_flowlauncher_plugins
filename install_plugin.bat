@echo off
echo ========================================
echo Flow Launcher Shortcuts Plugin Installer
echo ========================================
echo.

REM Check if Flow Launcher is installed
if not exist "%APPDATA%\FlowLauncher" (
    echo ERROR: Flow Launcher not found at %APPDATA%\FlowLauncher
    echo Please install Flow Launcher first: https://www.flowlauncher.com
    pause
    exit /b 1
)

set "PLUGIN_DIR=%APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts"

echo Installing to: %PLUGIN_DIR%
echo.

REM Create plugin directory if it doesn't exist
if not exist "%PLUGIN_DIR%" (
    echo Creating plugin directory...
    mkdir "%PLUGIN_DIR%"
)

REM Copy plugin files
echo Copying plugin files...
xcopy /E /I /Y "Flow.Launcher.Plugin.Shortcuts\*" "%PLUGIN_DIR%"

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to copy plugin files
    pause
    exit /b 1
)

echo.
echo Plugin files copied successfully!
echo.

REM Install Python dependencies
echo Installing Python dependencies...
cd "%PLUGIN_DIR%"
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo WARNING: Failed to install Python dependencies
    echo Please install manually:
    echo   cd "%PLUGIN_DIR%"
    echo   pip install -r requirements.txt
) else (
    echo.
    echo Dependencies installed successfully!
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Add icon files to: %PLUGIN_DIR%\Images\
echo    (See Images\ICONS_NEEDED.txt for details)
echo.
echo 2. Restart Flow Launcher
echo    (Right-click tray icon ^> Restart)
echo.
echo 3. Test the plugin:
echo    - Open Flow Launcher (Alt+Space)
echo    - Type: s shortcutlist
echo.
echo 4. Add shortcuts using the editor:
echo    - cd ShortcutsEditor
echo    - python editor.py
echo.
pause
