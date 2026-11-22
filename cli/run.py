# One-Click Project Launcher & Health Check Utility


import os
import subprocess
import sys

def run_project():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - ONE-CLICK LAUNCHER (run.py)")
    print("=" * 65)
    
    # 1. Check for manage.py
    if not os.path.exists("manage.py"):
        print("❌ Error: 'manage.py' not found! Make sure you are in the project root folder.")
        return

    # 2. Run Django System Checks (Health Check)
    print("\n🔍 Running Django System & Health Checks...")
    check_result = subprocess.run([sys.executable, "manage.py", "check"])
    
    if check_result.returncode != 0:
        print("⚠️ Warning: System checks found some issues. Please review above.")
        choice = input("Do you still want to start the server? [y/N]: ").strip().lower()
        if choice != 'y':
            print("❌ Server startup cancelled.")
            return
    else:
        print("✅ System checks passed successfully!")

    # 3. Check for pending migrations
    print("\n📦 Checking database migrations...")
    subprocess.run([sys.executable, "manage.py", "makemigrations", "--dry-run"])

    # 4. Start Development Server
    print("\n🚀 Starting Django Development Server...")
    print("=" * 65)
    try:
        subprocess.run([sys.executable, "manage.py", "runserver"])
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user. Goodbye!")

if __name__ == "__main__":
    run_project()