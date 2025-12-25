# Documentation Images

This folder contains images used in the project's documentation and README.

## Image Guidelines

### Recommended Images for README

1. **Hero/Banner Image** (`hero.png` or `banner.png`)
   - Showcase the plugin in action
   - Recommended size: 1200x630px (GitHub social preview size)

2. **Editor Screenshot** (`editor-screenshot.png`)
   - Full window screenshot of ShortcutsEditor
   - Show the table with some example shortcuts
   - Include menu bar and buttons
   - Recommended size: 1920x1080px or actual window size

3. **Flow Launcher Integration** (`flow-launcher-demo.png`)
   - Screenshot showing shortcuts in Flow Launcher
   - Show the categorized list view (`s shortcutlist`)
   - Recommended size: 800-1200px wide

4. **Bookmark Import** (`bookmark-import.png`)
   - Screenshot of the bookmark import dialog
   - Show browser selection and bookmark list
   - Recommended size: 600-800px wide

5. **Demo GIF** (`demo.gif`)
   - Animated demonstration of using a shortcut
   - Type keyword → Press Enter → Action happens
   - Keep file size under 5MB for fast loading

### File Naming Conventions

- Use lowercase with hyphens: `editor-screenshot.png`
- Be descriptive: `bookmark-import-dialog.png`
- Version if needed: `editor-screenshot-v1.png`

### Supported Formats

- **PNG** - Screenshots, UI elements (best quality)
- **JPG** - Photos, complex images (smaller file size)
- **GIF** - Short animations (under 5MB)
- **WebP** - Modern format (if GitHub support is confirmed)

### Image Optimization

Before committing images:
1. **Compress** using tools like TinyPNG, ImageOptim, or Squoosh
2. **Resize** to appropriate dimensions (no need for 4K screenshots)
3. **Crop** to focus on relevant content
4. Keep file sizes reasonable (< 500KB for screenshots, < 2MB for GIFs)

## Usage in README

### Markdown Syntax

```markdown
![Alt Text](docs/images/image-name.png)
```

### With Links

```markdown
[![Alt Text](docs/images/image-name.png)](https://link-to-larger-version.png)
```

### Centered Images

```markdown
<p align="center">
  <img src="docs/images/image-name.png" alt="Alt Text" width="800">
</p>
```

### Side-by-Side Images

```markdown
| Editor | Flow Launcher |
|--------|---------------|
| ![Editor](docs/images/editor.png) | ![Flow](docs/images/flow.png) |
```

## Example README Section

```markdown
## 📸 Screenshots

### Shortcuts Editor
![Shortcuts Editor](docs/images/editor-screenshot.png)
*Modern PySide6 interface with dark mode support*

### Flow Launcher Integration
![Flow Launcher](docs/images/flow-launcher-demo.png)
*Quick access to your shortcuts with categorized display*

### Bookmark Import
![Bookmark Import](docs/images/bookmark-import.png)
*Import bookmarks from Chrome, Edge, Opera, and Brave*

## 🎬 Demo

![Demo](docs/images/demo.gif)
*See it in action!*
```

## Tips

- Take screenshots with a clean background
- Use dark mode for consistency (or provide both themes)
- Annotate important features with arrows or highlights
- Include realistic example data (not "test1", "test2")
- Consider a demo video hosted on YouTube/Vimeo for longer demonstrations

---

**Ready to add images?** Just drop your screenshots in this folder and reference them in the README!
