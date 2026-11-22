# Project Cache, Database & Migration Cleanup Utility (clean.py)

import os
import shutil
from pathlib import Path

def clean_project_files():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - ADVANCED PROJECT CLEANUP (clean.py)")
    print("=" * 65)
    
    deleted_folders_count = 0
    deleted_files_count = 0
    
    confirm = input("Are you sure you want to clean cache, temporary files, DB, and migration init files? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("❌ Cleanup cancelled.")
        return

    print("\n🔍 Scanning and cleaning project...")

    project_root = Path(__file__).resolve().parent

    # 1. Remove db.sqlite3 if exists
    db_path = project_root / "db.sqlite3"
    if db_path.exists():
        try:
            db_path.unlink()
            print(f"  🗑️ Removed database file: {db_path}")
            deleted_files_count += 1
        except Exception as e:
            print(f"  ⚠️ Error removing database: {e}")

    # 2. Clean migration __init__.py files (clear contents)
    apps_dir = project_root / "apps"
    if apps_dir.exists():
        for mig_init in apps_dir.glob("**/migrations/__init__.py"):
            try:
                mig_init.write_text("")
                print(f"  🧹 Emptied migration init: {mig_init.relative_to(project_root)}")
                deleted_files_count += 1
            except Exception as e:
                print(f"  ⚠️ Error clearing {mig_init}: {e}")

    # 3. Walk through project directories for cache and temp files
    for root, dirs, files in os.walk(project_root, topdown=False):
        # Remove __pycache__ directories
        if "__pycache__" in dirs:
            cache_path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(cache_path)
                print(f"  🗑️ Removed cache folder: {os.path.relpath(cache_path, project_root)}")
                deleted_folders_count += 1
            except Exception as e:
                print(f"  ⚠️ Error removing {cache_path}: {e}")

        # Remove compiled python files (.pyc, .pyo, logs, etc.)
        for file in files:
            if file.endswith((".pyc", ".pyo", ".log")) or file.startswith(".DS_Store"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_files_count += 1
                except Exception as e:
                    print(f"  ⚠️ Error removing {file_path}: {e}")

    print("\n" + "=" * 65)
    print(f"✅ Cleanup Complete! Removed {deleted_folders_count} cache folders, DB, and cleaned temp files.")
    print("=" * 65)

if __name__ == "__main__":
    clean_project_files()