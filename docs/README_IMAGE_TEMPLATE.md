# README Image Placement Guide

This is a suggested layout for adding images to your README.md. Copy the sections you want to use.

---

## Option 1: Add Screenshots Section After Features

Place after the "Features" section (around line 50):

```markdown
## 📸 Screenshots

<p align="center">
  <img src="docs/images/editor-screenshot.png" alt="Shortcuts Editor" width="900">
</p>
<p align="center"><i>Modern PySide6 editor with dark mode support</i></p>

<br>

<p align="center">
  <img src="docs/images/flow-launcher-demo.png" alt="Flow Launcher Integration" width="700">
</p>
<p align="center"><i>Quick access to shortcuts in Flow Launcher</i></p>

<br>

<p align="center">
  <img src="docs/images/bookmark-import.png" alt="Bookmark Import" width="600">
</p>
<p align="center"><i>Import bookmarks from major browsers</i></p>
```

---

## Option 2: Add Hero Banner at Top

Place right after the title and badges (around line 8):

```markdown
# Flow Launcher Shortcuts Plugin

[![GitHub release](https://img.shields.io/github/v/release/AMoorer/am_flowlauncher_plugins)](https://github.com/AMoorer/am_flowlauncher_plugins/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

<p align="center">
  <img src="docs/images/hero.png" alt="Flow Launcher Shortcuts Plugin" width="100%">
</p>

A powerful Flow Launcher plugin for quick access to folders, files, applications, and URLs with browser bookmark import support!
```

---

## Option 3: Add Demo GIF in Usage Section

Place in the "Usage" section to show it in action:

```markdown
## 🚀 Usage

### Quick Demo

<p align="center">
  <img src="docs/images/demo.gif" alt="Plugin Demo" width="700">
</p>

### Basic Usage

1. **Add shortcuts** using the GUI editor
2. **In Flow Launcher**, type `s <keyword>` to trigger your shortcut
3. **Press Enter** to execute
```

---

## Option 4: Side-by-Side Comparison

Show editor and Flow Launcher side by side:

```markdown
## 📸 See It in Action

| Shortcuts Editor | Flow Launcher Integration |
|:----------------:|:-------------------------:|
| ![Editor](docs/images/editor-screenshot.png) | ![Flow Launcher](docs/images/flow-launcher-demo.png) |
| *Manage shortcuts with an intuitive GUI* | *Quick access with keyboard shortcuts* |
```

---

## Option 5: Feature Showcase with Images

Replace text-heavy feature sections with visual examples:

```markdown
## ✨ Key Features

### 🎨 Beautiful GUI Editor
<img src="docs/images/editor-screenshot.png" alt="Editor" width="700">

Modern PySide6 interface with:
- Dark mode support
- Table view of all shortcuts
- Icon preview
- Drag-and-drop support

### 🔖 Browser Bookmark Import
<img src="docs/images/bookmark-import.png" alt="Import" width="600">

Import bookmarks from:
- Google Chrome
- Microsoft Edge
- Opera
- Brave

### ⚡ Quick Access
<img src="docs/images/flow-launcher-demo.png" alt="Flow Launcher" width="700">

Type `s shortcutlist` to see all your shortcuts organized by category.
```

---

## Recommended Image Sizes

- **Hero/Banner**: 1200x630px (GitHub social preview)
- **Full Screenshots**: 1920x1080px or actual window size
- **Feature Screenshots**: 600-900px wide
- **Demo GIFs**: 700-800px wide, under 5MB

---

## Pro Tips

1. **Use consistent styling**: Same background, theme, example data
2. **Annotate if helpful**: Add arrows or highlights to show features
3. **Compress images**: Use TinyPNG or Squoosh before committing
4. **Provide alt text**: Helps with accessibility and SEO
5. **Link to full size**: Let users click for larger versions if needed

---

## Example Image Filenames

Here's what you might create:

```
docs/images/
├── hero.png                      # Main banner/hero image
├── editor-screenshot.png         # Full editor window
├── editor-dark-mode.png          # Editor in dark mode
├── flow-launcher-demo.png        # Plugin in Flow Launcher
├── shortcutlist-view.png         # Category list view
├── bookmark-import.png           # Import dialog
├── bookmark-import-browsers.png  # Browser selection
├── demo.gif                      # Animated demo
├── context-menu.png              # Right-click menu
└── about-dialog.png              # About dialog
```

---

**Ready to add images?** 
1. Take your screenshots
2. Save them to `docs/images/`
3. Add markdown to README.md using the templates above
4. Commit and push!
