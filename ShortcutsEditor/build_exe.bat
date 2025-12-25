@echo off
echo Building Shortcuts Editor...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    pip install pyinstaller
)

echo.
echo Creating standalone executable...
echo.

pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name "ShortcutsEditor" ^
    --icon=NONE ^
    --add-data "editor.py;." ^
    editor.py

echo.
echo Build complete!
echo.
echo Executable location: dist\ShortcutsEditor.exe
echo.
pause
