# =====================================================================
# HYBRID MARKETPLACE - ADVANCED MASTER TOOLKIT CONTROLLER (cli.py)
# ---------------------------------------------------------------------
# Details: This master script acts as the centralized terminal control room
# for the Hybrid Marketplace project. It automatically discovers all utility 
# Python scripts located in the 'cli/' directory, presents an interactive 
# numeric menu with color-coded styling, executes the selected tool, 
# measures execution time, and provides seamless developer automation.
# =====================================================================

import os
import subprocess
import sys
import time

# Directory where all utility scripts are located
TOOLS_DIR = "cli"

# ANSI Colors for Terminal Styling and High-Fi Developer Interface
class Color:
    HEADER = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

# Dictionary mapping script names to their single-line descriptions (in English)
TOOL_DESCRIPTIONS = {
    "clean.py": "Clean up project cache (__pycache__) and temporary files",
    "db.py": "Manage database backups and operations",
    "dep.py": "Manage Python packages and requirements.txt",
    "docs.py": "Generate project structure documentation",
    "extract.py": "Extract specific code files into code/ directory",
    "git_hub.py": "Automate Git and GitHub status, commit, and push",
    "inspect.py": "Inspect project and generate AI_PROJECT_CONTEXT.md",
    "logs.py": "View and manage application and error logs",
    "opener.py": "Open specific file paths directly in VS Code",
    "run.py": "Run project health checks and start local server",
    "shell.py": "Launch Django interactive shell",
    "structure.py": "Analyze and export project directory structure",
    "test.py": "Run automated system checks and unit tests"
}

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_available_tools():
    """Automatically discover all Python files in the cli/ directory in alphabetical order."""
    if not os.path.exists(TOOLS_DIR):
        os.makedirs(TOOLS_DIR)
        
    files = [f for f in os.listdir(TOOLS_DIR) if f.endswith('.py') and f != '__init__.py']
    return sorted(files)

def show_advanced_menu():
    """Display the interactive master toolkit menu and handle user execution flow."""
    while True:
        clear_screen()
        print(f"{Color.HEADER}{'=' * 75}")
        print(f"   HYBRID MARKETPLACE - ADVANCED MASTER TOOLKIT (cli.py)")
        print(f"{'=' * 75}{Color.RESET}")
        
        tools = get_available_tools()
        
        if not tools:
            print(f"{Color.RED}⚠️ Warning: No files found in '{TOOLS_DIR}/' directory!{Color.RESET}")
        else:
            print(f"📁 Source Directory: {Color.BOLD}{TOOLS_DIR}/{Color.RESET}\n")
            for idx, tool in enumerate(tools, 1):
                # Fetch description from dictionary, or show a default message if not found
                desc = TOOL_DESCRIPTIONS.get(tool, "Utility script for project management")
                print(f"  {Color.YELLOW}[{idx:2d}]{Color.RESET} {tool:<15} - {desc}")
                
        print(f"\n  {Color.RED}[ 0]{Color.RESET} Exit")
        print(f"{Color.HEADER}{'=' * 75}{Color.RESET}")
        
        choice = input(f"{Color.BOLD}👉 Enter your choice number: {Color.RESET}").strip()
        
        if choice == '0':
            print(f"\n{Color.GREEN}👋 Goodbye! Toolkit closed successfully.{Color.RESET}")
            break
            
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(tools):
                script_name = tools[idx]
                script_path = os.path.join(TOOLS_DIR, script_name)
                
                print(f"\n{Color.GREEN}🚀 Executing: {script_name}...{Color.RESET}\n" + "-" * 75)
                start_time = time.time()
                
                try:
                    # Execute the selected utility script
                    subprocess.run([sys.executable, script_path])
                except Exception as e:
                    print(f"\n{Color.RED}❌ Error occurred: {e}{Color.RESET}")
                    
                elapsed = time.time() - start_time
                print(f"\n{Color.HEADER}{'=' * 75}")
                print(f"✅ Finished in {elapsed:.2f} seconds.")
                print(f"{'=' * 75}{Color.RESET}")
                
                input(f"\n{Color.BOLD}👉 Press Enter to return to menu...{Color.RESET}")
            else:
                print(f"\n{Color.RED}❌ Invalid number! Please try a valid selection.{Color.RESET}")
                time.sleep(1.5)
        else:
            print(f"\n{Color.RED}❌ Please enter numbers only.{Color.RESET}")
            time.sleep(1.5)

if __name__ == "__main__":
    show_advanced_menu()