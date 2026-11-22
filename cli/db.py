# Database Backup & Management Utility


import os
import shutil
from datetime import datetime

def manage_database():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - DATABASE BACKUP UTILITY (db.py)")
    print("=" * 65)
    
    db_file = "db.sqlite3"
    if not os.path.exists(db_file):
        print(f"❌ Error: Database file '{db_file}' not found!")
        return

    # Create backups directory if not exists
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print("\nSelect Database Action:")
    print("  [1] Create Database Backup")
    print("  [2] List Existing Backups")
    choice = input("Enter choice [1 or 2]: ").strip()

    if choice == '1':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"db_backup_{timestamp}.sqlite3"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        try:
            shutil.copy2(db_file, backup_path)
            print(f"\n✅ Success! Database backed up to: {backup_path}")
        except Exception as e:
            print(f"\n❌ Error creating backup: {e}")
            
    elif choice == '2':
        backups = [f for f in os.listdir(backup_dir) if f.endswith('.sqlite3')]
        if not backups:
            print("\n📁 No backups found in 'backups/' folder.")
        else:
            print(f"\n📁 Available Backups ({len(backups)}):")
            for idx, b in enumerate(sorted(backups, reverse=True), 1):
                b_path = os.path.join(backup_dir, b)
                size_kb = os.path.getsize(b_path) / 1024
                print(f"  [{idx}] {b} ({size_kb:.2f} KB)")
    else:
        print("❌ Invalid choice.")

if __name__ == "__main__":
    manage_database()