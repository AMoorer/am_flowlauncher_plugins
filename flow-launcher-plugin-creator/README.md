# Flow Launcher Plugin Creator - Claude Skill

A comprehensive Claude skill for creating professional Flow Launcher plugins with Python, including GUI editors, automation, and plugin store submission.

## 📖 Overview

This skill democratizes Flow Launcher plugin creation by providing AI assistants with:
- Complete plugin architecture knowledge
- Production-ready templates
- Automated scaffolding scripts
- Best practices from real-world development
- GUI editor patterns with PySide6
- Plugin store submission automation

## 📂 Structure

```
flow-launcher-plugin-creator/
├── SKILL.md                          # Main skill document
├── README.md                         # This file
├── templates/                        # Code templates
│   ├── template_basic_plugin.py      # Simple query-response plugin
│   ├── template_shortcuts_plugin.py  # Data-driven plugin pattern
│   └── template_pyside6_editor.py    # GUI editor template
├── scripts/                          # Helper automation scripts
│   ├── generate_plugin_scaffold.py   # Create complete project structure
│   └── create_manifest.py            # Generate plugin store manifest
└── resources/                        # Reference documentation
    └── best_practices.md             # Comprehensive best practices
```

## 🚀 Quick Start

### For Claude Desktop Users

1. Download or clone this skill folder
2. In Claude Desktop: Settings → Features → Add Custom Skill
3. Select the `flow-launcher-plugin-creator` folder
4. Claude will now have plugin creation capabilities!

### For Developers

Reference the templates and best practices when creating plugins manually.

## 💡 What This Skill Enables

### For Users
Ask Claude to:
- "Create a Flow Launcher plugin for quick access to my documents"
- "Add a GUI editor to my existing plugin"
- "Help me submit my plugin to the Flow Launcher store"
- "Generate a shortcuts plugin with bookmark import"

### For AI Assistants
This skill provides:
- **Architecture Knowledge**: JSON-RPC, result formatting, context menus
- **Development Patterns**: Data-driven, search, action, calculator plugins
- **Critical Solutions**: Result ordering with invisible Unicode prefixes
- **Complete Templates**: Ready-to-use code for common plugin types
- **Best Practices**: File operations, error handling, Windows compatibility
- **Automation**: Scripts for scaffolding, testing, and deployment

## 📚 Key Knowledge Areas

### 1. Plugin Architecture
- Flow Launcher communication via JSON-RPC
- FlowLauncher base class usage
- Result format and scoring
- Context menu implementation

### 2. Development Patterns
- **Data-Driven** (Shortcuts, Bookmarks)
- **Dynamic Search** (APIs, File System)
- **Action Plugins** (System Operations)
- **Calculator/Converter** (Transform Input)

### 3. GUI Editor Development
- PySide6 application structure
- Dark mode support
- Settings persistence
- Data synchronization

### 4. Build & Release
- GitHub Actions workflows
- PyInstaller for standalone editors
- Release automation
- Plugin store submission

### 5. Critical Fixes
- **Result Ordering**: Invisible Unicode prefix solution
- **Atomic Writes**: Prevent data corruption
- **Path Handling**: Environment variables and Windows paths
- **Error Handling**: User-friendly error messages

## 🎯 Use Cases

This skill handles:

### Plugin Creation
- ✅ New plugin from scratch
- ✅ Complete project structure
- ✅ Working code out of the box
- ✅ Test suite included

### GUI Editors
- ✅ PySide6 desktop applications
- ✅ Table views with CRUD operations
- ✅ Dark mode support
- ✅ Settings persistence

### Automation
- ✅ GitHub Actions workflows
- ✅ Automated builds
- ✅ Release packaging
- ✅ Store manifest generation

### Plugin Store
- ✅ Manifest file creation
- ✅ Fork and PR automation
- ✅ Submission guide

## 🛠️ Templates Included

### 1. Basic Plugin (`template_basic_plugin.py`)
Simple query-response pattern with:
- Query handling
- Result formatting
- Context menu
- Clipboard integration

### 2. Shortcuts Plugin (`template_shortcuts_plugin.py`)
Data-driven pattern with:
- JSON data storage
- Category grouping
- List view
- CRUD operations via context menu
- Multiple shortcut types (folder, file, app, url)

### 3. PySide6 Editor (`template_pyside6_editor.py`)
Full-featured GUI editor with:
- Table view of data
- Add/Edit/Delete dialogs
- Browse buttons for files
- Menu bar (File, Help)
- About dialog
- Settings persistence
- Dark mode support

## 📖 Scripts Included

### 1. Plugin Scaffold Generator
```bash
python scripts/generate_plugin_scaffold.py
```
Creates complete plugin project structure with all necessary files.

### 2. Manifest Creator
```bash
python scripts/create_manifest.py Flow.Launcher.Plugin.Name 1.0.0
```
Generates plugin store manifest file ready for submission.

## 🎓 Learning from Real Development

This skill is based on the actual development of the **Shortcuts plugin**, which includes:
- Browser bookmark import (Chrome, Edge, Opera, Brave)
- GUI editor with PySide6
- Category organization with priority ordering
- Custom save locations
- Complete plugin store submission

All patterns, solutions, and best practices come from real-world experience.

## 📋 Best Practices Covered

### Performance
- Load data once in `__init__`
- Cache expensive operations
- Limit result counts

### Reliability
- Atomic file writes
- Graceful error handling
- Input validation

### Compatibility
- Environment variable expansion
- Windows path handling
- Python 3.8+ support
- Console encoding (ASCII for tests)

### User Experience
- Dark mode support in editors
- Settings persistence
- User-friendly error messages
- Comprehensive documentation

## 🔗 Related Resources

- **Flow Launcher**: https://www.flowlauncher.com/
- **Plugin Docs**: https://www.flowlauncher.com/docs/
- **Plugin Store**: https://github.com/Flow-Launcher/Flow.Launcher.PluginsManifest
- **Example Plugin**: https://github.com/AMoorer/am_flowlauncher_plugins

## 📝 Example Usage

**User Request:**
> "I want a plugin to quickly access my frequently used folders and files"

**AI Response (with this skill):**
1. Confirms requirements (data-driven plugin with JSON storage)
2. Asks about GUI editor preference
3. Generates unique GUID
4. Creates complete project structure:
   - `main.py` with shortcuts pattern
   - `plugin.json` with metadata
   - `requirements.txt` with dependencies
   - GUI editor (if requested)
   - Test suite
   - GitHub Actions workflow
   - Complete documentation
5. Provides testing instructions
6. Creates plugin store submission guide

**Result:** A complete, working plugin ready to use and share!

## 🎯 Success Metrics

A plugin created with this skill is complete when:
- ✅ Loads in Flow Launcher without errors
- ✅ Action keyword triggers correctly
- ✅ Results display and execute properly
- ✅ Tests pass
- ✅ Editor works (if applicable)
- ✅ Documentation is complete
- ✅ GitHub Actions workflow is set up
- ✅ Ready for plugin store submission

## 🤝 Contributing

This skill is open source and welcomes improvements:
- Additional plugin patterns
- More templates
- Enhanced automation scripts
- Better documentation

## 📄 License

MIT License - Free to use, modify, and distribute.

## 👤 Author

Created by **Andy Moorer** based on real-world Flow Launcher plugin development experience.

- GitHub: [@AMoorer](https://github.com/AMoorer)
- Example Plugin: [Shortcuts Plugin](https://github.com/AMoorer/am_flowlauncher_plugins)

## 🌟 Version

**1.0.0** (2024-12-24)
- Initial release based on Shortcuts plugin development
- Complete architecture knowledge
- Production-ready templates
- Automation scripts
- Comprehensive best practices

---

**Democratizing Flow Launcher plugin creation, one AI conversation at a time!** 🚀
