import os
import shutil
from pathlib import Path

try:
    from cli.common import PROJECT_ROOT, SKIP_DIRS, ask_dry_run
except ImportError:
    from common import PROJECT_ROOT, SKIP_DIRS, ask_dry_run


def clean_project_files():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - SAFE CACHE CLEANER (cli/clean.py)")
    print("=" * 65)

    dry_run = ask_dry_run(default_yes=True)
    cache_dirs, temp_files = [], []

    for root, dirs, files in os.walk(PROJECT_ROOT):
        if any(skip in Path(root).parts for skip in SKIP_DIRS):
            continue
        if "__pycache__" in dirs:
            cache_dirs.append(Path(root) / "__pycache__")
        for file in files:
            if file.endswith((".pyc", ".pyo", ".log")) or file == ".DS_Store":
                temp_files.append(Path(root) / file)

    print(f"\nFound {len(cache_dirs)} __pycache__ folder(s) and {len(temp_files)} temp file(s).")
    print("Protected: db.sqlite3, migrations/, and documents/ will NOT be touched.")

    if dry_run:
        for d in cache_dirs[:15]:
            print(f"  [DRY-RUN] Would remove folder: {d.relative_to(PROJECT_ROOT)}")
        for f in temp_files[:15]:
            print(f"  [DRY-RUN] Would remove file  : {f.relative_to(PROJECT_ROOT)}")
        print("\nDry-run complete. Re-run and enter 'n' to execute.")
        return

    if input("Proceed to delete cache/temp files? [y/N]: ").strip().lower() != "y":
        print("Cleanup cancelled.")
        return

    removed_dirs = sum(1 for d in cache_dirs if d.exists() and not shutil.rmtree(d, ignore_errors=True))
    removed_files = 0
    for f in temp_files:
        if f.exists():
            try:
                f.unlink()
                removed_files += 1
            except OSError:
                pass

    print(f"\nDone! Removed {removed_dirs} cache folder(s) and {removed_files} temp file(s).")


if __name__ == "__main__":
    clean_project_files()