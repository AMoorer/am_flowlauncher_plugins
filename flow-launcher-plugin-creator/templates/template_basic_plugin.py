"""
Basic Flow Launcher Plugin Template
Use this as a starting point for simple query-response plugins.
"""

import sys
import os

# Add parent directory to path for flowlauncher module
parent_folder_path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(parent_folder_path)
sys.path.append(os.path.join(parent_folder_path, 'lib'))
sys.path.append(os.path.join(parent_folder_path, '..',

 'lib'))

from flowlauncher import FlowLauncher


class BasicPlugin(FlowLauncher):
    def query(self, query):
        """
        Handle user query and return results.
        
        Args:
            query (str): User's search query
            
        Returns:
            list: List of result dictionaries
        """
        results = []
        
        # Example: Echo the query back
        if query.strip():
            results.append({
                "Title": f"You typed: {query}",
                "SubTitle": "Press Enter to copy to clipboard",
                "IcoPath": "Images/icon.png",
                "JsonRPCAction": {
                    "method": "copy_to_clipboard",
                    "parameters": [query]
                }
            })
        else:
            results.append({
                "Title": "Type something...",
                "SubTitle": "Enter your query to see results",
                "IcoPath": "Images/icon.png"
            })
        
        return results
    
    def copy_to_clipboard(self, text):
        """Copy text to clipboard."""
        try:
            import pyperclip
            pyperclip.copy(text)
            return True
        except Exception as e:
            self.logger.error(f"Error copying to clipboard: {e}")
            return False
    
    def context_menu(self, data):
        """
        Provide context menu options (right-click).
        
        Args:
            data: Context data from the result
            
        Returns:
            list: List of context menu items
        """
        return [
            {
                "Title": "Example Action",
                "SubTitle": "This appears on right-click",
                "JsonRPCAction": {
                    "method": "example_action",
                    "parameters": []
                }
            }
        ]
    
    def example_action(self):
        """Example action method."""
        pass


if __name__ == "__main__":
    BasicPlugin()
