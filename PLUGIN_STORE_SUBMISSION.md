# Flow Launcher Plugin Store Submission Guide

This guide will walk you through submitting your Shortcuts plugin to the official Flow Launcher Plugin Store.

## ✅ Prerequisites Checklist

Before submitting, ensure you have:

- [x] **Proper GUID in plugin.json** - Updated to `8F2A4B1C-9E7D-4A3B-B5C8-1F9E2A7D4C6B`
- [x] **GitHub Release v1.0.0** - Already published with plugin ZIP
- [x] **GitHub Actions Workflow** - Created at `.github/workflows/publish-release.yml`
- [x] **Manifest file** - Created `Shortcuts-8F2A4B1C-9E7D-4A3B-B5C8-1F9E2A7D4C6B.json`
- [x] **Plugin conforms to policy** - No malicious code, piracy, etc.

## 📋 Submission Steps

### 1. Fork the Plugin Manifest Repository

1. Go to https://github.com/Flow-Launcher/Flow.Launcher.PluginsManifest
2. Click **"Fork"** in the top-right corner
3. Create fork in your account

### 2. Add Your Plugin Manifest

1. In your fork, navigate to the `plugins/` directory
2. Click **"Add file"** → **"Upload files"**
3. Upload `Shortcuts-8F2A4B1C-9E7D-4A3B-B5C8-1F9E2A7D4C6B.json`
4. Or create the file directly on GitHub:
   - Click **"Add file"** → **"Create new file"**
   - Name: `plugins/Shortcuts-8F2A4B1C-9E7D-4A3B-B5C8-1F9E2A7D4C6B.json`
   - Paste the content from your local file

### 3. Create Pull Request

1. After committing the file, go to your fork's main page
2. Click **"Contribute"** → **"Open pull request"**
3. Fill in the PR details:

**Title:**
```
Add Shortcuts Plugin
```

**Description:**
```
## Plugin Information
- **Name**: Shortcuts
- **Author**: Andy Moorer
- **Version**: 1.0.0
- **Language**: Python

## Description
Quick access to folders, files, apps, and URLs via custom keywords. Includes browser bookmark import from Chrome, Edge, Opera, and Brave.

## Features
- Quick access via custom keywords
- Browser bookmark import (Chrome, Edge, Opera, Brave)
- Category organization
- Priority-based ordering
- Custom icons support
- Beautiful PySide6 GUI editor with dark mode

## Links
- **Repository**: https://github.com/AMoorer/am_flowlauncher_plugins
- **Release**: https://github.com/AMoorer/am_flowlauncher_plugins/releases/tag/v1.0.0
- **Plugin ZIP**: https://github.com/AMoorer/am_flowlauncher_plugins/releases/download/v1.0.0/Flow.Launcher.Plugin.Shortcuts.zip

## Checklist
- [x] Plugin has a valid GUID
- [x] GitHub Actions workflow set up for automated releases
- [x] Plugin conforms to Plugin Store policy
- [x] Plugin has been tested and works correctly
- [x] Icon is hosted on CDN (jsdelivr)
```

4. Click **"Create pull request"**

### 4. Wait for Approval

- The Flow Launcher team will review your submission
- They may request changes or ask questions
- Once approved, your plugin will appear in the store
- Note: It may take several days to a week for the plugin to show up due to CDN syncing

## 📦 Manifest File Details

Your manifest file (`Shortcuts-8F2A4B1C-9E7D-4A3B-B5C8-1F9E2A7D4C6B.json`) contains:

```json
{
  "ID": "8F2A4B1C-9E7D-4A3B-B5C8-1F9E2A7D4C6B",
  "Name": "Shortcuts",
  "Description": "Quick access to folders, files, apps, and URLs via custom keywords",
  "Author": "Andy Moorer",
  "Version": "1.0.0",
  "Language": "python",
  "Website": "https://github.com/AMoorer/am_flowlauncher_plugins",
  "UrlDownload": "https://github.com/AMoorer/am_flowlauncher_plugins/releases/download/v1.0.0/Flow.Launcher.Plugin.Shortcuts.zip",
  "UrlSourceCode": "https://github.com/AMoorer/am_flowlauncher_plugins",
  "IcoPath": "https://cdn.jsdelivr.net/gh/AMoorer/am_flowlauncher_plugins@main/Flow.Launcher.Plugin.Shortcuts/Images/shortcut.png"
}
```

**Key Points:**
- `ID` must match the GUID in `plugin.json`
- `UrlDownload` points to the plugin ZIP from your GitHub release
- `IcoPath` uses jsdelivr CDN for global accessibility
- Version matches your current release (1.0.0)

## 🔄 Future Updates

**Good news!** After your initial submission is approved, you don't need to manually update the manifest.

Every **3 hours**, the Flow Launcher CI automatically checks for new releases and updates plugins to the latest version.

**To release an update:**
1. Update version in `plugin.json` (e.g., `1.1.0`)
2. Update `CHANGELOG.md`
3. Create a new GitHub release with tag `v1.1.0`
4. GitHub Actions will automatically build and attach the ZIP
5. Flow Launcher CI will detect it and update the manifest automatically

## 🧪 Testing Before Store Availability

While waiting for approval, users can manually install your plugin:

```
pm install https://github.com/AMoorer/am_flowlauncher_plugins/releases/download/v1.0.0/Flow.Launcher.Plugin.Shortcuts.zip
```

Or from a local path:
```
pm install C:\path\to\Flow.Launcher.Plugin.Shortcuts.zip
```

## 📖 Plugin Store Policy

Your plugin must comply with these rules (you're good!):

✅ No malicious code  
✅ No piracy  
✅ No deceptive use  
✅ No inappropriate content  
✅ No illegal activities  
✅ No impersonation  
✅ No abuse  
✅ No fraud  
✅ No spam  

## 🎯 After Approval

Once approved, users can install via:

**Plugin Store UI:**
- Open Flow Launcher
- Type `pm` to open Plugin Manager
- Search for "Shortcuts"
- Click Install

**Command Line:**
```
pm install Shortcuts
```

## 🐛 Support & Issues

Users should report issues directly to your repository, not the plugin manifest repo.

They can access this via:
1. Type `pm install` in Flow Launcher
2. Find your plugin
3. `Shift+Enter` or right-click
4. Select "Suggest an enhancement or submit an issue"

## 📞 Need Help?

- **Flow Launcher Docs**: https://www.flowlauncher.com/docs/
- **Plugin Development**: Check the HelloWorldPython example
- **Your repository issues**: https://github.com/AMoorer/am_flowlauncher_plugins/issues

---

**Ready to submit?** Follow the steps above and get your plugin on the store! 🚀
