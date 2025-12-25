"""
Create Flow Launcher Plugin Store manifest file
Usage: python create_manifest.py [plugin_dir] [version]
"""

import os
import sys
import json
from pathlib import Path


def create_manifest(plugin_dir, version="1.0.0"):
    """Create plugin store manifest file."""
    plugin_json_path = Path(plugin_dir) / "plugin.json"
    
    if not plugin_json_path.exists():
        print(f"❌ Error: plugin.json not found in {plugin_dir}")
        return
    
    # Load plugin.json
    with open(plugin_json_path, 'r', encoding='utf-8') as f:
        plugin_data = json.load(f)
    
    guid = plugin_data.get('ID')
    name = plugin_data.get('Name')
    description = plugin_data.get('Description')
    author = plugin_data.get('Author')
    language = plugin_data.get('Language', 'python')
    website = plugin_data.get('Website', '')
    icon_path = plugin_data.get('IcoPath', 'Images/icon.png')
    
    # Extract GitHub info from website
    if 'github.com' in website:
        parts = website.rstrip('/').split('/')
        github_user = parts[-2] if len(parts) >= 2 else ''
        github_repo = parts[-1] if len(parts) >= 1 else ''
    else:
        print("⚠️  Warning: Website is not a GitHub URL")
        github_user = input("GitHub username: ").strip()
        github_repo = input("GitHub repo name: ").strip()
    
    # Create manifest
    manifest = {
        "ID": guid,
        "Name": name,
        "Description": description,
        "Author": author,
        "Version": version,
        "Language": language,
        "Website": website,
        "UrlDownload": f"https://github.com/{github_user}/{github_repo}/releases/download/v{version}/{github_repo}.zip",
        "UrlSourceCode": website,
        "IcoPath": f"https://cdn.jsdelivr.net/gh/{github_user}/{github_repo}@main/{icon_path.replace(chr(92), '/')}"
    }
    
    # Create filename
    manifest_filename = f"{name}-{guid}.json"
    
    # Save manifest
    with open(manifest_filename, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"✅ Manifest created: {manifest_filename}")
    print(f"\n📋 Manifest content:")
    print(json.dumps(manifest, indent=2))
    print(f"\n📝 Next steps:")
    print(f"1. Fork https://github.com/Flow-Launcher/Flow.Launcher.PluginsManifest")
    print(f"2. Add {manifest_filename} to the plugins/ directory")
    print(f"3. Create pull request")
    print(f"4. Wait for approval")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python create_manifest.py [plugin_dir] [version]")
        print("Example: python create_manifest.py Flow.Launcher.Plugin.Shortcuts 1.0.0")
        return
    
    plugin_dir = sys.argv[1]
    version = sys.argv[2] if len(sys.argv) > 2 else "1.0.0"
    
    create_manifest(plugin_dir, version)


if __name__ == "__main__":
    main()
