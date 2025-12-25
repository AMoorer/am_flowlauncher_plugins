# Changelog

All notable changes to the Flow Launcher Shortcuts Plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-24

### Added
- Initial release of Flow Launcher Shortcuts Plugin
- Core plugin functionality:
  - Support for folder, file, app, and URL shortcuts
  - Custom keywords for quick access
  - Priority-based result ordering
  - Category organization (Folders, Files, Apps, custom categories)
  - Custom icon support
  - Context menu actions (Edit, Copy, Delete)
  - `shortcutlist` command to view all shortcuts by category
  - Environment variable expansion in paths
  
- GUI Editor features:
  - PySide6-based desktop application
  - Table view for all shortcuts
  - Add/Edit/Delete operations
  - Browser bookmark import from Chrome, Edge, Opera, Brave
  - Custom save location support
  - Icon picker with preview
  - Priority control (0-200)
  - Dark mode support
  - About dialog with usage instructions
  - Auto-save functionality
  
- Documentation:
  - Comprehensive README
  - Quick start guide
  - Project structure documentation
  - Claude development skill reference
  - Installation scripts
  
- Build tools:
  - PyInstaller build script for standalone .exe
  - Sync script for development
  - Test suite

### Features Breakdown

#### Plugin (Flow.Launcher.Plugin.Shortcuts)
- JSON-RPC communication via FlowLauncher base class
- Smart action execution based on shortcut type
- Invisible zero-width character ordering for category display
- Result scoring system for proper list ordering
- Clipboard integration for copy actions
- Editor launching from within Flow Launcher

#### Editor (ShortcutsEditor)
- Modern Qt-based GUI with responsive design
- Multi-browser bookmark parsing (Chromium-based browsers)
- Automatic keyword generation from bookmark names
- Duplicate keyword handling
- Folder-based category mapping from bookmarks
- Settings persistence (window geometry, custom save location)
- Comprehensive About dialog
- File menu with save location management
- Help menu with usage documentation

### Technical Details
- Python 3.8+ compatibility
- PySide6 6.6.0+ for GUI
- flowlauncher 0.2.0+ for plugin integration
- JSON-based data storage
- Cross-application data sharing
- Windows environment variable support

### Known Limitations
- Windows only (uses Windows-specific shell commands)
- Chromium-based browsers only for bookmark import
- Relative icon paths resolved from plugin directory

## [Unreleased]

### Planned Features
- Firefox bookmark import support
- Bulk edit operations
- Import/export shortcuts to JSON
- Shortcut search/filter in editor
- Keyboard shortcuts in editor
- Drag-and-drop file/folder support
- Icon download from URLs
- Shortcut usage statistics
- Categories management dialog
- Multi-language support

---

For more information, visit: https://github.com/AMoorer/am_flowlauncher_plugins
