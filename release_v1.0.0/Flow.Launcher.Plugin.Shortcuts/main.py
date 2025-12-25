# -*- coding: utf-8 -*-

import sys
import os
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, 'plugin'))

from flowlauncher import FlowLauncher
import json
import webbrowser
import subprocess
from pathlib import Path


class Shortcuts(FlowLauncher):
    
    def __init__(self):
        self.shortcuts_file = os.path.join(parent_folder_path, 'shortcuts.json')
        self.shortcuts = self.load_shortcuts()
        super().__init__()
    
    def load_shortcuts(self):
        """Load shortcuts from JSON file"""
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
        """Save shortcuts to JSON file"""
        try:
            with open(self.shortcuts_file, 'w', encoding='utf-8') as f:
                json.dump({'shortcuts': self.shortcuts}, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            self.logger.error(f"Error saving shortcuts: {e}")
            return False
    
    def query(self, query):
        """Main query handler"""
        results = []
        query_lower = query.lower().strip()
        
        # Check for "shortcutlist" command
        if query_lower.startswith('shortcutlist') or query_lower == '':
            return self.show_shortcut_list(query_lower.replace('shortcutlist', '').strip())
        
        # Search shortcuts by keyword
        for shortcut in self.shortcuts:
            keyword = shortcut.get('keyword', '').lower()
            if query_lower in keyword or keyword.startswith(query_lower):
                results.append(self.create_result(shortcut))
        
        # Sort by priority (higher first) and keyword match quality
        results.sort(key=lambda x: (
            -x.get('Score', 0),  # Higher priority first
            len(x.get('Title', ''))  # Shorter matches first
        ))
        
        if not results and query:
            results.append({
                "Title": f"No shortcuts found for '{query}'",
                "SubTitle": "Use 's shortcutlist' to view all shortcuts or open the editor to add new ones",
                "IcoPath": "Images/shortcut.png",
                "JsonRPCAction": {
                    "method": "do_nothing",
                    "parameters": []
                }
            })
        
        return results
    
    def show_shortcut_list(self, filter_category=''):
        """Display all shortcuts grouped by category"""
        results = []
        
        # Group shortcuts by category
        categories = {}
        for shortcut in self.shortcuts:
            category = shortcut.get('category', 'Uncategorized')
            if category not in categories:
                categories[category] = []
            categories[category].append(shortcut)
        
        # Sort categories: Folders, Files, Apps, then alphabetically
        priority_categories = ['Folders', 'Files', 'Apps']
        sorted_categories = []
        for cat in priority_categories:
            if cat in categories:
                sorted_categories.append(cat)
        sorted_categories.extend(sorted([c for c in categories.keys() if c not in priority_categories]))
        
        # Filter by category if specified
        if filter_category:
            sorted_categories = [c for c in sorted_categories if filter_category.lower() in c.lower()]
        
        # Add category headers and shortcuts with invisible ordering prefix
        result_counter = 1
        for category in sorted_categories:
            # Use zero-width space + number for invisible sorting (U+200B repeated)
            invisible_prefix = '\u200B' * result_counter
            
            # Category header
            results.append({
                "Title": f"{invisible_prefix}═══ {category} ═══",
                "SubTitle": f"{len(categories[category])} shortcut(s) - Press Enter to open editor",
                "IcoPath": self.get_category_icon(category),
                "Score": 10000,
                "JsonRPCAction": {
                    "method": "open_editor",
                    "parameters": []
                }
            })
            result_counter += 1
            
            # Shortcuts in this category
            for shortcut in sorted(categories[category], key=lambda x: x.get('keyword', '')):
                invisible_prefix = '\u200B' * result_counter
                result = self.create_result(shortcut, show_category=False)
                result["Title"] = f"{invisible_prefix}{result['Title']}"
                result["Score"] = 10000
                results.append(result)
                result_counter += 1
        
        if not results:
            results.append({
                "Title": "No shortcuts configured",
                "SubTitle": "Open the Shortcuts Editor to add your first shortcut",
                "IcoPath": "Images/shortcut.png",
                "JsonRPCAction": {
                    "method": "open_editor",
                    "parameters": []
                }
            })
        
        # Sort results by score (descending) to ensure proper ordering
        results.sort(key=lambda x: x.get('Score', 0), reverse=True)
        
        return results
    
    def create_result(self, shortcut, show_category=True):
        """Create a Flow Launcher result from a shortcut"""
        keyword = shortcut.get('keyword', '')
        path = shortcut.get('path', '')
        shortcut_type = shortcut.get('type', 'app')
        category = shortcut.get('category', 'Uncategorized')
        icon = shortcut.get('icon', 'Images/shortcut.png')
        priority = shortcut.get('priority', 50)
        open_with = shortcut.get('openWith', '')
        
        # Resolve icon path
        if icon and not os.path.isabs(icon):
            icon = os.path.join(parent_folder_path, icon)
        if not os.path.exists(icon):
            icon = os.path.join(parent_folder_path, "Images/shortcut.png")
        
        # Create subtitle based on type
        if shortcut_type == 'url':
            subtitle = f"🌐 {path}"
        elif shortcut_type == 'folder':
            subtitle = f"📁 {path}"
        elif shortcut_type == 'file':
            if open_with:
                subtitle = f"📄 {path} (with {os.path.basename(open_with)})"
            else:
                subtitle = f"📄 {path}"
        else:  # app
            subtitle = f"🚀 {path}"
        
        if show_category:
            subtitle = f"[{category}] {subtitle}"
        
        return {
            "Title": keyword,
            "SubTitle": subtitle,
            "IcoPath": icon,
            "Score": priority,
            "JsonRPCAction": {
                "method": "execute_shortcut",
                "parameters": [json.dumps(shortcut)]
            },
            "ContextData": json.dumps(shortcut)
        }
    
    def get_category_icon(self, category):
        """Get icon for category header"""
        category_lower = category.lower()
        if 'folder' in category_lower:
            return "Images/folder.png"
        elif 'file' in category_lower:
            return "Images/file.png"
        elif 'app' in category_lower:
            return "Images/app.png"
        else:
            return "Images/bookmark.png"
    
    def context_menu(self, data):
        """Right-click context menu"""
        try:
            shortcut = json.loads(data) if isinstance(data, str) else data
            
            return [
                {
                    "Title": "Open Shortcuts Editor",
                    "SubTitle": "Edit this shortcut or add new ones",
                    "IcoPath": "Images/shortcut.png",
                    "JsonRPCAction": {
                        "method": "open_editor",
                        "parameters": [data]
                    }
                },
                {
                    "Title": "Copy Path",
                    "SubTitle": shortcut.get('path', ''),
                    "IcoPath": "Images/copy.png",
                    "JsonRPCAction": {
                        "method": "copy_to_clipboard",
                        "parameters": [shortcut.get('path', '')]
                    }
                },
                {
                    "Title": "Delete Shortcut",
                    "SubTitle": f"Remove '{shortcut.get('keyword', '')}' from shortcuts",
                    "IcoPath": "Images/delete.png",
                    "JsonRPCAction": {
                        "method": "delete_shortcut",
                        "parameters": [shortcut.get('keyword', '')]
                    }
                }
            ]
        except Exception as e:
            self.logger.error(f"Context menu error: {e}")
            return []
    
    def execute_shortcut(self, shortcut_json):
        """Execute a shortcut based on its type"""
        try:
            shortcut = json.loads(shortcut_json) if isinstance(shortcut_json, str) else shortcut_json
            path = shortcut.get('path', '')
            shortcut_type = shortcut.get('type', 'app')
            open_with = shortcut.get('openWith', '')
            
            # Expand environment variables
            path = os.path.expandvars(path)
            if open_with:
                open_with = os.path.expandvars(open_with)
            
            if shortcut_type == 'url':
                webbrowser.open(path)
            elif shortcut_type == 'folder':
                os.startfile(path)
            elif shortcut_type == 'file':
                if open_with and os.path.exists(open_with):
                    subprocess.Popen([open_with, path])
                else:
                    os.startfile(path)
            elif shortcut_type == 'app':
                subprocess.Popen(path, shell=True)
            
        except Exception as e:
            self.logger.error(f"Error executing shortcut: {e}")
    
    def open_editor(self, shortcut_json=None):
        """Open the shortcuts editor GUI"""
        try:
            # Try multiple possible locations for the editor
            possible_paths = [
                # Development location
                os.path.join(os.path.dirname(parent_folder_path), 'ShortcutsEditor', 'editor.py'),
                # Installed alongside plugin in Plugins folder
                os.path.join(os.path.dirname(parent_folder_path), 'Flow.Launcher.Plugin.Shortcuts.Editor', 'editor.py'),
                # In plugin directory
                os.path.join(parent_folder_path, 'editor.py'),
            ]
            
            editor_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    editor_path = path
                    break
            
            if editor_path:
                subprocess.Popen([sys.executable, editor_path])
            else:
                # Fallback: open shortcuts.json in default editor
                os.startfile(self.shortcuts_file)
        except Exception as e:
            self.logger.error(f"Error opening editor: {e}")
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard"""
        try:
            import win32clipboard
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text)
            win32clipboard.CloseClipboard()
        except:
            # Fallback using PowerShell
            subprocess.run(['powershell', '-command', f'Set-Clipboard -Value "{text}"'], 
                         capture_output=True, shell=True)
    
    def delete_shortcut(self, keyword):
        """Delete a shortcut by keyword"""
        try:
            self.shortcuts = [s for s in self.shortcuts if s.get('keyword') != keyword]
            self.save_shortcuts()
        except Exception as e:
            self.logger.error(f"Error deleting shortcut: {e}")
    
    def do_nothing(self):
        """Placeholder action"""
        pass


if __name__ == "__main__":
    Shortcuts()
