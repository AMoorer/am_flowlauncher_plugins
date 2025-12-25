# Flow Launcher Shortcuts Plugin

A powerful Flow Launcher plugin for quick access to folders, files, applications, and URLs via custom keywords. Includes a beautiful PySide6 GUI editor for managing shortcuts.

## Features

- **Quick Access**: Launch folders, files, apps, and URLs with custom keywords
- **Categorized**: Organize shortcuts by category (Folders, Files, Apps, custom bookmark categories)
- **GUI Editor**: Intuitive PySide6 application for managing shortcuts
- **Priority System**: Control result ordering with priority weights
- **Custom Icons**: Assign custom icons to each shortcut
- **Smart Actions**:
  - Open folders in File Explorer
  - Open files with default or specified applications
  - Launch applications
  - Open URLs in default browser
- **Context Menu**: Right-click for edit, copy, and delete options
- **List View**: Use `s shortcutlist` to see all shortcuts grouped by category

## Repository Structure

```
am_flowlauncher_plugins/
├── Flow.Launcher.Plugin.Shortcuts/    # The Flow Launcher plugin
│   ├── main.py                        # Plugin entry point
│   ├── plugin.json                    # Plugin metadata
│   ├── shortcuts.json                 # Shortcuts data file
│   ├── requirements.txt               # Python dependencies
│   └── Images/                        # Icon resources
│       └── shortcut.png               # Default icon
│
└── ShortcutsEditor/                   # GUI editor application
    ├── editor.py                      # Main editor application
    ├── requirements.txt               # Editor dependencies
    └── launch_editor.bat              # Windows launcher
```

## Installation

### Plugin Installation

1. **Copy to Flow Launcher**:
   ```
   Copy Flow.Launcher.Plugin.Shortcuts to:
   %APPDATA%\FlowLauncher\Plugins\
   ```

2. **Install Dependencies**:
   ```bash
   cd %APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts
   pip install -r requirements.txt
   ```

3. **Restart Flow Launcher**

### Editor Installation

1. **Install PySide6**:
   ```bash
   cd ShortcutsEditor
   pip install -r requirements.txt
   ```

2. **Launch Editor**:
   - Double-click `launch_editor.bat`, or
   - Run `python editor.py`

## Usage

### Basic Usage

1. **Add a shortcut** using the GUI editor
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

## GUI Editor

The Shortcuts Editor provides:

- **Table View**: See all shortcuts at a glance
- **Add/Edit/Delete**: Full CRUD operations
- **Type Selection**: Choose folder, file, app, or url
- **Category Organization**: Group shortcuts logically
- **Icon Picker**: Browse for custom icons
- **Priority Control**: Set display order (0-200)
- **Open With**: Specify application for file shortcuts
- **Auto-Save**: Changes saved immediately to JSON

### Editor Fields

| Field | Description |
|-------|-------------|
| **Keyword** | Trigger keyword (e.g., "docs", "vscode") |
| **Type** | folder, file, app, or url |
| **Path/URL** | Target location or web address |
| **Category** | Organizational category |
| **Priority** | Display order (higher = first, 0-200) |
| **Icon** | Path to icon file (png, ico, jpg) |
| **Open With** | (Files only) Application path |

## Shortcuts Data Format

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
      "icon": "Images/github.png"
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

## Environment Variables

Paths support Windows environment variables:

- `%APPDATA%`
- `%USERPROFILE%`
- `%LOCALAPPDATA%`
- `%PROGRAMFILES%`
- etc.

Example: `%USERPROFILE%\\Documents\\my-file.txt`

## Development

### Project Stack

- **Plugin**: Python 3.x with flowlauncher library
- **Editor**: PySide6 (Qt for Python)
- **Data**: JSON file storage

### Testing the Plugin

1. Edit shortcuts using the GUI editor
2. Test in Flow Launcher with `s <keyword>`
3. Check logs in Flow Launcher settings if issues occur

### Extending the Plugin

The plugin is designed to be extensible:

- Add new shortcut types in `main.py`
- Customize result formatting
- Add additional context menu items
- Integrate with external services

## Claude Development Skill

This project serves as a reference implementation for creating Flow Launcher plugins with GUI editors. Key patterns demonstrated:

1. **Flow Launcher Plugin Structure**
   - JSON-RPC communication via FlowLauncher base class
   - Result formatting with icons and actions
   - Context menu implementation

2. **PySide6 GUI Development**
   - Modern Qt application with forms and tables
   - File browser integration
   - Settings persistence
   - Icon preview and selection

3. **Shared Data Architecture**
   - JSON as data interchange format
   - Cross-application data access
   - File watching and auto-reload

4. **Windows Integration**
   - Environment variable expansion
   - File associations
   - Shell commands
   - Clipboard access

## Troubleshooting

### Plugin doesn't appear in Flow Launcher
- Verify plugin folder location: `%APPDATA%\FlowLauncher\Plugins\`
- Check `plugin.json` for syntax errors
- Ensure `flowlauncher` package is installed
- Restart Flow Launcher

### Editor can't find shortcuts.json
- Editor looks in sibling `Flow.Launcher.Plugin.Shortcuts/` directory
- Or in `%APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts\`
- Verify file exists and has correct JSON format

### Shortcut doesn't execute
- Check path exists (expand environment variables mentally)
- Verify file/folder permissions
- Check Flow Launcher logs for errors

### Icons don't display
- Use absolute paths or paths relative to plugin directory
- Supported formats: PNG, ICO, JPG, BMP
- Default icon used if custom icon not found

## Contributing

This is a personal development repository. Feel free to fork and adapt for your needs.

## License

MIT License - see individual files for details.

## Author

Andy Moorer  
GitHub: [@AMoorer](https://github.com/AMoorer)

---

*Part of the am_flowlauncher_plugins collection*
