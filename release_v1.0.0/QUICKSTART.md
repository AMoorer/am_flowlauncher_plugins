# Quick Start Guide

Get the Shortcuts plugin running in 5 minutes!

## Prerequisites

- Windows 10/11
- Flow Launcher installed
- Python 3.8+ installed
- pip available

## Installation Steps

### 1. Install Plugin

```powershell
# Navigate to Flow Launcher plugins directory
cd %APPDATA%\FlowLauncher\Plugins

# Copy the plugin folder
xcopy /E /I "c:\Users\andym\develop\repositories\am_flowlauncher_plugins\Flow.Launcher.Plugin.Shortcuts" "Flow.Launcher.Plugin.Shortcuts"

# Install Python dependencies
cd Flow.Launcher.Plugin.Shortcuts
pip install -r requirements.txt
```

### 2. Setup Icons

Add icon files to `Flow.Launcher.Plugin.Shortcuts\Images\` directory:
- shortcut.png
- folder.png
- file.png
- app.png
- bookmark.png
- copy.png
- delete.png

See `Images\ICONS_NEEDED.txt` for details and sources.

### 3. Restart Flow Launcher

- Right-click Flow Launcher tray icon
- Select "Restart"

### 4. Test Plugin

- Open Flow Launcher (Alt+Space by default)
- Type: `s shortcutlist`
- Should see empty list or example shortcuts

## Using the Editor

### 1. Install Editor Dependencies

```powershell
cd c:\Users\andym\develop\repositories\am_flowlauncher_plugins\ShortcutsEditor
pip install -r requirements.txt
```

### 2. Launch Editor

```powershell
# Option 1: Double-click
launch_editor.bat

# Option 2: Command line
python editor.py
```

### 3. Add Your First Shortcut

1. Click **"Add Shortcut"**
2. Fill in:
   - **Keyword**: `docs`
   - **Type**: `folder`
   - **Path**: Browse to your Documents folder
   - **Category**: `Folders`
   - **Priority**: `100`
3. Click **"Save"**

### 4. Test in Flow Launcher

- Open Flow Launcher
- Type: `s docs`
- Press Enter → Documents folder opens!

## Example Shortcuts to Add

### Folder Shortcuts

| Keyword | Type | Path |
|---------|------|------|
| `docs` | folder | `%USERPROFILE%\Documents` |
| `downloads` | folder | `%USERPROFILE%\Downloads` |
| `desktop` | folder | `%USERPROFILE%\Desktop` |
| `projects` | folder | `C:\Dev\Projects` |

### App Shortcuts

| Keyword | Type | Path |
|---------|------|------|
| `vscode` | app | `%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe` |
| `notepad` | app | `notepad.exe` |
| `chrome` | app | `%PROGRAMFILES%\Google\Chrome\Application\chrome.exe` |

### URL Shortcuts

| Keyword | Type | Path | Category |
|---------|------|------|----------|
| `github` | url | `https://github.com` | Development |
| `gmail` | url | `https://mail.google.com` | Productivity |
| `youtube` | url | `https://youtube.com` | Media |
| `chatgpt` | url | `https://chat.openai.com` | AI Tools |

### File Shortcuts

| Keyword | Type | Path | Open With |
|---------|------|------|-----------|
| `todos` | file | `%USERPROFILE%\Documents\todos.txt` | `notepad.exe` |
| `budget` | file | `C:\Finance\budget.xlsx` | *leave empty for default app* |

## Tips

### Use Environment Variables

Instead of hardcoding paths:
- ❌ `C:\Users\YourName\Documents`
- ✅ `%USERPROFILE%\Documents`

Common variables:
- `%USERPROFILE%` - User home directory
- `%APPDATA%` - Application data
- `%LOCALAPPDATA%` - Local application data
- `%PROGRAMFILES%` - Program Files
- `%TEMP%` - Temp directory

### Priority Weights

Set priorities to control order:
- **120-200**: Most important (always at top)
- **80-119**: High priority
- **50-79**: Normal priority
- **0-49**: Low priority

### Organize by Category

Group related shortcuts:
- **Folders**: All folder shortcuts
- **Files**: All file shortcuts
- **Apps**: All application shortcuts
- **Development**: Dev-related URLs
- **Social**: Social media URLs
- **Media**: Entertainment URLs

### Context Menu (Right-Click)

Right-click any result in Flow Launcher:
- **Open Shortcuts Editor**: Edit this shortcut
- **Copy Path**: Copy the path/URL
- **Delete Shortcut**: Remove from list

## Testing Commands

### View All Shortcuts
```
s shortcutlist
```

### Filter by Category
```
s shortcutlist folders
s shortcutlist dev
```

### Search by Keyword
```
s doc    (finds: docs, documents, etc.)
s vs     (finds: vscode)
```

## Troubleshooting

### Plugin doesn't appear

1. Check plugin installed to: `%APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts`
2. Verify `plugin.json` exists
3. Check Python dependencies: `pip install flowlauncher`
4. Restart Flow Launcher

### Editor can't find shortcuts.json

The editor looks in:
1. `../Flow.Launcher.Plugin.Shortcuts/shortcuts.json` (development)
2. `%APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts\shortcuts.json` (installed)

Create the file if it doesn't exist:
```json
{
  "shortcuts": []
}
```

### Shortcut doesn't work

1. **Test path** - Open manually to verify it exists
2. **Check environment variables** - Expand them in your mind
3. **View logs** - Check `%APPDATA%\FlowLauncher\Logs\` for errors

### Icons missing

1. Add icon files to `Images\` directory
2. Use absolute paths for custom icons
3. Plugin uses `Images/shortcut.png` as fallback

## Next Steps

1. **Add 10 shortcuts** you use daily
2. **Customize icons** for better visual recognition
3. **Share shortcuts** - export `shortcuts.json` to backup or share
4. **Explore context menus** - right-click for more options
5. **Set up categories** - organize by workflow

## Load Example Data

Want to start with examples?

```powershell
# Copy example shortcuts
cd %APPDATA%\FlowLauncher\Plugins\Flow.Launcher.Plugin.Shortcuts
copy shortcuts_example.json shortcuts.json

# Restart Flow Launcher
# Then type: s shortcutlist
```

## Support

- Check `README.md` for detailed documentation
- Review `CLAUDE_SKILL_FLOW_LAUNCHER_PLUGINS.md` for development patterns
- See Flow Launcher logs for debugging

---

Happy shortcutting! 🚀
