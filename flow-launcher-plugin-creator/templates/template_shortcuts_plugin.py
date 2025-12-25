"""
Data-Driven Shortcuts Plugin Template
Perfect for plugins that manage user-defined items (shortcuts, bookmarks, notes, etc.)
"""

import sys
import os
import json
import subprocess

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, '..', 'lib'))

from flowlauncher import FlowLauncher


class ShortcutsPlugin(FlowLauncher):
    def __init__(self):
        # Initialize data before calling super().__init__()
        self.shortcuts_file = os.path.join(parent_folder_path, 'shortcuts.json')
        self.shortcuts = self.load_shortcuts()
        
        super().__init__()
    
    def load_shortcuts(self):
        """Load shortcuts from JSON file."""
        try:
            if os.path.exists(self.shortcuts_file):
                with open(self.shortcuts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('shortcuts', [])
            return []
        except Exception as e:
            self.logger.error(f"Error loading shortcuts: {e}")
            return []
    
    def save_shortcuts(self):
        """Save shortcuts to JSON file."""
        try:
            with open(self.shortcuts_file, 'w', encoding='utf-8') as f:
                json.dump({'shortcuts': self.shortcuts}, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving shortcuts: {e}")
    
    def query(self, query):
        """Handle user query."""
        results = []
        
        # Special command: list all shortcuts
        if query.lower() == 'list':
            return self.show_shortcut_list()
        
        # Search shortcuts by keyword
        if query.strip():
            for shortcut in self.shortcuts:
                if query.lower() == shortcut.get('keyword', '').lower():
                    results.append(self.format_shortcut_result(shortcut))
        else:
            # Show help
            results.append({
                "Title": "Type a shortcut keyword",
                "SubTitle": "Or type 'list' to see all shortcuts",
                "IcoPath": "Images/icon.png"
            })
        
        return results
    
    def format_shortcut_result(self, shortcut):
        """Format a shortcut as a Flow Launcher result."""
        return {
            "Title": shortcut.get('name', 'Unnamed'),
            "SubTitle": shortcut.get('path', ''),
            "IcoPath": shortcut.get('icon', 'Images/icon.png'),
            "JsonRPCAction": {
                "method": "execute_shortcut",
                "parameters": [shortcut['keyword']]
            },
            "ContextData": shortcut['keyword']
        }
    
    def show_shortcut_list(self):
        """Show all shortcuts grouped by category."""
        results = []
        
        # Group by category
        categories = {}
        for shortcut in self.shortcuts:
            category = shortcut.get('category', 'Uncategorized')
            if category not in categories:
                categories[category] = []
            categories[category].append(shortcut)
        
        # Sort categories by priority
        for category, shortcuts in sorted(categories.items()):
            # Category header
            results.append({
                "Title": f"📁 {category}",
                "SubTitle": f"{len(shortcuts)} shortcuts",
                "IcoPath": "Images/folder.png"
            })
            
            # Shortcuts in category
            for shortcut in sorted(shortcuts, key=lambda x: x.get('priority', 0), reverse=True):
                results.append(self.format_shortcut_result(shortcut))
        
        return results
    
    def execute_shortcut(self, keyword):
        """Execute a shortcut by keyword."""
        shortcut = next((s for s in self.shortcuts if s['keyword'] == keyword), None)
        
        if not shortcut:
            return False
        
        try:
            path = shortcut.get('path', '')
            
            # Expand environment variables
            path = os.path.expandvars(path)
            
            # Execute based on type
            shortcut_type = shortcut.get('type', 'file')
            
            if shortcut_type == 'url':
                # Open URL in browser
                os.startfile(path)
            elif shortcut_type == 'folder':
                # Open folder in Explorer
                subprocess.Popen(f'explorer "{path}"')
            elif shortcut_type == 'file':
                # Open file with default or specific application
                open_with = shortcut.get('openWith')
                if open_with:
                    subprocess.Popen([open_with, path])
                else:
                    os.startfile(path)
            elif shortcut_type == 'app':
                # Launch application
                subprocess.Popen(path)
            
            return True
        except Exception as e:
            self.logger.error(f"Error executing shortcut: {e}")
            return False
    
    def context_menu(self, data):
        """Provide context menu for shortcuts."""
        return [
            {
                "Title": "Edit Shortcut",
                "SubTitle": "Open editor to modify this shortcut",
                "JsonRPCAction": {
                    "method": "open_editor",
                    "parameters": []
                }
            },
            {
                "Title": "Copy Path",
                "SubTitle": "Copy path/URL to clipboard",
                "JsonRPCAction": {
                    "method": "copy_path",
                    "parameters": [data]
                }
            },
            {
                "Title": "Delete Shortcut",
                "SubTitle": "Remove this shortcut",
                "JsonRPCAction": {
                    "method": "delete_shortcut",
                    "parameters": [data]
                }
            }
        ]
    
    def open_editor(self):
        """Open the GUI editor."""
        try:
            editor_path = os.path.join(parent_folder_path, '..', 'Editor', 'editor.py')
            if os.path.exists(editor_path):
                subprocess.Popen([sys.executable, editor_path])
            else:
                os.startfile(self.shortcuts_file)
        except Exception as e:
            self.logger.error(f"Error opening editor: {e}")
    
    def copy_path(self, keyword):
        """Copy shortcut path to clipboard."""
        shortcut = next((s for s in self.shortcuts if s['keyword'] == keyword), None)
        if shortcut:
            import pyperclip
            pyperclip.copy(shortcut.get('path', ''))
    
    def delete_shortcut(self, keyword):
        """Delete a shortcut."""
        self.shortcuts = [s for s in self.shortcuts if s['keyword'] != keyword]
        self.save_shortcuts()


if __name__ == "__main__":
    ShortcutsPlugin()
