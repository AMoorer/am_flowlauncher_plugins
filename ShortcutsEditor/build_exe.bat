@echo off
echo ========================================
echo  Flow Launcher Shortcuts Editor Builder
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>NUL
if errorlevel 1 (
    echo [INFO] PyInstaller not found. Installing...
    pip install pyinstaller
    echo.
)

REM Check if PySide6 is installed
python -c "import PySide6" 2>NUL
if errorlevel 1 (
    echo [ERROR] PySide6 not found. Please install dependencies:
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [INFO] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist ShortcutsEditor.spec del ShortcutsEditor.spec

echo.
echo [INFO] Building standalone executable...
echo.

pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name "ShortcutsEditor" ^
    --add-data "editor.py;." ^
    --hidden-import "PySide6.QtCore" ^
    --hidden-import "PySide6.QtGui" ^
    --hidden-import "PySide6.QtWidgets" ^
    --exclude-module "matplotlib" ^
    --exclude-module "scipy" ^
    --exclude-module "pandas" ^
    --exclude-module "numpy" ^
    editor.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Build Complete!
echo ========================================
echo.
echo Executable location: dist\ShortcutsEditor.exe
echo File size:
dir dist\ShortcutsEditor.exe | find "ShortcutsEditor.exe"
echo.
echo You can now distribute ShortcutsEditor.exe as a standalone application.
echo.
pause
