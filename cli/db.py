import shutil
from datetime import datetime

try:
    from cli.common import BACKUPS_DIR, PROJECT_ROOT
except ImportError:
    from common import BACKUPS_DIR, PROJECT_ROOT


def manage_database():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - DATABASE BACKUP & RESTORE (cli/db.py)")
    print("=" * 65)

    db_file = PROJECT_ROOT / "db.sqlite3"
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)

    print("\nSelect Database Action:")
    print("  [1] Create Database Backup")
    print("  [2] List Existing Backups")
    print("  [3] Restore Database from Backup")
    choice = input("Enter choice [1, 2, or 3]: ").strip()

    if choice == "1":
        if not db_file.exists():
            print(f"Error: Database file '{db_file}' not found!")
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUPS_DIR / f"db_backup_{timestamp}.sqlite3"
        shutil.copy2(db_file, backup_path)
        print(f"\nSuccess! Database backed up to: {backup_path.relative_to(PROJECT_ROOT)}")

    elif choice in ("2", "3"):
        backups = sorted(BACKUPS_DIR.glob("db_backup_*.sqlite3"), reverse=True)
        if not backups:
            print("\nNo database backups found in 'backups/' folder.")
            return

        print(f"\nAvailable Backups ({len(backups)}):")
        for idx, b in enumerate(backups, 1):
            size_kb = b.stat().st_size / 1024
            print(f"  [{idx}] {b.name} ({size_kb:.2f} KB)")

        if choice == "3":
            sel = input("\nEnter backup number to restore (or 0 to cancel): ").strip()
            if not sel.isdigit() or int(sel) < 1 or int(sel) > len(backups):
                print("Restore cancelled.")
                return
            chosen = backups[int(sel) - 1]
            if input(f"Restore '{chosen.name}' over db.sqlite3? [y/N]: ").strip().lower() != "y":
                print("Restore cancelled.")
                return
            if db_file.exists():
                safety = BACKUPS_DIR / f"db_before_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sqlite3"
                shutil.copy2(db_file, safety)
                print(f"Safety copy saved: {safety.relative_to(PROJECT_ROOT)}")
            shutil.copy2(chosen, db_file)
            print(f"Success! Restored db.sqlite3 from {chosen.name}")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    manage_database()