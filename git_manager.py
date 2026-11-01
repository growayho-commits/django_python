import datetime
import subprocess
import sys

def run_git_command(command, error_message):
    """Utility to run git commands safely using Windows Shell"""
    try:
        # shell=True சேர்ப்பதன் மூலம் Windows PowerShell/CMD மூலம் Git கட்டளைகள் தடையின்றி இயங்கும்
        result = subprocess.run(command, capture_output=True, text=True, check=True, shell=True)
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Error: {error_message}")
        if e.stderr:
            print(e.stderr.strip())
        return False
    except Exception as e:
        print(f"[!] System Error: {e}")
        return False

def do_git_pull():
    print("\n[!] Fetching and Pulling latest code from GitHub...")
    if run_git_command("git pull", "Failed to pull updates from remote repository."):
        print("\n==================================================")
        print(" SUCCESS: Successfully pulled latest updates!")
        print("==================================================")

def do_git_push():
    # 1. Generate CalVer version (yyyy.mm.dd)
    today_version = datetime.date.today().strftime("%Y.%m.%d")
    print(f"\n[*] CalVer Version : v{today_version}")
    
    # 2. Get optional commit message
    custom_msg = input("Enter commit message (or press [ENTER] for default): ").strip()
    commit_message = f"v{today_version} - {custom_msg}" if custom_msg else f"v{today_version} - Automated project sync"

    # 3. Git Status check
    print("\n[1/4] Checking git status...")
    try:
        status_res = subprocess.run("git status --porcelain", capture_output=True, text=True, shell=True)
        if not status_res.stdout.strip():
            print("[!] No changes detected to commit!")
            return
    except Exception as e:
        print(f"[!] Error checking status: {e}")
        return

    # 4. Stage, Commit & Push
    print("[2/4] Staging all files...")
    if not run_git_command("git add .", "Failed to stage files."): return

    print(f"[3/4] Committing as '{commit_message}'...")
    if not run_git_command(f'git commit -m "{commit_message}"', "Failed to commit."): return

    print("[4/4] Pushing to GitHub...")
    if run_git_command("git push", "Failed to push to GitHub. Check your network or credentials."):
        print("\n==================================================")
        print(f" SUCCESS: Pushed to GitHub as v{today_version}!")
        print("==================================================")

def main():
    print("==================================================")
    print("      HYBRID MARKETPLACE - ADVANCED GIT MANAGER     ")
    print("==================================================\n")
    print("  [1] Push (Auto Stage + CalVer Commit + Push)")
    print("  [2] Pull (Get Latest Code from Remote)")
    print("  [3] Status (Check Modified/Untracked files)")
    print("==================================================")
    
    choice = input("Select option (1 for Push, 2 for Pull, 3 for Status, or press [ENTER] for Push) -> ").strip()
    
    if choice == '2' or choice.lower() == 'pull':
        do_git_pull()
    elif choice == '3' or choice.lower() == 'status':
        run_git_command("git status", "Failed to check status.")
    else:
        do_git_push()

if __name__ == "__main__":
    main()