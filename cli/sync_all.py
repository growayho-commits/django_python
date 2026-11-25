import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SCRIPTS = [
    "cli/sync_apps.py",
    "cli/sync_conf.py",
    "cli/sync_init.py",
    "cli/sync_urls.py",
    "cli/sync_admin.py",
]


def main():
    print("=" * 70)
    print("   HYBRID MARKETPLACE - UNIFIED SYNC ALL (cli/sync_all.py)")
    print("=" * 70)

    for script in SCRIPTS:
        script_path = BASE_DIR / script
        if not script_path.exists():
            print(f"  [SKIP] {script} not found.")
            continue
        print(f"\n>>> Running {script} ...")
        subprocess.run([sys.executable, str(script_path)], cwd=str(BASE_DIR), check=False)

    print("\n>>> Running Django System Check ...")
    res = subprocess.run([sys.executable, "manage.py", "check"], cwd=str(BASE_DIR), check=False)
    if res.returncode == 0:
        print("\n[OK] All sync scripts and Django check completed cleanly!")
    else:
        print("\n[WARNING] Django check reported issues. Please review above.")


if __name__ == "__main__":
    main()