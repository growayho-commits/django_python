# Automated Test & Health Check Utility


import os
import subprocess
import sys

def run_tests():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - TEST & HEALTH CHECK (test.py)")
    print("=" * 65)
    
    if not os.path.exists("manage.py"):
        print("❌ Error: 'manage.py' not found!")
        return

    print("\nSelect Testing Option:")
    print("  [1] Run Django System Checks (Health Check)")
    print("  [2] Run Unit Tests (python manage.py test)")
    print("  [3] Check Missing Migrations")
    choice = input("Enter choice [1, 2, or 3]: ").strip()

    if choice == '1':
        print("\n🔍 Running Django System Checks...")
        subprocess.run([sys.executable, "manage.py", "check"])
        
    elif choice == '2':
        print("\n🧪 Running Unit Tests...")
        app_name = input("Enter app name to test (or press Enter to test all): ").strip()
        cmd = [sys.executable, "manage.py", "test"]
        if app_name:
            cmd.append(app_name)
        subprocess.run(cmd)
        
    elif choice == '3':
        print("\n📦 Checking Migration Status...")
        subprocess.run([sys.executable, "manage.py", "showmigrations"])
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    run_tests()