@echo off
echo Syncing plugin to Flow Launcher...

set "SOURCE=c:\Users\andym\develop\repositories\am_flowlauncher_plugins\Flow.Launcher.Plugin.Shortcuts"
set "DEST=%APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts"

echo Copying main.py...
copy /Y "%SOURCE%\main.py" "%DEST%\main.py"

echo Copying plugin.json...
copy /Y "%SOURCE%\plugin.json" "%DEST%\plugin.json"

echo Copying shortcuts.json...
copy /Y "%SOURCE%\shortcuts.json" "%DEST%\shortcuts.json"

echo.
echo Done! Restart Flow Launcher to see changes.
pause
