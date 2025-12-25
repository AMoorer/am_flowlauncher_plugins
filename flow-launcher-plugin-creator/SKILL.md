---
name: flow-launcher-plugin-creator
description: Comprehensive skill for creating Flow Launcher plugins with Python, including project setup, plugin development, GUI editors with PySide6, GitHub Actions automation, and Flow Launcher Plugin Store submission
---

# Flow Launcher Plugin Creator

This skill provides AI assistants with complete knowledge and automation tools for creating professional Flow Launcher plugins from scratch, including optional PySide6 GUI editors, automated builds, and plugin store submission.

## Purpose

Democratize the creation of Flow Launcher plugins by providing AI assistants with:
- Complete plugin architecture knowledge
- Project scaffolding templates
- Best practices and patterns
- Automated build and release workflows
- GUI editor creation with PySide6
- Plugin store submission automation

## When to Use This Skill

Use this skill when the user wants to:
- Create a new Flow Launcher plugin
- Add a GUI editor to an existing plugin
- Automate plugin builds and releases
- Submit a plugin to the Flow Launcher Plugin Store
- Understand Flow Launcher plugin architecture
- Implement common plugin patterns (shortcuts, searches, actions, etc.)

## Flow Launcher Architecture Overview

### Plugin Communication
- **JSON-RPC Protocol**: Flow Launcher communicates with plugins via JSON-RPC
- **Base Class**: Python plugins use the `flowlauncher` package's `FlowLauncher` base class
- **Query Method**: The `query(query: str)` method receives user input
- **Results**: Return list of result dictionaries with Title, SubTitle, IcoPath, JsonRPCAction

### Plugin Structure
```
Flow.Launcher.Plugin.YourPlugin/
├── main.py                 # Entry point, inherits FlowLauncher
├── plugin.json             # Metadata (ID, Name, Version, etc.)
├── requirements.txt        # Python dependencies
├── shortcuts.json          # Optional: Data files
└── Images/                 # Icons and images
    └── icon.png
```

### Result Format
```python
{
    "Title": "Main text displayed",
    "SubTitle": "Secondary description",
    "IcoPath": "Images/icon.png",  # Relative or absolute
    "JsonRPCAction": {
        "method": "method_name",
        "parameters": ["param1", "param2"]
    },
    "Score": 100,  # Optional: Result priority
    "ContextData": {},  # Optional: Data for context menu
}
```

### Context Menu Actions
```python
def context_menu(self, data):
    return [
        {
            "Title": "Action Name",
            "SubTitle": "Action description",
            "JsonRPCAction": {
                "method": "method_name",
                "parameters": [data]
            }
        }
    ]
```

## Plugin Development Patterns

### Pattern 1: Data-Driven Plugins (like Shortcuts)
**Use Case**: Quick access to predefined items (shortcuts, bookmarks, notes)

**Key Components**:
- JSON data file for user content
- Query method filters/searches data
- Result display with categories
- Context menu for edit/delete
- Optional: GUI editor for managing data

**Architecture**:
1. Load data from JSON on initialization
2. Filter/search in `query()` method
3. Execute actions (open file, launch app, open URL)
4. Provide context menu for management

### Pattern 2: Dynamic Search Plugins
**Use Case**: Search external APIs, databases, or file systems

**Key Components**:
- API integration or file system search
- Async operations for responsiveness
- Caching for performance
- Error handling for network issues

**Architecture**:
1. Accept search query from user
2. Query external source
3. Format results dynamically
4. Handle errors gracefully

### Pattern 3: Action Plugins
**Use Case**: Perform system operations (clipboard, screenshots, file operations)

**Key Components**:
- System integration (Windows API, shell commands)
- Parameter handling
- Confirmation dialogs for destructive actions
- Status feedback

### Pattern 4: Calculator/Converter Plugins
**Use Case**: Transform input (math, units, formats)

**Key Components**:
- Real-time evaluation
- Multiple result formats
- Copy-to-clipboard
- No external dependencies (fast)

## Execution Process

### Phase 1: Requirements Gathering
1. Ask user about plugin purpose
2. Determine which pattern best fits
3. Identify required features:
   - Data storage needs (JSON, database, none)
   - GUI editor requirement
   - External API integrations
   - System interactions needed
4. Confirm Python version compatibility (3.8+ recommended)

### Phase 2: Project Setup
1. **Generate GUID** for plugin ID:
   ```python
   import uuid
   str(uuid.uuid4()).upper()
   ```

2. **Create project structure**:
   ```
   Flow.Launcher.Plugin.[Name]/
   ├── main.py
   ├── plugin.json
   ├── requirements.txt
   ├── test.py
   ├── README.md
   └── Images/
       └── icon.png
   ```

3. **Initialize plugin.json** with:
   - Generated GUID
   - Plugin name and description
   - Author information
   - Action keyword
   - Version 1.0.0
   - Language: python

4. **Create main.py** with:
   - FlowLauncher base class inheritance
   - query() method implementation
   - Context menu if needed
   - Proper error handling

5. **Set up requirements.txt**:
   - flowlauncher package
   - Additional dependencies as needed

### Phase 3: Core Plugin Development
1. **Implement `query(query: str)` method**:
   - Parse user input
   - Filter/search data or call APIs
   - Return formatted results
   - Handle empty queries gracefully

2. **Implement action methods**:
   - Methods called via JsonRPCAction
   - System operations (open files, launch apps)
   - Data mutations (add, edit, delete)
   - User feedback

3. **Add context menu** (if applicable):
   - Right-click actions
   - Edit, Copy, Delete patterns
   - Pass ContextData for identification

4. **Implement data persistence** (if needed):
   - JSON file read/write
   - Atomic writes to prevent corruption
   - Backup before modifications

5. **Error handling**:
   - Try-except around file operations
   - Graceful API failure handling
   - User-friendly error messages
   - Logging for debugging

### Phase 4: Result Ordering (Critical!)
**Problem**: Flow Launcher may not respect Score field for ordering

**Solution**: Use invisible zero-width characters as prefixes

```python
def generate_sort_prefix(priority: int) -> str:
    """Generate invisible Unicode prefix for reliable sorting"""
    # Use Zero-Width Space (U+200B) as invisible character
    zwsp = '\u200b'
    # Higher priority = fewer characters (sorts first)
    count = 200 - priority  # Invert so higher priority sorts first
    return zwsp * count

# Usage in results:
{
    "Title": f"{generate_sort_prefix(100)}Category Name",
    "SubTitle": "...",
    # ...
}
```

**Alternative**: Numeric prefixes (visible but effective):
```python
"Title": f"{priority:03d}. Item Name"
```

### Phase 5: GUI Editor (Optional but Recommended)
If user wants a GUI editor:

1. **Create editor directory structure**:
   ```
   [PluginName]Editor/
   ├── editor.py
   ├── requirements.txt
   ├── build_exe.bat
   └── README.md
   ```

2. **Implement PySide6 GUI**:
   - QMainWindow for main window
   - QTableWidget for data display
   - Add/Edit/Delete dialogs
   - Settings persistence (QSettings)
   - Icon picker
   - Menu bar (File, Help)
   - About dialog

3. **Key PySide6 patterns**:
   ```python
   from PySide6.QtWidgets import (
       QApplication, QMainWindow, QTableWidget,
       QPushButton, QVBoxLayout, QWidget
   )
   from PySide6.QtCore import QSettings
   
   class EditorWindow(QMainWindow):
       def __init__(self):
           super().__init__()
           self.settings = QSettings('Author', 'AppName')
           self.setup_ui()
           self.load_data()
   ```

4. **Dark mode support**:
   - Don't hardcode background colors
   - Use system palette
   - Test with both themes

5. **Data synchronization**:
   - Editor reads/writes same JSON as plugin
   - Use file locking if concurrent access possible
   - Auto-reload in Flow Launcher after changes

### Phase 6: Build Automation
1. **Create GitHub Actions workflow**:
   ```yaml
   name: Publish Release
   on:
     release:
       types: [published]
   jobs:
     publish:
       runs-on: windows-latest
       steps:
         - Checkout code
         - Setup Python
         - Install dependencies
         - Build editor (if exists) with PyInstaller
         - Create plugin ZIP
         - Upload to release
   ```

2. **Create local build scripts**:
   - `build_exe.bat` for editor (if applicable)
   - `create_release.bat` for packaging
   - `sync_to_flowlauncher.bat` for development

3. **PyInstaller configuration** (for GUI editors):
   ```bash
   python -m PyInstaller --noconfirm \
       --onefile \
       --windowed \
       --name "EditorName" \
       --hidden-import "PySide6.QtCore" \
       --hidden-import "PySide6.QtGui" \
       --hidden-import "PySide6.QtWidgets" \
       editor.py
   ```

### Phase 7: Testing
1. **Create test.py**:
   - Test query method with various inputs
   - Verify result format
   - Test action methods
   - Test data persistence
   - ASCII output for Windows console compatibility

2. **Manual testing**:
   - Install in Flow Launcher plugins directory
   - Test action keyword
   - Test all features
   - Test context menu
   - Test edge cases

3. **Test editor** (if applicable):
   - All CRUD operations
   - Data validation
   - File persistence
   - UI responsiveness

### Phase 8: Documentation
1. **README.md** with:
   - Feature list
   - Installation instructions
   - Usage examples
   - Screenshots (if GUI)
   - Troubleshooting section

2. **CHANGELOG.md**:
   - Version 1.0.0 release notes
   - Planned features section

3. **Code comments**:
   - Docstrings for methods
   - Inline comments for complex logic
   - Type hints where helpful

### Phase 9: Plugin Store Submission
1. **Prepare manifest file**:
   ```json
   {
     "ID": "GUID-FROM-PLUGIN-JSON",
     "Name": "Plugin Name",
     "Description": "Short description",
     "Author": "Your Name",
     "Version": "1.0.0",
     "Language": "python",
     "Website": "https://github.com/user/repo",
     "UrlDownload": "https://github.com/user/repo/releases/download/v1.0.0/plugin.zip",
     "UrlSourceCode": "https://github.com/user/repo",
     "IcoPath": "https://cdn.jsdelivr.net/gh/user/repo@main/Images/icon.png"
   }
   ```

2. **Submit to Flow Launcher**:
   - Fork Flow-Launcher/Flow.Launcher.PluginsManifest
   - Add manifest file to plugins/ directory
   - Create pull request with description
   - Wait for approval

3. **Future updates**:
   - Create new release on GitHub
   - Flow Launcher CI auto-detects updates every 3 hours
   - No manual PR needed after initial approval

## Critical Best Practices

### 1. Environment Variables
Support Windows environment variables in paths:
```python
import os
path = os.path.expandvars(user_path)
# "%USERPROFILE%\\Documents" -> "C:\\Users\\Name\\Documents"
```

### 2. Icon Paths
- Relative to plugin directory: `Images/icon.png`
- Absolute paths work but reduce portability
- Use CDN (jsdelivr) for plugin store manifest

### 3. Data Files
- Use JSON for simple data
- Atomic writes to prevent corruption:
  ```python
  import json, tempfile, os
  
  # Write to temp file first
  with tempfile.NamedTemporaryFile('w', delete=False) as f:
      json.dump(data, f)
      temp_name = f.name
  
  # Replace original atomically
  os.replace(temp_name, original_path)
  ```

### 4. Error Messages
- Technical errors → log file
- User-facing errors → result SubTitle
- Never crash on bad input

### 5. Performance
- Cache expensive operations
- Load data once in __init__
- Use async for network calls (if possible)
- Limit result count (20-50 max)

### 6. Windows Compatibility
- Use double backslashes in JSON: `"C:\\\\path"`
- Handle Unicode in console (ASCII for test output)
- Test on Windows 10 and 11
- Consider path length limits (260 chars)

### 7. Python Version
- Support Python 3.8+ (Flow Launcher compatibility)
- Avoid version-specific features
- Test with user's Python version

## Common Pitfalls to Avoid

1. **Forgetting to sort results** → Use invisible prefixes
2. **Hardcoded paths** → Use environment variables
3. **No error handling** → Always use try-except
4. **Ignoring Windows console encoding** → ASCII in tests
5. **Breaking atomic writes** → Use temp files
6. **Not testing manually** → Always install and test
7. **Forgetting context menu** → Implement for data-driven plugins
8. **Poor icon paths** → Relative or CDN for portability
9. **No GUI validation** → Validate all user input
10. **Skipping GitHub Actions** → Required for plugin store

## Template Selection Guide

Based on user requirements, select and customize:

1. **Basic Query Plugin** → Use `template_basic_plugin.py`
2. **Data-Driven Plugin** → Use `template_shortcuts_plugin.py`
3. **GUI Editor** → Use `template_pyside6_editor.py`
4. **Search Plugin** → Use `template_search_plugin.py`

All templates are in the `templates/` directory.

## Script Usage

Helper scripts in `scripts/` directory:

1. **generate_plugin_scaffold.py** → Create complete project structure
2. **create_manifest.py** → Generate plugin store manifest
3. **test_plugin_locally.py** → Install and test plugin
4. **update_version.py** → Bump version across all files

## Resources

Reference materials in `resources/` directory:

1. **flow_launcher_api.md** → Complete API reference
2. **pyside6_patterns.md** → Common GUI patterns
3. **best_practices.md** → Comprehensive best practices
4. **example_plugins.md** → Real-world examples with explanations

## Success Criteria

A plugin is complete when:

- [x] Plugin loads in Flow Launcher without errors
- [x] Action keyword triggers correctly
- [x] Results display with proper formatting
- [x] Actions execute successfully
- [x] Context menu works (if applicable)
- [x] Editor works (if applicable)
- [x] Tests pass
- [x] Documentation is complete
- [x] GitHub Actions workflow is set up
- [x] Plugin store manifest is created
- [x] Code is committed to GitHub
- [x] Release v1.0.0 is created
- [x] Plugin works on a clean Windows installation

## Output Format

When creating a plugin:

1. **Confirm understanding** of requirements
2. **Show project structure** to be created
3. **Create all files** with complete, working code
4. **Provide testing instructions**
5. **Create submission guide** if requested
6. **Generate helper scripts** as needed

## Example Workflow

User: "I want a plugin to quickly access my frequently used folders"

AI Response:
1. Confirm: Data-driven plugin with JSON storage
2. Ask about GUI editor preference
3. Generate GUID
4. Create project structure
5. Implement plugin with shortcuts pattern
6. Create GUI editor (if requested)
7. Set up GitHub Actions
8. Create documentation
9. Provide testing instructions
10. Prepare plugin store submission

## Technical Notes

- **Tested on**: Windows 10/11, Python 3.8-3.12
- **Flow Launcher compatibility**: v1.9+
- **Required packages**: flowlauncher, PySide6 (for editors)
- **Build tools**: PyInstaller for standalone editors

## Version History

- **1.0.0** (2024-12-24): Initial skill based on Shortcuts plugin development

---

**Remember**: The goal is to democratize plugin creation. Make it easy, provide complete code, and ensure everything works out of the box!
