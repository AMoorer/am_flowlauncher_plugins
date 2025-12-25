#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton,
                               QDialog, QFormLayout, QLineEdit, QComboBox, QSpinBox,
                               QFileDialog, QLabel, QMessageBox, QHeaderView, QGroupBox,
                               QListWidget, QCheckBox, QProgressDialog, QMenuBar, QTextEdit)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIcon, QPixmap, QAction


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = Path(__file__).parent
    return Path(base_path) / relative_path


class ShortcutDialog(QDialog):
    """Dialog for adding/editing a shortcut"""
    
    def __init__(self, parent=None, shortcut=None):
        super().__init__(parent)
        self.shortcut = shortcut or {}
        self.icon_path = self.shortcut.get('icon', '')
        
        self.setWindowTitle("Edit Shortcut" if shortcut else "Add Shortcut")
        self.setMinimumWidth(600)
        self.setup_ui()
        
        if shortcut:
            self.load_shortcut(shortcut)
    
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout()
        
        # Form layout
        form_layout = QFormLayout()
        
        # Keyword
        self.keyword_edit = QLineEdit()
        self.keyword_edit.setPlaceholderText("e.g., 'docs', 'myapp', 'google'")
        form_layout.addRow("Keyword:", self.keyword_edit)
        
        # Type
        self.type_combo = QComboBox()
        self.type_combo.addItems(['folder', 'file', 'app', 'url'])
        self.type_combo.currentTextChanged.connect(self.on_type_changed)
        form_layout.addRow("Type:", self.type_combo)
        
        # Path
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Path or URL")
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(self.path_edit)
        path_layout.addWidget(self.browse_btn)
        form_layout.addRow("Path/URL:", path_layout)
        
        # Category
        self.category_edit = QLineEdit()
        self.category_edit.setPlaceholderText("e.g., 'Folders', 'Development', 'Social'")
        form_layout.addRow("Category:", self.category_edit)
        
        # Open With (for files)
        self.openwith_layout = QHBoxLayout()
        self.openwith_edit = QLineEdit()
        self.openwith_edit.setPlaceholderText("Optional: Application to open file with")
        self.openwith_browse_btn = QPushButton("Browse...")
        self.openwith_browse_btn.clicked.connect(self.browse_openwith)
        self.openwith_layout.addWidget(self.openwith_edit)
        self.openwith_layout.addWidget(self.openwith_browse_btn)
        
        self.openwith_label = QLabel("Open With:")
        form_layout.addRow(self.openwith_label, self.openwith_layout)
        
        # Priority
        self.priority_spin = QSpinBox()
        self.priority_spin.setRange(0, 200)
        self.priority_spin.setValue(100)
        self.priority_spin.setToolTip("Higher values appear first in search results")
        form_layout.addRow("Priority:", self.priority_spin)
        
        # Icon
        icon_group = QGroupBox("Icon")
        icon_layout = QHBoxLayout()
        
        self.icon_preview = QLabel()
        self.icon_preview.setFixedSize(48, 48)
        self.icon_preview.setScaledContents(True)
        self.icon_preview.setStyleSheet("border: 1px solid #ccc;")
        
        self.icon_path_edit = QLineEdit()
        self.icon_path_edit.setPlaceholderText("Path to icon file")
        self.icon_path_edit.textChanged.connect(self.update_icon_preview)
        
        self.icon_browse_btn = QPushButton("Browse...")
        self.icon_browse_btn.clicked.connect(self.browse_icon)
        
        icon_layout.addWidget(self.icon_preview)
        icon_layout.addWidget(self.icon_path_edit)
        icon_layout.addWidget(self.icon_browse_btn)
        icon_group.setLayout(icon_layout)
        
        layout.addLayout(form_layout)
        layout.addWidget(icon_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Initial setup
        self.on_type_changed(self.type_combo.currentText())
    
    def on_type_changed(self, shortcut_type):
        """Handle type change"""
        is_file = shortcut_type == 'file'
        self.openwith_label.setVisible(is_file)
        self.openwith_edit.setVisible(is_file)
        self.openwith_browse_btn.setVisible(is_file)
        
        # Update placeholder
        if shortcut_type == 'url':
            self.path_edit.setPlaceholderText("https://example.com")
            self.browse_btn.setEnabled(False)
        else:
            self.path_edit.setPlaceholderText(f"Path to {shortcut_type}")
            self.browse_btn.setEnabled(True)
        
        # Auto-suggest category
        if not self.category_edit.text():
            category_map = {
                'folder': 'Folders',
                'file': 'Files',
                'app': 'Apps',
                'url': 'Bookmarks'
            }
            self.category_edit.setText(category_map.get(shortcut_type, ''))
    
    def browse_path(self):
        """Browse for path"""
        shortcut_type = self.type_combo.currentText()
        
        if shortcut_type == 'folder':
            path = QFileDialog.getExistingDirectory(self, "Select Folder")
        elif shortcut_type == 'file':
            path, _ = QFileDialog.getOpenFileName(self, "Select File")
        elif shortcut_type == 'app':
            path, _ = QFileDialog.getOpenFileName(self, "Select Application", 
                                                  filter="Executables (*.exe);;All Files (*.*)")
        else:
            return
        
        if path:
            self.path_edit.setText(path)
    
    def browse_openwith(self):
        """Browse for application to open file with"""
        path, _ = QFileDialog.getOpenFileName(self, "Select Application",
                                              filter="Executables (*.exe);;All Files (*.*)")
        if path:
            self.openwith_edit.setText(path)
    
    def browse_icon(self):
        """Browse for icon file"""
        path, _ = QFileDialog.getOpenFileName(self, "Select Icon",
                                              filter="Images (*.png *.jpg *.ico *.bmp);;All Files (*.*)")
        if path:
            self.icon_path_edit.setText(path)
    
    def update_icon_preview(self, path):
        """Update icon preview"""
        if path and os.path.exists(path):
            pixmap = QPixmap(path)
            self.icon_preview.setPixmap(pixmap)
        else:
            self.icon_preview.clear()
    
    def load_shortcut(self, shortcut):
        """Load shortcut data into form"""
        self.keyword_edit.setText(shortcut.get('keyword', ''))
        
        shortcut_type = shortcut.get('type', 'app')
        index = self.type_combo.findText(shortcut_type)
        if index >= 0:
            self.type_combo.setCurrentIndex(index)
        
        self.path_edit.setText(shortcut.get('path', ''))
        self.category_edit.setText(shortcut.get('category', ''))
        self.openwith_edit.setText(shortcut.get('openWith', ''))
        self.priority_spin.setValue(shortcut.get('priority', 100))
        
        icon = shortcut.get('icon', '')
        self.icon_path_edit.setText(icon)
        if icon:
            self.update_icon_preview(icon)
    
    def get_shortcut(self):
        """Get shortcut data from form"""
        shortcut = {
            'keyword': self.keyword_edit.text().strip(),
            'type': self.type_combo.currentText(),
            'path': self.path_edit.text().strip(),
            'category': self.category_edit.text().strip() or 'Uncategorized',
            'priority': self.priority_spin.value(),
            'icon': self.icon_path_edit.text().strip() or 'Images/shortcut.png'
        }
        
        if self.type_combo.currentText() == 'file':
            shortcut['openWith'] = self.openwith_edit.text().strip()
        
        return shortcut


class BookmarkImporter:
    """Import bookmarks from various browsers"""
    
    @staticmethod
    def get_browser_bookmark_paths():
        """Get standard bookmark file locations for different browsers"""
        local_appdata = os.getenv('LOCALAPPDATA', '')
        appdata = os.getenv('APPDATA', '')
        
        paths = {
            'Chrome': Path(local_appdata) / 'Google' / 'Chrome' / 'User Data' / 'Default' / 'Bookmarks',
            'Edge': Path(local_appdata) / 'Microsoft' / 'Edge' / 'User Data' / 'Default' / 'Bookmarks',
            'Opera': Path(appdata) / 'Opera Software' / 'Opera Stable' / 'Bookmarks',
            'Brave': Path(local_appdata) / 'BraveSoftware' / 'Brave-Browser' / 'User Data' / 'Default' / 'Bookmarks',
        }
        
        return {name: path for name, path in paths.items() if path.exists()}
    
    @staticmethod
    def parse_chromium_bookmarks(bookmark_file):
        """Parse Chromium-based browser bookmarks (Chrome, Edge, Opera, Brave)"""
        try:
            with open(bookmark_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            bookmarks = []
            
            def extract_bookmarks(node, folder_path=''):
                """Recursively extract bookmarks from bookmark tree"""
                if isinstance(node, dict):
                    node_type = node.get('type')
                    
                    if node_type == 'url':
                        # This is a bookmark
                        bookmarks.append({
                            'name': node.get('name', ''),
                            'url': node.get('url', ''),
                            'folder': folder_path
                        })
                    elif node_type == 'folder':
                        # This is a folder, recurse into children
                        folder_name = node.get('name', '')
                        new_path = f"{folder_path}/{folder_name}" if folder_path else folder_name
                        
                        children = node.get('children', [])
                        for child in children:
                            extract_bookmarks(child, new_path)
                
                elif isinstance(node, list):
                    for item in node:
                        extract_bookmarks(item, folder_path)
            
            # Start extraction from bookmark roots
            roots = data.get('roots', {})
            for root_name, root_node in roots.items():
                if root_name in ['bookmark_bar', 'other', 'synced']:
                    extract_bookmarks(root_node)
            
            return bookmarks
        except Exception as e:
            print(f"Error parsing bookmarks: {e}")
            return []


class BookmarkImportDialog(QDialog):
    """Dialog for importing bookmarks"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_bookmarks = []
        
        self.setWindowTitle("Import Bookmarks")
        self.setMinimumSize(700, 500)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the dialog UI"""
        layout = QVBoxLayout()
        
        # Browser selection
        browser_group = QGroupBox("Select Browser")
        browser_layout = QVBoxLayout()
        
        self.browser_combo = QComboBox()
        self.available_browsers = BookmarkImporter.get_browser_bookmark_paths()
        
        if self.available_browsers:
            self.browser_combo.addItems(self.available_browsers.keys())
        else:
            self.browser_combo.addItem("(No browsers found - use Browse)")
            self.browser_combo.setEnabled(False)
        
        browser_layout.addWidget(QLabel("Browser:"))
        browser_layout.addWidget(self.browser_combo)
        
        # Button layout for Load and Browse
        btn_layout = QHBoxLayout()
        
        load_btn = QPushButton("Load Bookmarks")
        load_btn.clicked.connect(self.load_bookmarks)
        load_btn.setEnabled(bool(self.available_browsers))
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_bookmarks)
        
        btn_layout.addWidget(load_btn)
        btn_layout.addWidget(browse_btn)
        browser_layout.addLayout(btn_layout)
        
        browser_group.setLayout(browser_layout)
        layout.addWidget(browser_group)
        
        # Bookmark list
        list_group = QGroupBox("Select Bookmarks to Import")
        list_layout = QVBoxLayout()
        
        self.bookmark_list = QListWidget()
        self.bookmark_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        list_layout.addWidget(self.bookmark_list)
        
        # Selection controls
        select_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.bookmark_list.selectAll)
        deselect_all_btn = QPushButton("Deselect All")
        deselect_all_btn.clicked.connect(self.bookmark_list.clearSelection)
        select_layout.addWidget(select_all_btn)
        select_layout.addWidget(deselect_all_btn)
        select_layout.addStretch()
        list_layout.addLayout(select_layout)
        
        list_group.setLayout(list_layout)
        layout.addWidget(list_group)
        
        # Import settings
        settings_group = QGroupBox("Import Settings")
        settings_layout = QFormLayout()
        
        self.default_category = QLineEdit("Bookmarks")
        self.default_priority = QSpinBox()
        self.default_priority.setRange(0, 200)
        self.default_priority.setValue(80)
        
        self.use_folder_as_category = QCheckBox("Use bookmark folder as category")
        self.use_folder_as_category.setChecked(True)
        
        settings_layout.addRow("Default Category:", self.default_category)
        settings_layout.addRow("Default Priority:", self.default_priority)
        settings_layout.addRow("", self.use_folder_as_category)
        
        settings_group.setLayout(settings_layout)
        layout.addWidget(settings_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.import_btn = QPushButton("Import Selected")
        self.import_btn.clicked.connect(self.accept)
        self.import_btn.setEnabled(False)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(self.import_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def browse_bookmarks(self):
        """Browse for a bookmarks file manually"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select Bookmarks File",
            "",
            "Bookmark Files (Bookmarks);;JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            self.load_bookmarks_from_file(Path(file_path), "Custom Location")
    
    def load_bookmarks(self):
        """Load bookmarks from selected browser"""
        browser = self.browser_combo.currentText()
        bookmark_file = self.available_browsers.get(browser)
        
        if not bookmark_file or not bookmark_file.exists():
            QMessageBox.warning(self, "Error", f"Bookmark file not found for {browser}")
            return
        
        self.load_bookmarks_from_file(bookmark_file, browser)
    
    def load_bookmarks_from_file(self, bookmark_file, source_name):
        """Load and parse bookmarks from a file"""
        # Parse bookmarks
        progress = QProgressDialog("Loading bookmarks...", None, 0, 0, self)
        progress.setWindowModality(Qt.WindowModality.WindowModal)
        progress.show()
        
        QApplication.processEvents()
        
        bookmarks = BookmarkImporter.parse_chromium_bookmarks(bookmark_file)
        
        progress.close()
        
        if not bookmarks:
            QMessageBox.information(self, "No Bookmarks", "No bookmarks found in the selected file.")
            return
        
        # Populate list
        self.bookmark_list.clear()
        self.all_bookmarks = bookmarks
        
        for bookmark in bookmarks:
            folder = bookmark['folder'] or 'Root'
            name = bookmark['name'] or bookmark['url']
            item_text = f"{name} ({folder})"
            self.bookmark_list.addItem(item_text)
        
        self.import_btn.setEnabled(True)
        QMessageBox.information(self, "Success", f"Loaded {len(bookmarks)} bookmarks from {source_name}")
    
    def get_selected_shortcuts(self):
        """Convert selected bookmarks to shortcuts"""
        selected_items = self.bookmark_list.selectedItems()
        selected_indices = [self.bookmark_list.row(item) for item in selected_items]
        
        shortcuts = []
        for idx in selected_indices:
            bookmark = self.all_bookmarks[idx]
            
            # Determine category
            if self.use_folder_as_category.isChecked() and bookmark['folder']:
                category = bookmark['folder'].replace('/', ' > ')
            else:
                category = self.default_category.text()
            
            # Create keyword from name (lowercase, replace spaces with dashes)
            name = bookmark['name'] or bookmark['url']
            keyword = name.lower().replace(' ', '-').replace('/', '-')[:30]
            
            # Remove special characters
            keyword = ''.join(c for c in keyword if c.isalnum() or c == '-')
            
            # Create shortcut with relative icon path
            shortcut = {
                'keyword': keyword,
                'type': 'url',
                'path': bookmark['url'],
                'category': category,
                'priority': self.default_priority.value(),
                'icon': 'Images/bookmark.png'  # Keep relative path
            }
            shortcuts.append(shortcut)
        
        return shortcuts


class ShortcutsEditorWindow(QMainWindow):
    """Main editor window"""
    
    def __init__(self):
        super().__init__()
        
        # Load settings first
        self.settings = QSettings('AMoorer', 'ShortcutsEditor')
        
        # Determine shortcuts file location (custom or default)
        custom_location = self.settings.value('custom_shortcuts_location', '')
        if custom_location and os.path.exists(os.path.dirname(custom_location)):
            self.shortcuts_file = custom_location
        else:
            self.shortcuts_file = self.find_shortcuts_file()
        
        self.shortcuts = []
        
        self.setWindowTitle("Flow Launcher Shortcuts Editor")
        self.setMinimumSize(900, 600)
        
        self.restore_geometry()
        self.setup_menu()
        self.setup_ui()
        self.load_shortcuts()
    
    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        change_location_action = QAction("Change Save Location...", self)
        change_location_action.triggered.connect(self.change_save_location)
        file_menu.addAction(change_location_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def find_shortcuts_file(self):
        """Find the shortcuts.json file"""
        # Try sibling plugin directory first
        plugin_dir = Path(__file__).parent.parent / 'Flow.Launcher.Plugin.Shortcuts'
        shortcuts_file = plugin_dir / 'shortcuts.json'
        
        if shortcuts_file.exists():
            return str(shortcuts_file)
        
        # Try Flow Launcher installation
        appdata = os.getenv('APPDATA')
        if appdata:
            fl_path = Path(appdata) / 'FlowLauncher' / 'Plugins' / 'Flow.Launcher.Plugin.Shortcuts' / 'shortcuts.json'
            if fl_path.exists():
                return str(fl_path)
        
        # Default to development location
        return str(shortcuts_file)
    
    def setup_ui(self):
        """Setup the main UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Shortcuts Manager")
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Info label
        info = QLabel(f"Editing: {self.shortcuts_file}")
        info.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(info)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['Keyword', 'Type', 'Path/URL', 'Category', 'Priority', 'Icon'])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setColumnWidth(0, 120)
        self.table.setColumnWidth(1, 80)
        self.table.setColumnWidth(2, 300)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 80)
        self.table.setColumnWidth(5, 100)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.doubleClicked.connect(self.edit_shortcut)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Add Shortcut")
        self.add_btn.clicked.connect(self.add_shortcut)
        
        self.edit_btn = QPushButton("Edit")
        self.edit_btn.clicked.connect(self.edit_shortcut)
        
        self.delete_btn = QPushButton("Delete")
        self.delete_btn.clicked.connect(self.delete_shortcut)
        
        self.import_btn = QPushButton("Import Bookmarks...")
        self.import_btn.clicked.connect(self.import_bookmarks)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_shortcuts)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.import_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(button_layout)
        
        # Status
        self.status_label = QLabel(f"Loaded {len(self.shortcuts)} shortcuts")
        self.status_label.setStyleSheet("padding: 10px;")
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout)
    
    def load_shortcuts(self):
        """Load shortcuts from JSON file"""
        try:
            if os.path.exists(self.shortcuts_file):
                with open(self.shortcuts_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.shortcuts = data.get('shortcuts', [])
            else:
                self.shortcuts = []
                # Create empty file
                self.save_shortcuts()
            
            self.update_table()
            self.status_label.setText(f"Loaded {len(self.shortcuts)} shortcuts")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load shortcuts:\n{e}")
    
    def save_shortcuts(self):
        """Save shortcuts to JSON file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.shortcuts_file), exist_ok=True)
            
            with open(self.shortcuts_file, 'w', encoding='utf-8') as f:
                json.dump({'shortcuts': self.shortcuts}, f, indent=2, ensure_ascii=False)
            
            self.status_label.setText(f"Saved {len(self.shortcuts)} shortcuts")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save shortcuts:\n{e}")
            return False
    
    def update_table(self):
        """Update table with current shortcuts"""
        self.table.setRowCount(len(self.shortcuts))
        
        for row, shortcut in enumerate(self.shortcuts):
            self.table.setItem(row, 0, QTableWidgetItem(shortcut.get('keyword', '')))
            self.table.setItem(row, 1, QTableWidgetItem(shortcut.get('type', '')))
            self.table.setItem(row, 2, QTableWidgetItem(shortcut.get('path', '')))
            self.table.setItem(row, 3, QTableWidgetItem(shortcut.get('category', '')))
            self.table.setItem(row, 4, QTableWidgetItem(str(shortcut.get('priority', 100))))
            self.table.setItem(row, 5, QTableWidgetItem(shortcut.get('icon', '')))
    
    def add_shortcut(self):
        """Add a new shortcut"""
        dialog = ShortcutDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            shortcut = dialog.get_shortcut()
            
            if not shortcut['keyword']:
                QMessageBox.warning(self, "Warning", "Keyword is required")
                return
            
            # Check for duplicate keyword
            if any(s.get('keyword') == shortcut['keyword'] for s in self.shortcuts):
                QMessageBox.warning(self, "Warning", f"Keyword '{shortcut['keyword']}' already exists")
                return
            
            self.shortcuts.append(shortcut)
            if self.save_shortcuts():
                self.update_table()
    
    def edit_shortcut(self):
        """Edit selected shortcut"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Please select a shortcut to edit")
            return
        
        shortcut = self.shortcuts[row]
        dialog = ShortcutDialog(self, shortcut)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated = dialog.get_shortcut()
            
            if not updated['keyword']:
                QMessageBox.warning(self, "Warning", "Keyword is required")
                return
            
            # Check for duplicate keyword (excluding current)
            if any(i != row and s.get('keyword') == updated['keyword'] for i, s in enumerate(self.shortcuts)):
                QMessageBox.warning(self, "Warning", f"Keyword '{updated['keyword']}' already exists")
                return
            
            self.shortcuts[row] = updated
            if self.save_shortcuts():
                self.update_table()
    
    def delete_shortcut(self):
        """Delete selected shortcut"""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Please select a shortcut to delete")
            return
        
        keyword = self.shortcuts[row].get('keyword', '')
        reply = QMessageBox.question(self, "Confirm Delete",
                                     f"Delete shortcut '{keyword}'?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            self.shortcuts.pop(row)
            if self.save_shortcuts():
                self.update_table()
    
    def import_bookmarks(self):
        """Import bookmarks from browsers"""
        dialog = BookmarkImportDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            imported_shortcuts = dialog.get_selected_shortcuts()
            
            if not imported_shortcuts:
                QMessageBox.information(self, "No Selection", "No bookmarks were selected for import.")
                return
            
            # Check for duplicate keywords
            existing_keywords = {s.get('keyword') for s in self.shortcuts}
            duplicates = []
            added_count = 0
            
            for shortcut in imported_shortcuts:
                keyword = shortcut['keyword']
                
                # Handle duplicates by appending a number
                original_keyword = keyword
                counter = 1
                while keyword in existing_keywords:
                    keyword = f"{original_keyword}-{counter}"
                    counter += 1
                    if counter > 1 and keyword != original_keyword:
                        duplicates.append(original_keyword)
                
                shortcut['keyword'] = keyword
                self.shortcuts.append(shortcut)
                existing_keywords.add(keyword)
                added_count += 1
            
            if self.save_shortcuts():
                self.update_table()
                
                msg = f"Successfully imported {added_count} bookmark(s)!"
                if duplicates:
                    msg += f"\n\nNote: {len(duplicates)} keyword(s) were renamed to avoid duplicates."
                
                QMessageBox.information(self, "Import Complete", msg)
    
    def change_save_location(self):
        """Change the shortcuts file save location"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Choose Shortcuts Save Location",
            self.shortcuts_file,
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            # Ensure it has .json extension
            if not file_path.endswith('.json'):
                file_path += '.json'
            
            # Ask to copy existing shortcuts
            if os.path.exists(self.shortcuts_file) and self.shortcuts:
                reply = QMessageBox.question(
                    self,
                    "Copy Existing Shortcuts?",
                    f"Copy existing {len(self.shortcuts)} shortcuts to the new location?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # Save to new location
                    old_file = self.shortcuts_file
                    self.shortcuts_file = file_path
                    self.save_shortcuts()
                else:
                    self.shortcuts_file = file_path
                    self.shortcuts = []
            else:
                self.shortcuts_file = file_path
            
            # Save the custom location
            self.settings.setValue('custom_shortcuts_location', self.shortcuts_file)
            
            # Reload
            self.load_shortcuts()
            
            QMessageBox.information(
                self,
                "Location Changed",
                f"Shortcuts will now be saved to:\n{self.shortcuts_file}"
            )
    
    def show_about(self):
        """Show about dialog"""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About Shortcuts Editor")
        about_dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("<h2>Flow Launcher Shortcuts Editor</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Version and date
        version_label = QLabel("<b>Version:</b> 1.0.0<br><b>Date:</b> December 2024")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # Description
        desc = QTextEdit()
        desc.setReadOnly(True)
        desc.setHtml("""
        <h3>About</h3>
        <p>A powerful GUI editor for managing Flow Launcher shortcuts. Create and organize 
        shortcuts for folders, files, applications, and URLs.</p>
        
        <h3>Features</h3>
        <ul>
            <li><b>Multiple Shortcut Types:</b> Folders, Files, Apps, URLs</li>
            <li><b>Browser Bookmark Import:</b> Import from Chrome, Edge, Opera, Brave</li>
            <li><b>Category Organization:</b> Organize shortcuts by custom categories</li>
            <li><b>Priority Control:</b> Set display priority (0-200)</li>
            <li><b>Icon Support:</b> Custom icons for each shortcut</li>
            <li><b>Flexible Storage:</b> Choose where shortcuts are saved</li>
        </ul>
        
        <h3>Flow Launcher Plugin</h3>
        <p>This editor works with the <b>Flow.Launcher.Plugin.Shortcuts</b> plugin.</p>
        <ul>
            <li><b>Action Keyword:</b> <code>s</code></li>
            <li><b>List Shortcuts:</b> <code>s shortcutlist</code></li>
            <li><b>Use Shortcut:</b> <code>s [keyword]</code></li>
        </ul>
        
        <h3>Usage</h3>
        <ol>
            <li>Click <b>Add Shortcut</b> to create a new shortcut</li>
            <li>Fill in the keyword, type, path, and category</li>
            <li>Optionally set priority and custom icon</li>
            <li>Import bookmarks using <b>Import Bookmarks...</b></li>
            <li>Changes are saved automatically</li>
        </ol>
        
        <h3>Author</h3>
        <p><b>Andy Moorer</b><br>
        GitHub: <a href="https://github.com/AMoorer/am_flowlauncher_plugins">AMoorer/am_flowlauncher_plugins</a></p>
        """)
        layout.addWidget(desc)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(about_dialog.close)
        layout.addWidget(close_btn)
        
        about_dialog.setLayout(layout)
        about_dialog.exec()
    
    def restore_geometry(self):
        """Restore window geometry from settings"""
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
    
    def closeEvent(self, event):
        """Save geometry on close"""
        self.settings.setValue('geometry', self.saveGeometry())
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Shortcuts Editor")
    app.setOrganizationName("AMoorer")
    
    window = ShortcutsEditorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
