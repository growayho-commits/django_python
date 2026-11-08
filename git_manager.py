import os
import subprocess
from datetime import datetime

def run_command(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def git_manager():
    print("==================================================")
    print("      GIT AUTOMATION MANAGER (PUSH & PULL)       ")
    print("==================================================")
    
    # இன்றைய தேதியை YYYY.MM.DD வடிவத்தில் எடுத்தல்
    today_version = datetime.now().strftime("%Y.%m.%d")
    print(f"[*] Today's Version Tag: {today_version}\n")
    
    # யூசரிடம் Push அல்லது Pull கேட்கும் முறை
    print("--- GUIDE ---")
    print(" 1. 'pull' -> Downloads latest changes from GitHub.")
    print(" 2. 'push' -> Uploads your local changes to GitHub.")
    print("--------------------------------------------------")
    
    action = input("Do you want to PUSH or PULL? (Enter 'push' or 'pull'): ").strip().lower()
    
    if action == 'pull':
        print("\n[*] [ACTION] Pulling latest changes from GitHub...")
        out, err, code = run_command("git pull origin main")
        if code == 0:
            print("[✓] Successfully pulled latest changes!")
            print(out)
        else:
            print(f"[X] Pull Failed: {err}")
            
    elif action == 'push':
        print(f"\n[*] [ACTION] Pushing local changes to GitHub with version [{today_version}]...")

        # மாற்றங்கள் உள்ளதா என சோதித்தல்
        status_out, _, _ = run_command("git status --porcelain")
        if not status_out:
            print("[!] No changes detected to commit/push.")
            return

        # வெர்ஷன் உறுதிப்படுத்தல் (YYYY.MM.DD)
        version_choice = input(f"Use today's version tag [{today_version}]? (y/n): ").strip().lower()
        if version_choice == 'y':
            version_tag = today_version
        else:
            version_tag = input("Enter custom version (e.g., 2026.11.07): ").strip()

        commit_msg = f"Update: version {version_tag} - Enterprise Dashboard Sync"

        # கோப்புகளைச் சேர்த்தல் மற்றும் கமிட் செய்தல்
        print("[*] Staging and committing changes...")
        run_command("git add .")
        out, err, code = run_command(f'git commit -m "{commit_msg}"')
        
        if code == 0:
            print(f"[✓] Committed successfully with version: {version_tag}")
        else:
            print(f"[!] Commit info/Notice: {out or err}")

        # GitHub-க்கு புஷ் செய்தல்
        print("[*] Pushing changes to GitHub (main)...")
        out, err, code = run_command("git push origin main")
        if code == 0:
            print("[✓] Successfully pushed to GitHub!")
        else:
            print(f"[X] Push Failed: {err}")
    else:
        print("[!] Invalid choice. Please type either 'push' or 'pull'.")

if __name__ == "__main__":
    git_manager()