import os
import shutil

def clean_project():
    root_dir = "."
    print("🧹 Cleaning up cache files and database...")
    
    deleted_pycache = 0
    deleted_pyc = 0
    db_removed = False

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 1. Remove __pycache__ folders
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(pycache_path, ignore_errors=True)
            deleted_pycache += 1

        # 2. Remove .pyc and .pyo files
        for filename in filenames:
            if filename.endswith(('.pyc', '.pyo')):
                file_path = os.path.join(dirpath, filename)
                os.remove(file_path)
                deleted_pyc += 1

        # 3. Remove db.sqlite3
        if "db.sqlite3" in filenames:
            db_path = os.path.join(dirpath, "db.sqlite3")
            os.remove(db_path)
            db_removed = True

    print(f"✅ Removed {deleted_pycache} '__pycache__' folders.")
    print(f"✅ Removed {deleted_pyc} compiled python files.")
    if db_removed:
        print("✅ Removed 'db.sqlite3' database file.")
    else:
        print("ℹ️ 'db.sqlite3' not found.")

if __name__ == "__main__":
    clean_project()