---
description: Create a new Flow Launcher plugin with Python and PySide6
---

# Create Flow Launcher Plugin Workflow

Use this workflow to create new Flow Launcher plugins based on the Shortcuts plugin pattern.

## Prerequisites

- Review `CLAUDE_SKILL_FLOW_LAUNCHER_PLUGINS.md` for patterns
- Check existing `Flow.Launcher.Plugin.Shortcuts` as reference

## Step 1: Define Plugin Concept

Ask user for:
- Plugin name (e.g., "QuickNotes")
- Action keyword (e.g., "qn")
- Core functionality description
- Data structure needs
- Whether GUI editor is needed

## Step 2: Create Plugin Structure

```bash
mkdir Flow.Launcher.Plugin.{Name}
mkdir Flow.Launcher.Plugin.{Name}/Images
```

Create files:
- `plugin.json` - Generate unique GUID, set metadata
- `main.py` - Plugin class inheriting from FlowLauncher
- `requirements.txt` - Add flowlauncher dependency
- `data.json` or `{name}.json` - Data file if needed
- `.gitignore` - Standard Python gitignore

## Step 3: Implement Core Plugin

In `main.py`:

1. **Import and Setup**
   ```python
   from flowlauncher import FlowLauncher
   import json, os
   ```

2. **Class Structure**
   - `__init__()` - Load data, initialize state
   - `query(query)` - Main search/filter logic
   - `context_menu(data)` - Right-click options
   - Action methods as needed

3. **Data Management**
   - `load_data()` - Read from JSON
   - `save_data()` - Write to JSON
   - Error handling

4. **Result Creation**
   - Create result dictionaries
   - Set titles, subtitles, icons
   - Configure JsonRPCAction

## Step 4: Create GUI Editor (if needed)

```bash
mkdir {Name}Editor
```

In `editor.py`:

1. **Main Window** (QMainWindow)
   - Table/List view of items
   - Add/Edit/Delete buttons
   - Load/Save functionality

2. **Edit Dialog** (QDialog)
   - Form layout for fields
   - Validation
   - File browsers if needed

3. **Data Integration**
   - Find plugin data file
   - Shared JSON format
   - Auto-save on changes

4. **Supporting Files**
   - `requirements.txt` - PySide6
   - `launch_editor.bat` - Launcher script

## Step 5: Create Documentation

1. **README.md**
   - Features overview
   - Installation instructions
   - Usage examples
   - Data format
   - Troubleshooting

2. **QUICKSTART.md** (optional)
   - 5-minute setup guide
   - Essential examples

3. **Example Data**
   - `data_example.json` with samples

## Step 6: Add Supporting Files

1. **test.py**
   - Query tests
   - Data operation tests
   - Action tests

2. **install_plugin.bat**
   - Automated installer
   - Dependency installation
   - Post-install instructions

3. **Icons**
   - Create `Images/ICONS_NEEDED.txt`
   - List required icons
   - Suggest sources

## Step 7: Testing

// turbo
1. Run test script:
   ```bash
   cd Flow.Launcher.Plugin.{Name}
   python test.py
   ```

2. Test with Flow Launcher:
   - Copy to `%APPDATA%\FlowLauncher\Plugins`
   - Restart Flow Launcher
   - Test action keyword

3. Test editor (if applicable):
   ```bash
   cd {Name}Editor
   python editor.py
   ```

## Key Patterns to Follow

### Query Method
```python
def query(self, query):
    results = []
    # Filter/search logic
    # Sort by relevance/priority
    return results
```

### Result Format
```python
{
    "Title": "Main text",
    "SubTitle": "Description",
    "IcoPath": "path/to/icon.png",
    "Score": 100,
    "JsonRPCAction": {
        "method": "method_name",
        "parameters": ["param"]
    },
    "ContextData": "data"
}
```

### Action Method
```python
def action_name(self, param):
    try:
        # Do action
        pass
    except Exception as e:
        self.logger.error(f"Error: {e}")
```

### Context Menu
```python
def context_menu(self, data):
    return [
        {
            "Title": "Action",
            "SubTitle": "Description",
            "JsonRPCAction": {
                "method": "action",
                "parameters": [data]
            }
        }
    ]
```

## Common Integrations

### File Operations
- `os.startfile(path)` - Open file/folder
- `subprocess.Popen([app, file])` - Open with app

### URLs
- `webbrowser.open(url)` - Open in browser

### Clipboard
- `win32clipboard` or PowerShell fallback

### Environment Variables
- `os.path.expandvars(path)` - Expand %VARS%

## Checklist

- [ ] Plugin structure created
- [ ] plugin.json configured with unique GUID
- [ ] main.py implements query() and actions
- [ ] Data loading/saving works
- [ ] Icons specified (ICONS_NEEDED.txt)
- [ ] test.py runs successfully
- [ ] README.md written
- [ ] install_plugin.bat created
- [ ] GUI editor implemented (if needed)
- [ ] Tested in Flow Launcher
- [ ] Documentation complete

## Reference Files

Always refer to:
- `Flow.Launcher.Plugin.Shortcuts/main.py` - Plugin example
- `ShortcutsEditor/editor.py` - GUI example
- `CLAUDE_SKILL_FLOW_LAUNCHER_PLUGINS.md` - Patterns
- Flow Launcher docs: https://www.flowlauncher.com/docs/

## Tips

1. Start simple, add features iteratively
2. Test frequently during development
3. Use example shortcuts as starting point
4. Keep JSON schema simple
5. Validate all user input
6. Provide clear error messages
7. Use environment variables for paths
8. Document data format clearly

---

*This workflow was created based on the Shortcuts plugin implementation.*
