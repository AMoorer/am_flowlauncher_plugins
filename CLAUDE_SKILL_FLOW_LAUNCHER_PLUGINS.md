# Claude Skill: Flow Launcher Plugin Development

This document describes patterns and best practices for developing Flow Launcher plugins with Python, based on the Shortcuts plugin implementation.

## Overview

Flow Launcher is a Windows application launcher that supports custom plugins. Plugins communicate via JSON-RPC and can be written in Python, C#, JavaScript, or as executables.

## Core Architecture

### 1. Plugin Structure

**Required Files:**
```
Flow.Launcher.Plugin.YourPlugin/
├── main.py              # Entry point (must match ExecuteFileName)
├── plugin.json          # Plugin metadata
├── requirements.txt     # Python dependencies
└── Images/             # Icon resources
    └── app.png         # Default icon (must match IcoPath)
```

### 2. plugin.json Schema

```json
{
    "ID": "UNIQUE-GUID-HERE",
    "ActionKeyword": "s",
    "Name": "Plugin Name",
    "Description": "Short description",
    "Author": "Your Name",
    "Version": "1.0.0",
    "Language": "python",
    "Website": "https://github.com/you/plugin",
    "IcoPath": "Images\\app.png",
    "ExecuteFileName": "main.py"
}
```

**Key Fields:**
- `ID`: Unique GUID (generate online or use `str(uuid.uuid4())`)
- `ActionKeyword`: Trigger keyword (e.g., "s" → user types "s query")
- `Language`: "python" for Python plugins
- `IcoPath`: Relative path to default icon (use `\\` for Windows paths)
- `ExecuteFileName`: Entry point file

### 3. Main Plugin Class

```python
from flowlauncher import FlowLauncher

class YourPlugin(FlowLauncher):
    
    def __init__(self):
        super().__init__()
        # Initialize your plugin state
    
    def query(self, query):
        """
        Main query handler - called when user types keyword + query
        Must return list of result dictionaries
        """
        return [
            {
                "Title": "Result title",
                "SubTitle": "Description",
                "IcoPath": "path/to/icon.png",
                "Score": 100,  # Priority (higher = appears first)
                "JsonRPCAction": {
                    "method": "method_name",
                    "parameters": ["param1", "param2"]
                },
                "ContextData": "data_for_context_menu"
            }
        ]
    
    def context_menu(self, data):
        """
        Context menu handler - called on right-click
        'data' comes from ContextData in result
        """
        return [
            {
                "Title": "Context action",
                "SubTitle": "Description",
                "IcoPath": "icon.png",
                "JsonRPCAction": {
                    "method": "context_action",
                    "parameters": [data]
                }
            }
        ]
    
    def method_name(self, param1, param2):
        """Custom action methods"""
        # Do something
        pass

if __name__ == "__main__":
    YourPlugin()
```

## Result Object Structure

```python
{
    "Title": str,           # Main text (required)
    "SubTitle": str,        # Secondary text (optional)
    "IcoPath": str,        # Icon path - absolute or relative (optional)
    "Score": int,          # Priority 0-200 (optional, default ~50)
    "JsonRPCAction": {     # Action on Enter (optional)
        "method": str,      # Method name in your class
        "parameters": list  # Arguments to pass
    },
    "ContextData": any,    # Data passed to context_menu (optional)
    "AutoCompleteText": str # Text to autocomplete (optional)
}
```

## Common Patterns

### 1. File Operations

```python
import os
import subprocess

def open_folder(self, path):
    path = os.path.expandvars(path)  # Expand %ENVVARS%
    os.startfile(path)

def open_file(self, path):
    path = os.path.expandvars(path)
    os.startfile(path)

def open_file_with(self, file_path, app_path):
    file_path = os.path.expandvars(file_path)
    app_path = os.path.expandvars(app_path)
    subprocess.Popen([app_path, file_path])

def launch_app(self, app_path):
    app_path = os.path.expandvars(app_path)
    subprocess.Popen(app_path, shell=True)
```

### 2. URL Handling

```python
import webbrowser

def open_url(self, url):
    webbrowser.open(url)
```

### 3. Clipboard Access

```python
import subprocess

def copy_to_clipboard(self, text):
    try:
        import win32clipboard
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text)
        win32clipboard.CloseClipboard()
    except:
        # Fallback using PowerShell
        subprocess.run(
            ['powershell', '-command', f'Set-Clipboard -Value "{text}"'],
            capture_output=True, shell=True
        )
```

### 4. JSON Data Persistence

```python
import json
import os

class YourPlugin(FlowLauncher):
    
    def __init__(self):
        super().__init__()
        self.data_file = os.path.join(
            os.path.dirname(__file__), 
            'data.json'
        )
        self.data = self.load_data()
    
    def load_data(self):
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            self.logger.error(f"Load error: {e}")
            return {}
    
    def save_data(self):
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Save error: {e}")
            return False
```

### 5. Icon Resolution

```python
import os

def resolve_icon(self, icon_path):
    """Resolve icon path - handles relative and absolute paths"""
    if not icon_path:
        return "Images/default.png"
    
    if not os.path.isabs(icon_path):
        # Relative to plugin directory
        icon_path = os.path.join(
            os.path.dirname(__file__),
            icon_path
        )
    
    if not os.path.exists(icon_path):
        return "Images/default.png"
    
    return icon_path
```

### 6. Query Filtering

```python
def query(self, query):
    query_lower = query.lower().strip()
    results = []
    
    # Exact match first
    for item in self.items:
        if item['keyword'].lower() == query_lower:
            results.append(self.create_result(item, score=200))
    
    # Starts with
    for item in self.items:
        if item['keyword'].lower().startswith(query_lower):
            if item not in results:
                results.append(self.create_result(item, score=150))
    
    # Contains
    for item in self.items:
        if query_lower in item['keyword'].lower():
            if item not in results:
                results.append(self.create_result(item, score=100))
    
    return results
```

### 7. Error Handling

```python
def safe_action(self, param):
    """Wrap actions in try-except for robustness"""
    try:
        # Do action
        result = self.do_something(param)
        return result
    except Exception as e:
        self.logger.error(f"Action failed: {e}")
        # Optionally show error to user
        return None
```

## PySide6 GUI Editor Pattern

When building companion GUI editors:

### 1. Resource Path Helper

```python
import sys
from pathlib import Path

def resource_path(relative_path):
    """Get absolute path - works for dev and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = Path(__file__).parent
    return Path(base_path) / relative_path
```

### 2. Find Plugin Data File

```python
def find_data_file(self):
    """Locate plugin's data file from editor"""
    # Try sibling plugin directory
    plugin_dir = Path(__file__).parent.parent / 'Flow.Launcher.Plugin.YourPlugin'
    data_file = plugin_dir / 'data.json'
    
    if data_file.exists():
        return str(data_file)
    
    # Try Flow Launcher installation
    appdata = os.getenv('APPDATA')
    if appdata:
        fl_path = (Path(appdata) / 'FlowLauncher' / 'Plugins' / 
                   'Flow.Launcher.Plugin.YourPlugin' / 'data.json')
        if fl_path.exists():
            return str(fl_path)
    
    return str(data_file)  # Default
```

### 3. Settings Persistence

```python
from PySide6.QtCore import QSettings

class EditorWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.settings = QSettings('Author', 'AppName')
        self.restore_geometry()
    
    def restore_geometry(self):
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
    
    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())
        event.accept()
```

### 4. Form Dialog Pattern

```python
from PySide6.QtWidgets import QDialog, QFormLayout

class EditDialog(QDialog):
    
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.data = data or {}
        self.setup_ui()
        if data:
            self.load_data(data)
    
    def setup_ui(self):
        layout = QFormLayout()
        # Add form fields
        self.setLayout(layout)
    
    def load_data(self, data):
        """Load data into form"""
        pass
    
    def get_data(self):
        """Extract data from form"""
        return {}
```

## Installation & Distribution

### Dependencies

**Plugin requirements.txt:**
```
flowlauncher>=2.0.0
```

**Editor requirements.txt:**
```
PySide6>=6.6.0
```

### Installation Steps

1. **Copy plugin** to `%APPDATA%\FlowLauncher\Plugins\`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Restart Flow Launcher**

### PyInstaller Distribution (Editor)

```bash
pyinstaller --onefile --windowed --name ShortcutsEditor editor.py
```

## Testing

### 1. Local Testing

Create `test.py` in plugin directory:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from main import YourPlugin

if __name__ == '__main__':
    plugin = YourPlugin()
    
    # Test query
    results = plugin.query("test query")
    print("Results:", results)
    
    # Test action
    if results:
        action = results[0].get('JsonRPCAction')
        if action:
            method = action['method']
            params = action['parameters']
            getattr(plugin, method)(*params)
```

### 2. Flow Launcher Testing

1. Copy plugin to plugins directory
2. Restart Flow Launcher
3. Type action keyword
4. Check logs: `%APPDATA%\FlowLauncher\Logs\`

## Best Practices

### Code Organization

1. **Separate concerns**: Data loading, result creation, actions
2. **Use type hints**: Improves IDE support
3. **Error handling**: Wrap actions in try-except
4. **Logging**: Use `self.logger` for debugging
5. **JSON serialization**: Use `json.dumps()` for complex ContextData

### Performance

1. **Cache data**: Load once in `__init__`, not per query
2. **Lazy loading**: Load heavy resources only when needed
3. **Limit results**: Return max 10-20 results for speed
4. **Quick scoring**: Use simple integer scores, not complex calculations

### User Experience

1. **Clear titles**: Describe what will happen
2. **Informative subtitles**: Show paths, URLs, or details
3. **Consistent icons**: Use recognizable icons per type
4. **Smart defaults**: Provide sensible default values
5. **Context menus**: Offer edit, copy, delete options

### Data Management

1. **Use JSON**: Simple, readable, debuggable
2. **Validate input**: Check data exists and is correct type
3. **Backup on save**: Optional, but helpful for users
4. **Environment variables**: Support `%APPDATA%`, etc.
5. **Absolute paths**: Resolve relative paths early

## Common Pitfalls

### ❌ Don't

```python
# Don't block in query()
def query(self, query):
    time.sleep(5)  # BAD - freezes UI
    
# Don't return non-serializable objects
def query(self, query):
    return [MyCustomClass()]  # BAD
    
# Don't use relative imports incorrectly
from .module import func  # BAD in main.py
```

### ✅ Do

```python
# Return quickly
def query(self, query):
    return self.get_cached_results(query)

# Return dictionaries
def query(self, query):
    return [{"Title": "Item", "SubTitle": "..."}]

# Use absolute imports
from module import func  # OK
import module  # OK
```

## Example: Complete Mini Plugin

```python
# -*- coding: utf-8 -*-
import sys
import os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)

from flowlauncher import FlowLauncher
import webbrowser

class QuickLinks(FlowLauncher):
    
    def __init__(self):
        super().__init__()
        self.links = {
            'github': 'https://github.com',
            'google': 'https://google.com',
            'gmail': 'https://gmail.com'
        }
    
    def query(self, query):
        query = query.lower().strip()
        results = []
        
        for keyword, url in self.links.items():
            if not query or query in keyword:
                results.append({
                    "Title": keyword,
                    "SubTitle": url,
                    "IcoPath": "Images/link.png",
                    "JsonRPCAction": {
                        "method": "open_url",
                        "parameters": [url]
                    }
                })
        
        return results
    
    def open_url(self, url):
        webbrowser.open(url)

if __name__ == "__main__":
    QuickLinks()
```

## Resources

- **Flow Launcher Docs**: https://www.flowlauncher.com/docs/
- **Python Template**: https://github.com/Flow-Launcher/Flow.Launcher.Plugin.PythonTemplate
- **pyFlowLauncher**: https://github.com/Garulf/pyFlowLauncher
- **Plugin Examples**: Search GitHub for "Flow.Launcher.Plugin"

## Workflow Summary

1. **Plan**: Define keywords, actions, data structure
2. **Create Structure**: plugin.json, main.py, Images/
3. **Implement Query**: Return results based on user input
4. **Implement Actions**: Methods called by JsonRPCAction
5. **Add Context Menu**: Right-click functionality
6. **Test Locally**: Use test script
7. **Test in Flow**: Install and verify
8. **Create Editor** (optional): PySide6 GUI for data management
9. **Document**: README with usage and installation

---

*This skill document is maintained alongside the Flow.Launcher.Plugin.Shortcuts reference implementation.*
