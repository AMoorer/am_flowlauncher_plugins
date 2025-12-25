# GitHub Repository Setup Guide

Follow these steps to publish your Flow Launcher Shortcuts Plugin to GitHub.

## Prerequisites

- GitHub account
- Git installed on your system
- Repository files ready (you have them!)

## Step-by-Step GitHub Setup

### 1. Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `am_flowlauncher_plugins`
   - **Description**: `A powerful Flow Launcher plugin for quick access to folders, files, apps, and URLs with browser bookmark import`
   - **Visibility**: Public
   - **Initialize**: 
     - ❌ Do NOT add README (we have one)
     - ❌ Do NOT add .gitignore (we have one)
     - ✅ Add MIT License (or use the LICENSE file we created)
3. Click **"Create repository"**

### 2. Initialize Local Git Repository

Open PowerShell in your project directory:

```powershell
cd c:\Users\andym\develop\repositories\am_flowlauncher_plugins

# Initialize git (if not already)
git init

# Add all files
git add .

# First commit
git commit -m "Initial release: Flow Launcher Shortcuts Plugin v1.0.0

Features:
- Quick access to folders, files, apps, and URLs
- Browser bookmark import (Chrome, Edge, Opera, Brave)
- PySide6 GUI editor with dark mode support
- Category organization and priority system
- Custom save location and icon support
"

# Add GitHub remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/am_flowlauncher_plugins.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Rename Files (Clean Up)

Before pushing, rename the new files to replace the old ones:

```powershell
# Backup originals (optional)
copy README.md README_OLD.md
copy ShortcutsEditor\build_exe.bat ShortcutsEditor\build_exe_OLD.bat

# Replace with new versions
move /Y README_NEW.md README.md
move /Y ShortcutsEditor\build_exe_NEW.bat ShortcutsEditor\build_exe.bat

# Remove temporary files
del README_NEW.md 2>NUL
del ShortcutsEditor\build_exe_NEW.bat 2>NUL

# Commit the updates
git add .
git commit -m "Update documentation and build scripts"
git push
```

### 4. Create First Release

#### Build Release Artifacts

```powershell
# Run the release packager
create_release.bat

# This creates:
# - release_v1.0.0/ShortcutsEditor.exe
# - release_v1.0.0/Flow.Launcher.Plugin.Shortcuts.zip
# - release_v1.0.0/README.md
# - release_v1.0.0/CHANGELOG.md
```

#### Create GitHub Release

1. Go to your repository on GitHub
2. Click **"Releases"** (right sidebar)
3. Click **"Create a new release"**
4. Fill in:
   - **Tag**: `v1.0.0` (create new tag)
   - **Target**: `main`
   - **Title**: `Flow Launcher Shortcuts Plugin v1.0.0`
   - **Description**: Copy from CHANGELOG.md
   
5. **Upload artifacts**:
   - Drag `release_v1.0.0/ShortcutsEditor.exe`
   - Drag `release_v1.0.0/Flow.Launcher.Plugin.Shortcuts.zip`

6. Click **"Publish release"**

### 5. Repository Settings (Optional but Recommended)

#### Add Topics
Go to repository home → "About" (gear icon):
- `flow-launcher`
- `flow-launcher-plugin`
- `shortcuts`
- `bookmark-manager`
- `pyside6`
- `python`
- `productivity`
- `windows`

#### Add Description
```
A powerful Flow Launcher plugin for quick access to folders, files, apps, and URLs with browser bookmark import
```

#### Website
```
https://github.com/AMoorer/am_flowlauncher_plugins
```

### 6. Create README Badges (Optional)

Add these to the top of README.md:

```markdown
[![GitHub release](https://img.shields.io/github/v/release/AMoorer/am_flowlauncher_plugins)](https://github.com/AMoorer/am_flowlauncher_plugins/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub downloads](https://img.shields.io/github/downloads/AMoorer/am_flowlauncher_plugins/total)](https://github.com/AMoorer/am_flowlauncher_plugins/releases)
[![GitHub stars](https://img.shields.io/github/stars/AMoorer/am_flowlauncher_plugins)](https://github.com/AMoorer/am_flowlauncher_plugins/stargazers)
```

## Sharing Your Plugin

### Submit to Flow Launcher Plugin Directory

1. Fork https://github.com/Flow-Launcher/Flow.Launcher.PluginsManifest
2. Add your plugin to `plugins.json`:
   ```json
   {
     "ID": "Flow.Launcher.Plugin.Shortcuts",
     "Name": "Shortcuts",
     "Description": "Quick access to folders, files, apps, and URLs with bookmark import",
     "Author": "Andy Moorer",
     "Version": "1.0.0",
     "Language": "python",
     "Website": "https://github.com/AMoorer/am_flowlauncher_plugins",
     "IcoPath": "Images\\shortcut.png",
     "ExecuteFileName": "main.py"
   }
   ```
3. Submit pull request

### Share on Social Media

Example post:
```
🚀 Just released my Flow Launcher Shortcuts Plugin!

✨ Features:
- Quick access to folders, files, apps & URLs
- Import bookmarks from Chrome/Edge/Opera/Brave
- Beautiful PySide6 GUI editor
- Dark mode support

Download: https://github.com/AMoorer/am_flowlauncher_plugins

#FlowLauncher #Productivity #Python #OpenSource
```

## Maintenance

### For Future Releases

1. **Update version numbers**:
   - `plugin.json`
   - `editor.py` (About dialog)
   - README.md
   - CHANGELOG.md

2. **Update CHANGELOG.md** with new features

3. **Build release**:
   ```powershell
   create_release.bat
   ```

4. **Create new GitHub release** with updated files

5. **Update plugin manifest** if submitting to official directory

## Git Workflow Tips

### Daily Development

```powershell
# Check status
git status

# Add changes
git add .

# Commit
git commit -m "Add feature: XYZ"

# Push
git push
```

### Create Feature Branch

```powershell
# Create and switch to new branch
git checkout -b feature/bookmark-firefox

# Make changes...
# Commit changes...

# Push branch
git push -u origin feature/bookmark-firefox

# Create pull request on GitHub
```

### Sync with Main

```powershell
# Switch to main
git checkout main

# Pull latest
git pull

# Switch back to feature branch
git checkout feature/bookmark-firefox

# Merge main into feature
git merge main
```

## Troubleshooting

### Large Files Warning
If you get warnings about large files (>50MB):
```powershell
# Add to .gitignore
echo "*.exe" >> .gitignore
echo "dist/" >> .gitignore
echo "build/" >> .gitignore

# Only upload .exe files to GitHub Releases, not to repo
```

### Authentication Issues
Use GitHub Personal Access Token:
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Use token as password when git asks

### File Line Ending Issues
```powershell
# Configure git for Windows
git config --global core.autocrlf true
```

## Resources

- [GitHub Docs](https://docs.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Flow Launcher Plugin Dev Guide](https://www.flowlauncher.com/docs/#/develop-plugins)
- [Semantic Versioning](https://semver.org/)

---

**Questions?** Open an issue on GitHub or check the documentation.
