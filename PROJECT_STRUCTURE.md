# Project Structure

Complete overview of the Flow Launcher Shortcuts plugin project.

## Directory Tree

```
am_flowlauncher_plugins/
│
├── Flow.Launcher.Plugin.Shortcuts/     # Main plugin directory
│   ├── main.py                         # Plugin entry point (785 lines)
│   ├── plugin.json                     # Plugin metadata
│   ├── shortcuts.json                  # User shortcuts data (empty by default)
│   ├── shortcuts_example.json          # Example shortcuts for testing
│   ├── requirements.txt                # Python dependencies (flowlauncher)
│   ├── test.py                         # Plugin test suite
│   ├── .gitignore                      # Git ignore rules
│   └── Images/                         # Icon resources
│       ├── ICONS_NEEDED.txt            # Icon requirements documentation
│       ├── shortcut.png                # Main plugin icon (to be added)
│       ├── folder.png                  # Folder shortcut icon (to be added)
│       ├── file.png                    # File shortcut icon (to be added)
│       ├── app.png                     # App shortcut icon (to be added)
│       ├── bookmark.png                # URL bookmark icon (to be added)
│       ├── copy.png                    # Context menu copy icon (to be added)
│       └── delete.png                  # Context menu delete icon (to be added)
│
├── ShortcutsEditor/                    # GUI editor application
│   ├── editor.py                       # PySide6 GUI application (550+ lines)
│   ├── requirements.txt                # Editor dependencies (PySide6)
│   └── launch_editor.bat               # Windows launcher script
│
├── README.md                           # Main project documentation
├── QUICKSTART.md                       # Quick start guide
├── CLAUDE_SKILL_FLOW_LAUNCHER_PLUGINS.md  # Claude development skill doc
├── PROJECT_STRUCTURE.md                # This file
├── install_plugin.bat                  # Automated installer for Windows
├── metadata.json                       # Repository metadata
└── prompts.json                        # AI prompts (if any)
```

## File Descriptions

### Plugin Core Files

#### `main.py` (785 lines)
The heart of the plugin. Inherits from `FlowLauncher` base class.

**Key Classes:**
- `Shortcuts(FlowLauncher)` - Main plugin class

**Key Methods:**
- `query(query)` - Handles user queries, returns results
- `show_shortcut_list(filter)` - Shows all shortcuts grouped by category
- `context_menu(data)` - Right-click context menu
- `execute_shortcut(shortcut_json)` - Executes folder/file/app/URL actions
- `open_editor()` - Launches GUI editor
- `copy_to_clipboard(text)` - Clipboard operations
- `delete_shortcut(keyword)` - Removes a shortcut
- `create_result(shortcut)` - Formats shortcut as Flow Launcher result
- `load_shortcuts()` / `save_shortcuts()` - JSON persistence

**Features:**
- Multi-type shortcut support (folder, file, app, url)
- Priority-based result ordering
- Category grouping
- Environment variable expansion
- Icon resolution
- Error handling and logging

#### `plugin.json`
Plugin metadata for Flow Launcher.

```json
{
    "ID": "A8B9C1D2E3F4G5H6I7J8K9L0M1N2O3P4",
    "ActionKeyword": "s",
    "Name": "Shortcuts",
    "Description": "Quick access to folders, files, apps, and URLs",
    "Author": "Andy Moorer",
    "Version": "1.0.0",
    "Language": "python",
    "Website": "https://github.com/AMoorer/am_flowlauncher_plugins",
    "IcoPath": "Images\\shortcut.png",
    "ExecuteFileName": "main.py"
}
```

#### `shortcuts.json`
User data file. Empty by default, populated by GUI editor.

**Schema:**
```json
{
  "shortcuts": [
    {
      "keyword": "string",
      "type": "folder|file|app|url",
      "path": "string",
      "category": "string",
      "priority": "integer (0-200)",
      "icon": "string (path)",
      "openWith": "string (optional, for files)"
    }
  ]
}
```

#### `test.py`
Standalone test suite for plugin functionality.

**Test Suites:**
- Data operations (load/save)
- Query tests (empty, shortcutlist, search, partial)
- Action method tests
- Result creation tests

**Usage:**
```bash
python test.py
```

### Editor Files

#### `editor.py` (550+ lines)
Full-featured PySide6 GUI application.

**Key Classes:**
- `ShortcutsEditorWindow(QMainWindow)` - Main window
- `ShortcutDialog(QDialog)` - Add/edit dialog

**Features:**
- Table view of all shortcuts
- Add/Edit/Delete operations
- Category organization
- Icon picker with preview
- Priority control (0-200 spinner)
- Type-specific fields (Open With for files)
- Form validation
- Auto-save to JSON
- Settings persistence (window geometry)
- Automatic plugin data file location

**UI Components:**
- QTableWidget for shortcuts list
- QFormLayout for input fields
- QFileDialog for browsing
- QComboBox for type selection
- QSpinBox for priority
- QLabel with QPixmap for icon preview

### Documentation Files

#### `README.md`
Comprehensive project documentation covering:
- Features overview
- Installation instructions (plugin + editor)
- Usage examples
- Data format specification
- Troubleshooting guide
- Development guidelines

#### `QUICKSTART.md`
Step-by-step quick start guide:
- 5-minute setup
- Example shortcuts to add
- Testing commands
- Common tips and tricks

#### `CLAUDE_SKILL_FLOW_LAUNCHER_PLUGINS.md`
Development skill documentation:
- Flow Launcher plugin architecture
- Python plugin patterns
- Result object structure
- Common implementation patterns
- Best practices
- Complete mini example
- PySide6 GUI patterns

#### `PROJECT_STRUCTURE.md`
This file - complete project overview.

### Installation Scripts

#### `install_plugin.bat`
Windows batch script for automated installation:
1. Checks for Flow Launcher installation
2. Creates plugin directory
3. Copies plugin files
4. Installs Python dependencies
5. Displays next steps

#### `launch_editor.bat`
Simple launcher for the GUI editor.

### Supporting Files

#### `requirements.txt` (Plugin)
```
flowlauncher>=2.0.0
```

#### `requirements.txt` (Editor)
```
PySide6>=6.6.0
```

#### `.gitignore`
Excludes:
- `__pycache__/`
- `*.pyc`
- `*.log`
- `shortcuts.json.bak`

## Data Flow

```
User Input (Flow Launcher)
         ↓
    main.py::query()
         ↓
    Load shortcuts.json
         ↓
    Filter & Sort
         ↓
    Create Results
         ↓
    Return to Flow Launcher
         ↓
    User Selects → execute_shortcut()
         ↓
    Action (open folder/file/app/url)
```

## GUI Editor Data Flow

```
Launch editor.py
        ↓
Find shortcuts.json
        ↓
Load into QTableWidget
        ↓
User Add/Edit/Delete
        ↓
Update shortcuts list
        ↓
Save to shortcuts.json
        ↓
Plugin auto-reloads on next query
```

## Dependencies

### Plugin Runtime
- **Python**: 3.8+
- **flowlauncher**: Flow Launcher JSON-RPC library
- **Windows**: os, subprocess, webbrowser (standard library)

### GUI Editor
- **Python**: 3.8+
- **PySide6**: Qt for Python framework
  - QtWidgets - UI components
  - QtCore - Settings, signals
  - QtGui - Icons, images

### Development
- **Flow Launcher**: 1.8+
- **pip**: Package management

## Integration Points

### Plugin ↔ Flow Launcher
- **Communication**: JSON-RPC over stdin/stdout
- **Protocol**: FlowLauncher base class handles
- **Data Exchange**: Result dictionaries, JsonRPCAction

### Editor ↔ Plugin
- **Shared File**: shortcuts.json
- **Format**: JSON
- **Location**: Auto-discovered or configurable
- **Sync**: Plugin reloads on each query

### Plugin ↔ Windows
- **File Operations**: os.startfile()
- **Process Launch**: subprocess.Popen()
- **URLs**: webbrowser.open()
- **Clipboard**: win32clipboard or PowerShell fallback
- **Env Vars**: os.path.expandvars()

## Extension Points

### Adding New Shortcut Types
1. Update `shortcuts.json` schema
2. Add type option in `editor.py::ShortcutDialog`
3. Implement execution logic in `main.py::execute_shortcut()`
4. Update result creation in `main.py::create_result()`

### Custom Actions
1. Add method to `Shortcuts` class in `main.py`
2. Reference in `JsonRPCAction` in result
3. Optionally add to context menu

### UI Enhancements
1. Modify `editor.py::ShortcutsEditorWindow`
2. Add new form fields in `editor.py::ShortcutDialog`
3. Update JSON schema if new data fields

### Integration Features
- Export/Import shortcuts
- Sync with cloud services
- Shortcut usage statistics
- Quick edit from Flow Launcher
- Backup/restore functionality

## Code Statistics

- **Total Lines**: ~2,500+
- **Python Files**: 3 (main.py, editor.py, test.py)
- **JSON Files**: 2 (plugin.json, shortcuts.json)
- **Documentation**: 4 MD files
- **Scripts**: 2 BAT files

## Version History

### v1.0.0 (Initial Release)
- Core plugin functionality
- GUI editor
- Full documentation
- Test suite
- Installation scripts

## Future Enhancements

### Planned Features
- [ ] Fuzzy search matching
- [ ] Shortcut usage analytics
- [ ] Backup/restore GUI
- [ ] Import from browser bookmarks
- [ ] Keyboard shortcut recording
- [ ] Folder/file monitoring
- [ ] Recently used shortcuts
- [ ] Shortcut groups/tags
- [ ] Quick edit without opening editor
- [ ] Portable mode support

### Technical Debt
- [ ] Add proper unit tests
- [ ] Implement logging rotation
- [ ] Add error recovery for corrupt JSON
- [ ] Icon caching for performance
- [ ] Async file operations
- [ ] Type hints throughout

## Building for Distribution

### Plugin Package
```bash
# Create release folder
mkdir release
xcopy /E /I Flow.Launcher.Plugin.Shortcuts release\Flow.Launcher.Plugin.Shortcuts

# Exclude development files
del release\*.example.json
del release\test.py
```

### Editor Executable (PyInstaller)
```bash
cd ShortcutsEditor
pyinstaller --onefile --windowed --name ShortcutsEditor editor.py
```

Result: `dist\ShortcutsEditor.exe` (standalone executable)

## License

MIT License - Free to use, modify, and distribute.

## Contact

**Author**: Andy Moorer  
**Repository**: https://github.com/AMoorer/am_flowlauncher_plugins  
**Issues**: Use GitHub issues for bug reports

---

*Document Version: 1.0*  
*Last Updated: 2024-12-24*
