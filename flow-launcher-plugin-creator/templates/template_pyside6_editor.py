"""
PySide6 GUI Editor Template
Use this for creating data editors for Flow Launcher plugins
"""

import sys
import os
import json
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QDialog,
    QFormLayout, QLineEdit, QComboBox, QSpinBox, QLabel,
    QFileDialog, QMessageBox, QMenuBar, QTextEdit
)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QAction


class ItemDialog(QDialog):
    """Dialog for adding/editing items."""
    
    def __init__(self, parent=None, item=None):
        super().__init__(parent)
        self.item = item or {}
        self.setWindowTitle("Edit Item" if item else "Add Item")
        self.setMinimumWidth(500)
        self.setup_ui()
        
        if item:
            self.load_item()
    
    def setup_ui(self):
        """Setup dialog UI."""
        layout = QFormLayout()
        
        # Name field
        self.name_input = QLineEdit()
        layout.addRow("Name:", self.name_input)
        
        # Type field
        self.type_combo = QComboBox()
        self.type_combo.addItems(["folder", "file", "app", "url"])
        layout.addRow("Type:", self.type_combo)
        
        # Path/URL field
        self.path_input = QLineEdit()
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_path)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(browse_btn)
        layout.addRow("Path/URL:", path_layout)
        
        # Category field
        self.category_input = QLineEdit()
        layout.addRow("Category:", self.category_input)
        
        # Priority field
        self.priority_spin = QSpinBox()
        self.priority_spin.setRange(0, 200)
        self.priority_spin.setValue(100)
        layout.addRow("Priority:", self.priority_spin)
        
        # Icon field
        self.icon_input = QLineEdit()
        icon_btn = QPushButton("Browse...")
        icon_btn.clicked.connect(self.browse_icon)
        
        icon_layout = QHBoxLayout()
        icon_layout.addWidget(self.icon_input)
        icon_layout.addWidget(icon_btn)
        layout.addRow("Icon:", icon_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addRow("", button_layout)
        
        self.setLayout(layout)
    
    def load_item(self):
        """Load item data into form."""
        self.name_input.setText(self.item.get('name', ''))
        self.type_combo.setCurrentText(self.item.get('type', 'file'))
        self.path_input.setText(self.item.get('path', ''))
        self.category_input.setText(self.item.get('category', ''))
        self.priority_spin.setValue(self.item.get('priority', 100))
        self.icon_input.setText(self.item.get('icon', ''))
    
    def browse_path(self):
        """Browse for file/folder path."""
        item_type = self.type_combo.currentText()
        
        if item_type == 'folder':
            path = QFileDialog.getExistingDirectory(self, "Select Folder")
        elif item_type in ['file', 'app']:
            path, _ = QFileDialog.getOpenFileName(self, "Select File")
        else:
            return
        
        if path:
            self.path_input.setText(path)
    
    def browse_icon(self):
        """Browse for icon file."""
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Icon",
            "",
            "Images (*.png *.ico *.jpg *.bmp);;All Files (*.*)"
        )
        if path:
            self.icon_input.setText(path)
    
    def get_data(self):
        """Get form data as dictionary."""
        return {
            'name': self.name_input.text(),
            'type': self.type_combo.currentText(),
            'path': self.path_input.text(),
            'category': self.category_input.text(),
            'priority': self.priority_spin.value(),
            'icon': self.icon_input.text()
        }


class EditorWindow(QMainWindow):
    """Main editor window."""
    
    def __init__(self):
        super().__init__()
        
        # Settings
        self.settings = QSettings('Author', 'AppName')
        
        # Find data file
        self.data_file = self.find_data_file()
        self.items = []
        
        self.setWindowTitle("Data Editor")
        self.setMinimumSize(900, 600)
        
        self.restore_geometry()
        self.setup_menu()
        self.setup_ui()
        self.load_data()
    
    def find_data_file(self):
        """Find the data JSON file."""
        # Try multiple locations
        possible_paths = [
            Path(__file__).parent / '..' / 'Plugin' / 'data.json',
            Path.home() / 'AppData' / 'Roaming' / 'FlowLauncher' / 'Plugins' / 'YourPlugin' / 'data.json',
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        # Default to first path
        return str(possible_paths[0])
    
    def setup_menu(self):
        """Setup menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        change_location = QAction("Change Save Location...", self)
        change_location.triggered.connect(self.change_save_location)
        file_menu.addAction(change_location)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_ui(self):
        """Setup main UI."""
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Name', 'Type', 'Path', 'Category', 'Priority'])
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Item")
        add_btn.clicked.connect(self.add_item)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Item")
        edit_btn.clicked.connect(self.edit_item)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete Item")
        delete_btn.clicked.connect(self.delete_item)
        button_layout.addWidget(delete_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Status
        self.status_label = QLabel(f"Loaded {len(self.items)} items")
        self.status_label.setStyleSheet("padding: 10px;")
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def load_data(self):
        """Load data from JSON file."""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.items = data.get('items', [])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load data: {e}")
            self.items = []
        
        self.refresh_table()
    
    def save_data(self):
        """Save data to JSON file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump({'items': self.items}, f, indent=2)
            
            self.status_label.setText(f"Saved {len(self.items)} items")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save data: {e}")
    
    def refresh_table(self):
        """Refresh table with current data."""
        self.table.setRowCount(len(self.items))
        
        for i, item in enumerate(self.items):
            self.table.setItem(i, 0, QTableWidgetItem(item.get('name', '')))
            self.table.setItem(i, 1, QTableWidgetItem(item.get('type', '')))
            self.table.setItem(i, 2, QTableWidgetItem(item.get('path', '')))
            self.table.setItem(i, 3, QTableWidgetItem(item.get('category', '')))
            self.table.setItem(i, 4, QTableWidgetItem(str(item.get('priority', 100))))
        
        self.status_label.setText(f"Loaded {len(self.items)} items")
    
    def add_item(self):
        """Add new item."""
        dialog = ItemDialog(self)
        if dialog.exec():
            self.items.append(dialog.get_data())
            self.save_data()
            self.refresh_table()
    
    def edit_item(self):
        """Edit selected item."""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select an item to edit")
            return
        
        dialog = ItemDialog(self, self.items[row])
        if dialog.exec():
            self.items[row] = dialog.get_data()
            self.save_data()
            self.refresh_table()
    
    def delete_item(self):
        """Delete selected item."""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Please select an item to delete")
            return
        
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this item?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            del self.items[row]
            self.save_data()
            self.refresh_table()
    
    def change_save_location(self):
        """Change data file save location."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Choose Save Location",
            self.data_file,
            "JSON Files (*.json);;All Files (*.*)"
        )
        
        if file_path:
            if not file_path.endswith('.json'):
                file_path += '.json'
            
            self.data_file = file_path
            self.settings.setValue('custom_data_location', file_path)
            self.save_data()
            
            QMessageBox.information(
                self,
                "Location Changed",
                f"Data will now be saved to:\n{file_path}"
            )
    
    def show_about(self):
        """Show about dialog."""
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About")
        about_dialog.setMinimumSize(500, 400)
        
        layout = QVBoxLayout()
        
        title = QLabel("<h2>Data Editor</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        info = QTextEdit()
        info.setReadOnly(True)
        info.setHtml("""
        <h3>About</h3>
        <p>A data editor for Flow Launcher plugins.</p>
        
        <h3>Usage</h3>
        <ol>
            <li>Click <b>Add Item</b> to create new items</li>
            <li>Select and click <b>Edit Item</b> to modify</li>
            <li>Select and click <b>Delete Item</b> to remove</li>
            <li>Changes are saved automatically</li>
        </ol>
        
        <h3>Author</h3>
        <p><b>Your Name</b><br>
        GitHub: <a href="https://github.com/yourname">yourname</a></p>
        """)
        layout.addWidget(info)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(about_dialog.close)
        layout.addWidget(close_btn)
        
        about_dialog.setLayout(layout)
        about_dialog.exec()
    
    def restore_geometry(self):
        """Restore window geometry from settings."""
        geometry = self.settings.value('geometry')
        if geometry:
            self.restoreGeometry(geometry)
    
    def closeEvent(self, event):
        """Save geometry on close."""
        self.settings.setValue('geometry', self.saveGeometry())
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("DataEditor")
    
    window = EditorWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
