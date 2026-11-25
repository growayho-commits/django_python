import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    print("=" * 70)
    print("   HYBRID MARKETPLACE - TEST & VERIFICATION (cli/sync_tests.py)")
    print("=" * 70)
    subprocess.run([sys.executable, "manage.py", "check"], cwd=str(BASE_DIR), check=True)
    subprocess.run([sys.executable, "manage.py", "test", "--keepdb"], cwd=str(BASE_DIR), check=False)


if __name__ == "__main__":
    main()