# Dependency & Package Manager Utility

import subprocess
import sys

def manage_dependencies():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - DEPENDENCY MANAGER (dep.py)")
    print("=" * 65)
    
    print("\nSelect Dependency Action:")
    print("  [1] Install a new package (pip install)")
    print("  [2] Export/Update requirements.txt")
    print("  [3] Install requirements from requirements.txt")
    choice = input("Enter choice [1, 2, or 3]: ").strip()

    if choice == '1':
        pkg_name = input("\nEnter package name to install (e.g., requests, pillow): ").strip()
        if pkg_name:
            print(f"\n📦 Installing {pkg_name}...")
            subprocess.run([sys.executable, "-m", "pip", "install", pkg_name])
            print("\n💡 Tip: Run option [2] to update requirements.txt")
        else:
            print("❌ Package name cannot be empty.")
            
    elif choice == '2':
        print("\n📝 Updating requirements.txt...")
        try:
            with open("requirements.txt", "w", encoding="utf-8") as f:
                subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=f)
            print("✅ Successfully updated requirements.txt!")
        except Exception as e:
            print(f"❌ Error updating requirements: {e}")
            
    elif choice == '3':
        print("\n⬇️ Installing packages from requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    manage_dependencies()