# Flow Launcher Shortcuts Plugin

A powerful Flow Launcher plugin for quick access to folders, files, applications, and URLs via custom keywords. Includes a beautiful PySide6 GUI editor with **browser bookmark import** for managing shortcuts.

[![GitHub release](https://img.shields.io/github/v/release/AMoorer/am_flowlauncher_plugins)](https://github.com/AMoorer/am_flowlauncher_plugins/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### Plugin Features
- **Quick Access**: Launch folders, files, apps, and URLs with custom keywords
- **Categorized**: Organize shortcuts by category (Folders, Files, Apps, custom bookmark categories)
- **Priority System**: Control result ordering with priority weights (0-200)
- **Custom Icons**: Assign custom icons to each shortcut
- **Smart Actions**:
  - Open folders in File Explorer
  - Open files with default or specified applications
  - Launch applications
  - Open URLs in default browser
- **Context Menu**: Right-click for edit, copy, and delete options
- **List View**: Use `s shortcutlist` to see all shortcuts grouped by category

### GUI Editor Features
- **Intuitive Interface**: Beautiful PySide6 application with dark mode support
- **Browser Bookmark Import**: Import bookmarks from Chrome, Edge, Opera, Brave
- **Custom Save Location**: Choose where shortcuts are saved
- **Table View**: See all shortcuts at a glance
- **Add/Edit/Delete**: Full CRUD operations
- **Category Organization**: Group shortcuts logically
- **Icon Picker**: Browse for custom icons
- **Auto-Save**: Changes saved immediately to JSON
- **About Dialog**: Built-in help and usage information

## 📥 Installation

### Quick Start (Recommended)

1. **Download the latest release**:
   - Download `ShortcutsEditor.exe` (standalone, no Python required)
   - Download `Flow.Launcher.Plugin.Shortcuts.zip`

2. **Install the plugin**:
   ```bash
   # Extract to Flow Launcher plugins directory
   Extract Flow.Launcher.Plugin.Shortcuts.zip to:
   %APPDATA%\FlowLauncher\Plugins\
   ```

3. **Install plugin dependencies**:
   ```bash
   cd %APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts
   pip install -r requirements.txt
   ```

4. **Run the editor**:
   - Double-click `ShortcutsEditor.exe`
   - Add your first shortcut!

5. **Restart Flow Launcher**

### Manual Installation (For Developers)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/AMoorer/am_flowlauncher_plugins.git
   cd am_flowlauncher_plugins
   ```

2. **Install plugin**:
   ```bash
   xcopy /E /I Flow.Launcher.Plugin.Shortcuts %APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts
   cd %APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts
   pip install -r requirements.txt
   ```

3. **Install editor dependencies**:
   ```bash
   cd ShortcutsEditor
   pip install -r requirements.txt
   ```

4. **Run editor**:
   ```bash
   python editor.py
   ```

## 🚀 Usage

### Basic Usage

1. **Add shortcuts** using the GUI editor
2. **In Flow Launcher**, type `s <keyword>` to trigger your shortcut
3. **Press Enter** to execute

### List All Shortcuts

Type `s shortcutlist` to view all shortcuts grouped by category.

### Examples

- `s docs` → Open Documents folder
- `s code` → Launch VS Code
- `s github` → Open GitHub in browser
- `s report` → Open report.xlsx with Excel

### Context Menu (Right-Click)

- **Open Shortcuts Editor**: Edit the shortcut
- **Copy Path**: Copy the path/URL to clipboard
- **Delete Shortcut**: Remove the shortcut

## 📚 GUI Editor Guide

### Main Features

The Shortcuts Editor provides a comprehensive interface for managing shortcuts:

- **File Menu**:
  - `Change Save Location...` - Choose custom shortcuts file location
  - `Exit` - Close the application

- **Help Menu**:
  - `About` - View version, features, and usage instructions

### Adding Shortcuts

1. Click **"Add Shortcut"**
2. Fill in the fields:
   - **Keyword**: Trigger word (e.g., "docs", "github")
   - **Type**: folder, file, app, or url
   - **Path/URL**: Target location
   - **Category**: Organizational category
   - **Priority**: Display order (0-200, higher appears first)
   - **Icon**: Optional custom icon path
   - **Open With** (files only): Specific application

### Importing Browser Bookmarks

1. Click **"Import Bookmarks..."**
2. **Select browser** from dropdown (Chrome, Edge, Opera, Brave)
3. Click **"Load Bookmarks"** or **"Browse..."** for custom location
4. **Select bookmarks** to import (Ctrl+Click for multiple)
5. **Configure import settings**:
   - Default Category
   - Default Priority
   - Use bookmark folder as category (recommended)
6. Click **"Import Selected"**

Keywords are automatically generated from bookmark names, and duplicates are handled gracefully.

### Field Reference

| Field | Description |
|-------|-------------|
| **Keyword** | Trigger keyword (e.g., "docs", "vscode") |
| **Type** | folder, file, app, or url |
| **Path/URL** | Target location or web address |
| **Category** | Organizational category |
| **Priority** | Display order (higher = first, 0-200) |
| **Icon** | Path to icon file (png, ico, jpg) |
| **Open With** | (Files only) Application path |

## 📁 Repository Structure

```
am_flowlauncher_plugins/
├── Flow.Launcher.Plugin.Shortcuts/    # The Flow Launcher plugin
│   ├── main.py                        # Plugin entry point
│   ├── plugin.json                    # Plugin metadata
│   ├── shortcuts.json                 # Shortcuts data file
│   ├── requirements.txt               # Python dependencies
│   ├── test.py                        # Test suite
│   └── Images/                        # Icon resources
│
├── ShortcutsEditor/                   # GUI editor application
│   ├── editor.py                      # Main editor application
│   ├── requirements.txt               # Editor dependencies
│   └── build_exe.bat                  # PyInstaller build script
│
├── README.md                          # This file
├── LICENSE                            # MIT License
├── QUICKSTART.md                      # 5-minute setup guide
└── .gitignore                         # Git ignore rules
```

## 🔧 Shortcuts Data Format

The `shortcuts.json` file structure:

```json
{
  "shortcuts": [
    {
      "keyword": "docs",
      "type": "folder",
      "path": "C:\\Users\\YourName\\Documents",
      "category": "Folders",
      "priority": 100,
      "icon": "Images/folder.png"
    },
    {
      "keyword": "github",
      "type": "url",
      "path": "https://github.com",
      "category": "Development",
      "priority": 90,
      "icon": "Images/bookmark.png"
    },
    {
      "keyword": "report",
      "type": "file",
      "path": "C:\\Reports\\monthly.xlsx",
      "category": "Files",
      "priority": 80,
      "icon": "Images/excel.png",
      "openWith": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
    }
  ]
}
```

## 🌍 Environment Variables

Paths support Windows environment variables:

- `%APPDATA%`
- `%USERPROFILE%`
- `%LOCALAPPDATA%`
- `%PROGRAMFILES%`
- etc.

Example: `%USERPROFILE%\\Documents\\my-file.txt`

## 🛠️ Development

### Project Stack

- **Plugin**: Python 3.8+ with flowlauncher library
- **Editor**: PySide6 (Qt for Python)
- **Data**: JSON file storage
- **Packaging**: PyInstaller for standalone executables

### Building the Standalone Editor

To create a standalone `.exe` file:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Run the build script**:
   ```bash
   cd ShortcutsEditor
   build_exe.bat
   ```

3. **Executable location**:
   ```
   ShortcutsEditor/dist/ShortcutsEditor.exe
   ```

### Testing the Plugin

1. Edit shortcuts using the GUI editor
2. Test in Flow Launcher with `s <keyword>`
3. Check Flow Launcher logs if issues occur
4. Run `test.py` for unit tests

### Extending the Plugin

The plugin is designed to be extensible:

- Add new shortcut types in `main.py`
- Customize result formatting
- Add additional context menu items
- Integrate with external services

## 📖 Documentation

- **[README.md](README.md)** - This file
- **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Detailed architecture
- **[CLAUDE_SKILL_FLOW_LAUNCHER_PLUGINS.md](CLAUDE_SKILL_FLOW_LAUNCHER_PLUGINS.md)** - Development patterns

## 🐛 Troubleshooting

### Plugin doesn't appear in Flow Launcher
- Verify plugin folder location: `%APPDATA%\FlowLauncher\Plugins\`
- Check `plugin.json` for syntax errors
- Ensure `flowlauncher` package is installed for the correct Python version
- Restart Flow Launcher

### Editor can't find shortcuts.json
- Use `File → Change Save Location...` to set custom location
- Editor auto-detects:
  - Sibling `Flow.Launcher.Plugin.Shortcuts/` directory
  - `%APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts\`
- Verify file exists and has correct JSON format

### Shortcut doesn't execute
- Check path exists (expand environment variables)
- Verify file/folder permissions
- Check Flow Launcher logs for errors

### Icons don't display
- Use absolute paths or paths relative to plugin directory
- Supported formats: PNG, ICO, JPG, BMP
- Default icon used if custom icon not found

### Bookmark import issues
- Ensure browser is closed when importing (Chrome locks bookmark file)
- Use "Browse..." for non-standard browser locations
- Check that bookmark file exists at expected location

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest features
- Submit pull requests
- Share your shortcuts

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Andy Moorer**  
GitHub: [@AMoorer](https://github.com/AMoorer)

## 🙏 Acknowledgments

- Flow Launcher team for the excellent launcher
- PySide6/Qt for the GUI framework
- The Python community

---

**Version**: 1.0.0  
**Date**: December 2024

*Part of the am_flowlauncher_plugins collection*
