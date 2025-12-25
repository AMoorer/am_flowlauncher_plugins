"""
Generate complete Flow Launcher plugin project structure
Usage: python generate_plugin_scaffold.py [plugin_name]
"""

import os
import sys
import uuid
import json
from pathlib import Path


def generate_guid():
    """Generate a GUID for the plugin."""
    return str(uuid.uuid4()).upper()


def create_plugin_json(plugin_name, author, description, action_keyword, guid):
    """Create plugin.json content."""
    return json.dumps({
        "ID": guid,
        "ActionKeyword": action_keyword,
        "Name": plugin_name,
        "Description": description,
        "Author": author,
        "Version": "1.0.0",
        "Language": "python",
        "Website": f"https://github.com/{author}/Flow.Launcher.Plugin.{plugin_name}",
        "IcoPath": "Images\\icon.png",
        "ExecuteFileName": "main.py"
    }, indent=4)


def create_requirements_txt():
    """Create requirements.txt content."""
    return """flowlauncher>=0.2.0
pyperclip>=1.8.0
"""


def create_main_py(plugin_name):
    """Create main.py content."""
    return f'''"""
{plugin_name} Plugin for Flow Launcher
"""

import sys
import os

parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, '..', 'lib'))

from flowlauncher import FlowLauncher


class {plugin_name}(FlowLauncher):
    def query(self, query):
        """Handle user query."""
        results = []
        
        if query.strip():
            results.append({{
                "Title": f"You searched for: {{query}}",
                "SubTitle": "Press Enter to continue",
                "IcoPath": "Images/icon.png",
                "JsonRPCAction": {{
                    "method": "handle_action",
                    "parameters": [query]
                }}
            }})
        else:
            results.append({{
                "Title": "Type something...",
                "SubTitle": "Start typing to see results",
                "IcoPath": "Images/icon.png"
            }})
        
        return results
    
    def handle_action(self, query):
        """Handle the action."""
        # TODO: Implement your action logic
        pass


if __name__ == "__main__":
    {plugin_name}()
'''


def create_readme(plugin_name, description):
    """Create README.md content."""
    return f"""# {plugin_name} Plugin for Flow Launcher

{description}

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

1. Copy this folder to `%APPDATA%\\FlowLauncher\\Plugins\\`
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Restart Flow Launcher

## Usage

Type the action keyword followed by your query.

## Development

### Testing
```bash
python test.py
```

### Building
See `.github/workflows/publish-release.yml` for automated builds.

## License

MIT License
"""


def create_test_py(plugin_name):
    """Create test.py content."""
    return f'''"""
Test suite for {plugin_name}
"""

def test_query():
    """Test query method."""
    # TODO: Add tests
    print("[OK] Query test passed")


def test_action():
    """Test action methods."""
    # TODO: Add tests
    print("[OK] Action test passed")


if __name__ == "__main__":
    print("Running tests...")
    test_query()
    test_action()
    print("All tests passed!")
'''


def create_github_workflow():
    """Create GitHub Actions workflow."""
    return """name: Publish Release

on:
  workflow_dispatch:
  release:
    types: [published]

jobs:
  publish:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Create plugin package
        run: |
          mkdir release
          xcopy /E /I . release\\Flow.Launcher.Plugin.* /EXCLUDE:exclude.txt
      
      - name: Create ZIP archive
        run: |
          powershell -command "Compress-Archive -Path 'release\\*' -DestinationPath 'plugin.zip' -Force"
      
      - name: Upload to release
        uses: softprops/action-gh-release@v1
        with:
          files: plugin.zip
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""


def generate_scaffold(plugin_name, author, description, action_keyword):
    """Generate complete plugin scaffold."""
    guid = generate_guid()
    
    # Create directory structure
    plugin_dir = f"Flow.Launcher.Plugin.{plugin_name}"
    os.makedirs(plugin_dir, exist_ok=True)
    os.makedirs(f"{plugin_dir}/Images", exist_ok=True)
    os.makedirs(f"{plugin_dir}/.github/workflows", exist_ok=True)
    
    # Create files
    files = {
        f"{plugin_dir}/plugin.json": create_plugin_json(plugin_name, author, description, action_keyword, guid),
        f"{plugin_dir}/requirements.txt": create_requirements_txt(),
        f"{plugin_dir}/main.py": create_main_py(plugin_name),
        f"{plugin_dir}/README.md": create_readme(plugin_name, description),
        f"{plugin_dir}/test.py": create_test_py(plugin_name),
        f"{plugin_dir}/.github/workflows/publish-release.yml": create_github_workflow(),
    }
    
    for filepath, content in files.items():
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ Plugin scaffold created: {plugin_dir}")
    print(f"📋 GUID: {guid}")
    print(f"\nNext steps:")
    print(f"1. cd {plugin_dir}")
    print(f"2. Add an icon to Images/icon.png")
    print(f"3. Implement your plugin logic in main.py")
    print(f"4. Test with: python test.py")
    print(f"5. Install in Flow Launcher plugins directory")


def main():
    """Main function."""
    print("Flow Launcher Plugin Scaffold Generator")
    print("=" * 50)
    
    plugin_name = input("Plugin name (e.g., 'Shortcuts'): ").strip()
    author = input("Author name (e.g., 'Andy Moorer'): ").strip()
    description = input("Description: ").strip()
    action_keyword = input("Action keyword (e.g., 's'): ").strip()
    
    if not all([plugin_name, author, description, action_keyword]):
        print("❌ All fields are required!")
        return
    
    generate_scaffold(plugin_name, author, description, action_keyword)


if __name__ == "__main__":
    main()
