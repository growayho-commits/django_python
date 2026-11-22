# Git & GitHub Automation Utility


import subprocess

def git_manager():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - GIT & GITHUB UTILITY (git_hub.py)")
    print("=" * 65)
    
    print("\nSelect Git Action:")
    print("  [1] Check Git Status")
    print("  [2] Quick Commit & Push (All changes)")
    print("  [3] Pull latest changes from GitHub")
    choice = input("Enter choice [1, 2, or 3]: ").strip()

    if choice == '1':
        print("\n📊 Checking Git Status...")
        subprocess.run(["git", "status"])
        
    elif choice == '2':
        commit_message = input("\nEnter commit message (e.g., 'Update utilities'): ").strip()
        if not commit_message:
            commit_message = "Auto-update project utilities via git_hub.py"

        print("\n📦 Adding changes (git add .)...")
        add_result = subprocess.run(["git", "add", "."])
        
        if add_result.returncode == 0:
            print(f"📝 Committing changes ('{commit_message}')...")
            commit_result = subprocess.run(["git", "commit", "-m", commit_message])
            
            if commit_result.returncode == 0:
                print("\n🚀 Pushing changes to GitHub...")
                push_result = subprocess.run(["git", "push"])
                if push_result.returncode == 0:
                    print("\n✅ Successfully pushed to GitHub!")
                else:
                    print("\n❌ Error during git push.")
            else:
                print("\n⚠️ No new changes to commit or commit failed.")
        else:
            print("\n❌ Error during git add.")
            
    elif choice == '3':
        print("\n⬇️ Pulling latest changes from GitHub...")
        subprocess.run(["git", "pull"])
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    git_manager()