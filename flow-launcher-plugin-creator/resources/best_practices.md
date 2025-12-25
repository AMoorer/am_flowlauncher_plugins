# Flow Launcher Plugin Best Practices

Comprehensive best practices learned from real-world plugin development.

## 🎯 Result Ordering

### The Problem
Flow Launcher may not respect the `Score` field for result ordering, leading to unpredictable list order.

### The Solution: Invisible Unicode Prefixes
```python
def generate_sort_prefix(priority: int) -> str:
    """Generate invisible Unicode prefix for reliable sorting"""
    zwsp = '\u200b'  # Zero-Width Space
    count = 200 - priority  # Higher priority = fewer chars = sorts first
    return zwsp * count

# Usage:
{
    "Title": f"{generate_sort_prefix(100)}My Item",
    "SubTitle": "Description",
    # ...
}
```

### Alternative: Visible Numeric Prefixes
```python
"Title": f"{priority:03d}. My Item"
```

## 📁 File Operations

### Atomic Writes
Always use atomic writes to prevent data corruption:

```python
import tempfile, os, json

def save_data_safely(data, filepath):
    """Save JSON with atomic write."""
    # Write to temp file first
    with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        temp_path = f.name
    
    # Replace original atomically (Windows-safe)
    try:
        os.replace(temp_path, filepath)
    except Exception as e:
        os.unlink(temp_path)  # Clean up temp file
        raise e
```

### Environment Variables
Always expand environment variables in paths:

```python
import os

def expand_path(path):
    """Expand environment variables and resolve path."""
    path = os.path.expandvars(path)  # %USERPROFILE% -> C:\Users\Name
    path = os.path.expanduser(path)  # ~ -> home directory
    return os.path.abspath(path)
```

## 🖼️ Icon Handling

### Plugin Icons
```python
# Relative to plugin directory (recommended)
"IcoPath": "Images/icon.png"

# Absolute path (works but less portable)
"IcoPath": "C:\\Users\\Name\\Icons\\icon.png"

# Dynamic icon selection
def get_icon_for_type(item_type):
    icons = {
        'folder': 'Images/folder.png',
        'file': 'Images/file.png',
        'url': 'Images/bookmark.png',
        'app': 'Images/app.png'
    }
    return icons.get(item_type, 'Images/icon.png')
```

### Plugin Store Icons
Use CDN for plugin store manifest:
```python
"IcoPath": "https://cdn.jsdelivr.net/gh/user/repo@main/Images/icon.png"
```

## ⚡ Performance Optimization

### Load Data Once
```python
class MyPlugin(FlowLauncher):
    def __init__(self):
        # Load data BEFORE calling super().__init__()
        self.data = self.load_data()
        super().__init__()
    
    def query(self, query):
        # Use self.data (already loaded)
        # Don't reload on every query!
        pass
```

### Limit Results
```python
def query(self, query):
    results = self.search_data(query)
    # Limit to reasonable number
    return results[:50]  # Max 50 results
```

### Cache Expensive Operations
```python
from functools import lru_cache
import hashlib

class MyPlugin(FlowLauncher):
    @lru_cache(maxsize=100)
    def expensive_operation(self, query):
        # This result will be cached
        return compute_something(query)
```

## 🛡️ Error Handling

### User-Friendly Errors
```python
def query(self, query):
    try:
        results = self.process_query(query)
        return results
    except FileNotFoundError:
        return [{
            "Title": "Data file not found",
            "SubTitle": "Please run the editor to create data",
            "IcoPath": "Images/error.png"
        }]
    except Exception as e:
        self.logger.error(f"Unexpected error: {e}")
        return [{
            "Title": "An error occurred",
            "SubTitle": "Check Flow Launcher logs for details",
            "IcoPath": "Images/error.png"
        }]
```

### Graceful Degradation
```python
def load_data(self):
    """Load data with fallback to empty list."""
    try:
        with open(self.data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('items', [])
    except FileNotFoundError:
        self.logger.warning("Data file not found, using empty list")
        return []
    except json.JSONDecodeError as e:
        self.logger.error(f"Invalid JSON: {e}")
        return []
    except Exception as e:
        self.logger.error(f"Error loading data: {e}")
        return []
```

## 🖥️ Windows Compatibility

### Path Separators
```python
# Use os.path.join for cross-platform paths
config_path = os.path.join(plugin_dir, 'config.json')

# JSON: Use double backslashes
{"path": "C:\\\\Users\\\\Name\\\\Documents"}

# Or use forward slashes (Windows accepts both)
{"path": "C:/Users/Name/Documents"}
```

### Console Encoding
```python
# For test scripts, use ASCII output
def print_result(success):
    # Don't use: ✓ ✗ (Unicode)
    # Use: [OK] [FAIL] (ASCII)
    status = "[OK]" if success else "[FAIL]"
    print(f"{status} Test completed")
```

### File Operations
```python
# Always use encoding='utf-8'
with open(filepath, 'r', encoding='utf-8') as f:
    data = f.read()

# Handle long paths (>260 chars)
if len(filepath) > 260:
    filepath = '\\\\?\\' + os.path.abspath(filepath)
```

## 🎨 GUI Editor Best Practices

### Dark Mode Support
```python
# DON'T hardcode colors
label.setStyleSheet("background: #f0f0f0;")  # ❌

# DO use system palette
label.setStyleSheet("padding: 10px;")  # ✅
```

### Settings Persistence
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

### Input Validation
```python
def validate_input(self):
    """Validate form input before saving."""
    if not self.name_input.text().strip():
        QMessageBox.warning(self, "Error", "Name is required")
        return False
    
    if not self.path_input.text().strip():
        QMessageBox.warning(self, "Error", "Path is required")
        return False
    
    # Validate path exists
    path = self.path_input.text()
    if not os.path.exists(os.path.expandvars(path)):
        reply = QMessageBox.question(
            self, "Warning",
            "Path does not exist. Save anyway?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.No:
            return False
    
    return True
```

## 🧪 Testing

### Automated Tests
```python
"""test.py - Plugin test suite"""

import sys
import os

# Setup path
sys.path.insert(0, os.path.dirname(__file__))

def test_query_empty():
    """Test empty query."""
    from main import MyPlugin
    plugin = MyPlugin()
    results = plugin.query("")
    assert len(results) > 0, "Should return help message"
    print("[OK] Empty query test passed")

def test_query_with_input():
    """Test query with input."""
    from main import MyPlugin
    plugin = MyPlugin()
    results = plugin.query("test")
    assert isinstance(results, list), "Results should be a list"
    print("[OK] Query test passed")

def test_result_format():
    """Test result format."""
    from main import MyPlugin
    plugin = MyPlugin()
    results = plugin.query("test")
    
    for result in results:
        assert 'Title' in result, "Result must have Title"
        assert 'SubTitle' in result, "Result must have SubTitle"
        assert 'IcoPath' in result, "Result must have IcoPath"
    
    print("[OK] Result format test passed")

if __name__ == "__main__":
    print("Running plugin tests...")
    test_query_empty()
    test_query_with_input()
    test_result_format()
    print("\\nAll tests passed!")
```

### Manual Testing Checklist
- [ ] Plugin loads without errors
- [ ] Action keyword triggers correctly
- [ ] Empty query shows help/default results
- [ ] Query with input returns relevant results
- [ ] Clicking results executes correct actions
- [ ] Context menu appears on right-click
- [ ] Context menu actions work
- [ ] Icons display correctly
- [ ] Editor opens (if applicable)
- [ ] Editor can add/edit/delete items
- [ ] Changes persist after Flow Launcher restart
- [ ] No console errors in Flow Launcher logs

## 📦 Packaging

### PyInstaller for GUI Editors
```bash
python -m PyInstaller --noconfirm \\
    --onefile \\
    --windowed \\
    --name "EditorName" \\
    --hidden-import "PySide6.QtCore" \\
    --hidden-import "PySide6.QtGui" \\
    --hidden-import "PySide6.QtWidgets" \\
    --exclude-module "matplotlib" \\
    --exclude-module "scipy" \\
    --exclude-module "pandas" \\
    --exclude-module "numpy" \\
    editor.py
```

### Plugin ZIP Structure
```
Flow.Launcher.Plugin.Name.zip
├── main.py
├── plugin.json
├── requirements.txt
├── data.json (if applicable)
└── Images/
    └── icon.png
```

## 🔄 Version Management

### Semantic Versioning
- **MAJOR** (1.0.0 → 2.0.0): Breaking changes
- **MINOR** (1.0.0 → 1.1.0): New features, backward compatible
- **PATCH** (1.0.0 → 1.0.1): Bug fixes

### Files to Update
When releasing a new version, update:
1. `plugin.json` → Version field
2. `editor.py` → About dialog (if applicable)
3. `CHANGELOG.md` → Add release notes
4. `README.md` → Update version badge (if using)

## 📖 Documentation

### README Template
```markdown
# Plugin Name

Description of what the plugin does.

## Features
- Feature 1
- Feature 2

## Installation
1. Download from releases
2. Extract to plugins directory
3. Install dependencies
4. Restart Flow Launcher

## Usage
- Command 1: Description
- Command 2: Description

## Configuration
How to configure (if applicable)

## Troubleshooting
Common issues and solutions

## License
MIT License
```

### Code Documentation
```python
def method_name(self, param):
    """
    Short description of what the method does.
    
    Args:
        param (type): Description of parameter
        
    Returns:
        type: Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
    pass
```

## 🔐 Security

### Input Validation
```python
def execute_command(self, command):
    """Execute command with validation."""
    # Validate command is in allowlist
    allowed_commands = ['open', 'copy', 'delete']
    if command not in allowed_commands:
        self.logger.warning(f"Attempted invalid command: {command}")
        return False
    
    # Execute safely
    # ...
```

### Path Traversal Prevention
```python
def load_file(self, filename):
    """Load file with path traversal prevention."""
    # Get absolute paths
    base_dir = os.path.abspath(self.data_dir)
    file_path = os.path.abspath(os.path.join(base_dir, filename))
    
    # Ensure file is within base directory
    if not file_path.startswith(base_dir):
        raise ValueError("Invalid file path")
    
    # Load safely
    with open(file_path, 'r') as f:
        return f.read()
```

## 🎓 Learning Resources

- **Flow Launcher Docs**: https://www.flowlauncher.com/docs/
- **Python flowlauncher Package**: https://pypi.org/project/flowlauncher/
- **PySide6 Documentation**: https://doc.qt.io/qtforpython/
- **Plugin Examples**: https://github.com/Flow-Launcher/Flow.Launcher.Plugin.HelloWorldPython

---

**Remember**: These practices come from real-world plugin development. Following them will save you hours of debugging!
