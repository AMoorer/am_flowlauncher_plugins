---
title: "Building a Flow Launcher Plugin with AI: From Idea to Plugin Store in One Session"
date: 2024-12-24
categories: [AI, Development, Productivity]
tags: [Claude, Flow Launcher, Python, PySide6, Productivity Tools]
---

# Building a Flow Launcher Plugin with AI: From Idea to Plugin Store in One Session

What if you could build a complete productivity tool—with a GUI editor, automated builds, and plugin store submission—in a single coding session? Not as a proof-of-concept or MVP, but production-ready code that people can actually use?

That's exactly what happened last night with Claude Code (Windsurf), and the result is now live: the **Flow Launcher Shortcuts Plugin** with browser bookmark import, a beautiful PySide6 editor, and a comprehensive Claude skill that democratizes plugin creation for everyone.

## The Journey

### Starting Point: A Need for Better Shortcuts

I've been using Flow Launcher for a while (if you don't know it, it's a fantastic keyboard-driven launcher for Windows—think Spotlight or Alfred but better). I wanted quick access to my frequently used folders, files, apps, and especially my browser bookmarks. The existing solutions weren't quite right, so I thought: "Let's build a plugin."

But here's the thing—I didn't want to just build it myself. I wanted to build it *with* AI, documenting the patterns and creating something that others could use to make their own plugins. And that's where Claude Code came in.

### The AI Partner: Claude Code (Windsurf)

For this project, I used [Windsurf](https://codeium.com/windsurf), a VSCode variant powered by Claude Sonnet 4.5. It's become my go-to for these kinds of "let's build something real" sessions. The agentic capabilities—where Claude can read files, search code, make edits, and run commands—made this possible.

And I have to say, the experience was... remarkable. Not just in terms of speed, but in the quality and completeness of what we built together.

## What We Built

### 1. The Flow Launcher Shortcuts Plugin

**Features:**
- Quick access via custom keywords (`s docs`, `s github`, etc.)
- Multiple shortcut types: folders, files, applications, URLs
- Category organization with priority-based ordering
- Custom icons for each shortcut
- Context menu for editing and management
- Special `s shortcutlist` command to view all shortcuts grouped by category
- Environment variable support (`%USERPROFILE%`, etc.)

The plugin integrates seamlessly with Flow Launcher's JSON-RPC architecture, and we solved some tricky problems along the way (more on that below).

### 2. The PySide6 GUI Editor

Because editing JSON files by hand isn't fun, we built a full-featured desktop application:

**Editor Features:**
- Modern Qt interface with dark mode support
- Table view of all shortcuts
- Add/Edit/Delete dialogs with form validation
- **Browser bookmark import** from Chrome, Edge, Opera, and Brave
- Icon picker with file browser
- Custom save location (choose where your shortcuts are stored)
- Settings persistence (window size, custom paths)
- Menu bar with File and Help menus
- Comprehensive About dialog with usage instructions
- Auto-save functionality

The bookmark import feature is particularly cool—it recursively parses Chromium bookmark files, lets you select which bookmarks to import, and automatically generates keywords from bookmark names. It even handles non-standard browser locations with a "Browse..." button.

### 3. The Claude Skill: Democratizing Plugin Creation

This is where it gets really interesting. After building the plugin, we extracted all the knowledge into a comprehensive **Claude skill** that any AI assistant (or developer) can use to create Flow Launcher plugins.

**The skill includes:**
- **Complete architecture knowledge**: JSON-RPC, result formatting, context menus, scoring
- **4 development patterns**: Data-driven, dynamic search, action plugins, calculator/converter
- **3 production-ready templates**:
  - Basic query-response plugin
  - Full shortcuts plugin with JSON storage
  - PySide6 GUI editor
- **2 automation scripts**:
  - Project scaffold generator
  - Plugin store manifest creator
- **Comprehensive best practices** (400+ lines of battle-tested wisdom)
- **9-phase execution process** from requirements to plugin store

The skill is now [published on GitHub](https://github.com/AMoorer/andys-claude-skills/tree/main/flow-launcher-plugin-creator) and ready for anyone to use with Claude Desktop.

## The Technical Challenges (and Solutions)

Building this wasn't just "AI writes code and it works." We hit real problems that required real solutions:

### Challenge 1: Result Ordering

**The Problem:** Flow Launcher wasn't respecting our priority scores. Categories and shortcuts appeared in random order.

**The Solution:** We discovered that Flow Launcher's internal sorting overrides the Score field. The fix? Use invisible Unicode characters (Zero-Width Spaces) as sorting prefixes:

```python
def generate_sort_prefix(priority: int) -> str:
    """Generate invisible Unicode prefix for reliable sorting"""
    zwsp = '\u200b'  # Zero-Width Space
    count = 200 - priority  # Higher priority = fewer chars = sorts first
    return zwsp * count

# Usage in results:
{
    "Title": f"{generate_sort_prefix(100)}Category Name",
    "SubTitle": "Description",
    # ...
}
```

This is the kind of solution that takes hours to figure out through trial and error. Claude and I worked through it systematically, testing different approaches until we found one that worked.

### Challenge 2: Atomic File Writes

**The Problem:** When saving shortcuts, if the process crashed mid-write, the JSON file could be corrupted.

**The Solution:** Implement atomic writes using temp files:

```python
import tempfile, os, json

def save_data_safely(data, filepath):
    # Write to temp file first
    with tempfile.NamedTemporaryFile('w', delete=False, encoding='utf-8') as f:
        json.dump(data, f, indent=2)
        temp_path = f.name
    
    # Replace original atomically (Windows-safe)
    os.replace(temp_path, filepath)
```

### Challenge 3: GUI Dark Mode

**The Problem:** Hardcoded background colors in the editor made text unreadable in dark mode.

**The Solution:** Don't hardcode colors—let Qt use the system palette:

```python
# DON'T do this:
label.setStyleSheet("background: #f0f0f0;")  # ❌

# DO this:
label.setStyleSheet("padding: 10px;")  # ✅ Let system theme handle colors
```

### Challenge 4: Plugin Store Submission

**The Problem:** Submitting to the Flow Launcher Plugin Store requires forking a repo, adding a manifest file, and creating a pull request.

**The Solution:** Automate it! Claude used GitHub CLI to:
1. Fork the plugin manifest repository
2. Copy the manifest file to the plugins directory
3. Commit and push
4. Create a pull request with a comprehensive description

All done programmatically. No manual clicking required.

## The AI Development Experience

Working with Claude Code on this project felt different from traditional coding. Here's what stood out:

### Pair Programming, Amplified

It wasn't "tell AI what to do and watch it work." It was genuinely collaborative:
- I'd describe what I wanted
- Claude would propose solutions
- We'd discuss trade-offs
- I'd test and provide feedback
- Claude would refine and iterate

The back-and-forth felt natural, like working with a very knowledgeable (and very fast) junior developer who never gets tired.

### Context Awareness

Claude read through the Flow Launcher documentation, examined existing plugins, understood the architecture, and applied patterns correctly. When I mentioned "I want bookmark import," it knew to:
- Parse Chromium bookmark JSON format
- Recursively traverse bookmark folders
- Generate keywords from names
- Handle duplicate keywords gracefully
- Provide UI for browser selection
- Support manual file browsing for edge cases

That's not just code generation—that's understanding the problem domain.

### Error Handling and Edge Cases

One of the most impressive aspects was how Claude thought about error handling and edge cases without being prompted:
- What if the shortcuts file doesn't exist? (Create empty list)
- What if the JSON is malformed? (Graceful fallback)
- What if the user's Python environment doesn't have PyInstaller? (Install it automatically)
- What if the GitHub remote has conflicting changes? (Handle merge conflicts)

This kind of defensive programming is what separates hobby code from production code.

### Building the Skill: Meta-Development

The final phase—extracting our knowledge into a Claude skill—was fascinating. We were essentially documenting our development process in a format that other AI assistants could use. It's like writing a "how-to guide" that's structured specifically for AI consumption.

The skill includes not just code templates, but the *reasoning* behind design decisions, common pitfalls, and solutions to problems we encountered. It's knowledge transfer at a new level.

## The Results

Let me quantify what we accomplished in one coding session (about 6 hours total, including breaks):

**Plugin:**
- ~310 lines of Python
- Full JSON-RPC integration
- Category organization
- Priority system
- Context menus
- Test suite

**Editor:**
- ~900 lines of Python
- Complete PySide6 GUI
- Bookmark import from 4 browsers
- Dark mode support
- Settings persistence
- Menu system with About dialog

**Documentation:**
- Comprehensive README
- CHANGELOG
- QUICKSTART guide
- Plugin store submission guide
- Release checklist

**Build Automation:**
- GitHub Actions workflow
- PyInstaller build script
- Release packaging script
- Plugin store manifest

**Claude Skill:**
- 2,300+ lines of knowledge
- 3 complete templates
- 2 automation scripts
- 400+ lines of best practices
- Published and ready to use

**And we:**
- Published to GitHub
- Created v1.0.0 release
- Submitted to Flow Launcher Plugin Store
- Published the skill to my skills repository

All production-ready. All tested. All documented.

## The Democratization Angle

This is what excites me most: the skill we created means *anyone* can now ask Claude to build them a Flow Launcher plugin, and they'll get production-quality code with best practices baked in.

Want a plugin to manage project shortcuts? Ask Claude.  
Want a calculator plugin? Ask Claude.  
Want a quick-search plugin for your knowledge base? Ask Claude.

The barrier to entry just dropped significantly. You don't need to know Flow Launcher's architecture, or Python's asyncio, or how to set up GitHub Actions, or how to submit to a plugin store. Claude knows all of that now, thanks to the skill.

## What This Means for Development

I think we're seeing a shift in how we should think about AI-assisted development:

### Before: AI as Code Generator
"Write me a function that does X"  
→ Get code, paste it, debug it, fix it

### Now: AI as Development Partner
"I want to build a productivity tool that does X"  
→ Get architecture, implementation, tests, docs, automation, deployment

The difference is **completeness** and **production-readiness**.

### The Future: AI as Knowledge Multiplier
"Here's what I learned building this tool. Capture it so others can benefit."  
→ Get reusable skills, patterns, and templates that make future development faster

This is the meta-layer: AI helping us create resources that help AI help others. It's recursive improvement.

## Try It Yourself

If you want to experience what we built:

### Use the Plugin
1. Download from the [GitHub release](https://github.com/AMoorer/am_flowlauncher_plugins/releases)
2. Install in Flow Launcher
3. Run the standalone editor to add shortcuts
4. Import your browser bookmarks
5. Use `s <keyword>` for quick access

### Use the Skill
1. Add the [Flow Launcher Plugin Creator skill](https://github.com/AMoorer/andys-claude-skills/tree/main/flow-launcher-plugin-creator) to Claude Desktop
2. Ask Claude to create a plugin for you
3. Watch as it generates complete, production-ready code

### Learn from the Code
Everything is open source and well-documented. Check out:
- The [plugin repository](https://github.com/AMoorer/am_flowlauncher_plugins)
- The [skill repository](https://github.com/AMoorer/andys-claude-skills)
- The best practices documentation
- The templates and automation scripts

## Final Thoughts

This project reinforced something I've been thinking about: **the bottleneck in software development is shifting from "writing code" to "knowing what to build and how it should work."**

With AI, if you can clearly articulate the problem and guide the solution, you can build production-quality tools in a fraction of the time. But you still need:
- Domain knowledge (what makes a good plugin?)
- Design sense (how should this work?)
- Quality standards (what's production-ready?)
- Testing discipline (does this actually work?)

AI amplifies your capabilities, but those capabilities still matter. The difference is that now, with the right AI partner, your capabilities can scale further than ever before.

And the best part? The knowledge we captured in the skill means the next person who wants to build a Flow Launcher plugin won't need to figure all this out. They can stand on our shoulders—or rather, on Claude's shoulders, equipped with our knowledge.

That's democratization in action.

---

**Ready to build your own Flow Launcher plugin?** Grab the skill, fire up Claude, and let's make productivity tools accessible to everyone.

*Comments? Questions? Find me on [GitHub](https://github.com/AMoorer) or [LinkedIn](https://www.linkedin.com/in/andymoorer/).*

---

**Technical Details:**
- **Flow Launcher Plugin**: Python 3.8+, flowlauncher package
- **GUI Editor**: PySide6 (Qt for Python)
- **AI Partner**: Claude Sonnet 4.5 via Windsurf (Claude Code)
- **Time**: ~6 hours, one session
- **Lines of Code**: ~1,200 (plugin + editor)
- **Lines of Documentation**: ~3,000+ (including skill)
- **Status**: Live on GitHub, submitted to Flow Launcher Plugin Store
- **License**: MIT (open source)

**Links:**
- Plugin: https://github.com/AMoorer/am_flowlauncher_plugins
- Skill: https://github.com/AMoorer/andys-claude-skills/tree/main/flow-launcher-plugin-creator
- Flow Launcher: https://www.flowlauncher.com/
