#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Shortcuts plugin
Run this to test plugin functionality without Flow Launcher
"""

import sys
import os
import json

# Add plugin to path
sys.path.insert(0, os.path.dirname(__file__))

from main import Shortcuts


def print_results(results, title="Results"):
    """Pretty print results"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    
    if not results:
        print("No results")
        return
    
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result.get('Title', 'N/A')}")
        print(f"   Subtitle: {result.get('SubTitle', 'N/A')}")
        print(f"   Icon: {result.get('IcoPath', 'N/A')}")
        print(f"   Score: {result.get('Score', 'N/A')}")
        
        action = result.get('JsonRPCAction', {})
        if action:
            print(f"   Action: {action.get('method', 'N/A')}({action.get('parameters', [])})")


def test_query():
    """Test query functionality"""
    plugin = Shortcuts()
    
    print("\n" + "="*60)
    print("TESTING SHORTCUTS PLUGIN")
    print("="*60)
    
    # Test: Empty query (should show shortcutlist)
    print("\n[TEST 1] Empty Query")
    results = plugin.query("")
    print_results(results, "[TEST 1] Empty Query Results")
    
    # Test: shortcutlist command
    print("\n[TEST 2] shortcutlist Command")
    results = plugin.query("shortcutlist")
    print_results(results, "[TEST 2] shortcutlist Results")
    
    # Test: Search by keyword
    if plugin.shortcuts:
        first_keyword = plugin.shortcuts[0].get('keyword', 'test')
        print(f"\n[TEST 3] Search for '{first_keyword}'")
        results = plugin.query(first_keyword)
        print_results(results, f"[TEST 3] Search '{first_keyword}' Results")
        
        # Test: Partial search
        if len(first_keyword) > 2:
            partial = first_keyword[:2]
            print(f"\n[TEST 4] Partial Search for '{partial}'")
            results = plugin.query(partial)
            print_results(results, f"[TEST 4] Partial Search '{partial}' Results")
    else:
        print("\n[INFO] No shortcuts configured. Add shortcuts using the editor.")
    
    # Test: Non-existent keyword
    print("\n[TEST 5] Non-existent Keyword")
    results = plugin.query("nonexistentxyz123")
    print_results(results, "[TEST 5] Non-existent Keyword Results")
    
    # Test: Context menu
    if plugin.shortcuts:
        print("\n[TEST 6] Context Menu")
        shortcut_json = json.dumps(plugin.shortcuts[0])
        context_results = plugin.context_menu(shortcut_json)
        print_results(context_results, "[TEST 6] Context Menu Results")


def test_data_operations():
    """Test data loading and saving"""
    plugin = Shortcuts()
    
    print("\n" + "="*60)
    print("DATA OPERATIONS TEST")
    print("="*60)
    
    print(f"\nShortcuts file: {plugin.shortcuts_file}")
    print(f"File exists: {os.path.exists(plugin.shortcuts_file)}")
    print(f"Shortcuts loaded: {len(plugin.shortcuts)}")
    
    if plugin.shortcuts:
        print("\nFirst shortcut:")
        print(json.dumps(plugin.shortcuts[0], indent=2))
    else:
        print("\nNo shortcuts configured.")
        print("Run the editor to add shortcuts:")
        print("  python ../ShortcutsEditor/editor.py")


def test_actions():
    """Test action methods"""
    plugin = Shortcuts()
    
    print("\n" + "="*60)
    print("ACTION METHODS TEST")
    print("="*60)
    
    # Test do_nothing
    print("\n[TEST] do_nothing()")
    try:
        plugin.do_nothing()
        print("[OK] Success")
    except Exception as e:
        print(f"[FAIL] Failed: {e}")
    
    # Test open_editor (don't actually execute)
    print("\n[TEST] open_editor() - method exists")
    try:
        assert hasattr(plugin, 'open_editor')
        print("[OK] Method exists")
    except:
        print("[FAIL] Method not found")
    
    # Test copy_to_clipboard (don't actually execute)
    print("\n[TEST] copy_to_clipboard() - method exists")
    try:
        assert hasattr(plugin, 'copy_to_clipboard')
        print("[OK] Method exists")
    except:
        print("[FAIL] Method not found")


def test_result_creation():
    """Test result creation"""
    plugin = Shortcuts()
    
    print("\n" + "="*60)
    print("RESULT CREATION TEST")
    print("="*60)
    
    # Test with sample shortcut
    sample = {
        "keyword": "test",
        "type": "url",
        "path": "https://example.com",
        "category": "Testing",
        "priority": 100,
        "icon": "Images/shortcut.png"
    }
    
    print("\nSample shortcut:")
    print(json.dumps(sample, indent=2))
    
    print("\nCreated result:")
    result = plugin.create_result(sample)
    print(json.dumps(result, indent=2))


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print(" "*20 + "SHORTCUTS PLUGIN TEST SUITE")
    print("="*80)
    
    try:
        test_data_operations()
        test_query()
        test_actions()
        test_result_creation()
        
        print("\n" + "="*80)
        print(" "*30 + "TESTS COMPLETE")
        print("="*80)
        print("\nIf all tests passed, the plugin is ready to use!")
        print("Install it in Flow Launcher: %APPDATA%\\FlowLauncher\\Plugins\\")
        
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"ERROR: {e}")
        print("="*80)
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
