import os
import re
import sys
from pathlib import Path

CLI_DIR = str(Path(__file__).resolve().parent)
BASE_DIR = Path(__file__).resolve().parent.parent

# Prevent cli/inspect.py from shadowing Python's standard library inspect module
sys.path = [p for p in sys.path if os.path.abspath(p or ".") != os.path.abspath(CLI_DIR)]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")

import django
django.setup()

from django.urls import Resolver404, resolve

CONTEXT_FILES = [
    "apps/users/superusers/context_processors.py",
    "apps/users/executives/context_processors.py",
    "apps/users/sellers/context_processors.py",
    "apps/users/merchants/context_processors.py",
    "apps/users/members/context_processors.py",
]


def main():
    print("=" * 70)
    print("   HYBRID MARKETPLACE - MENU URL AUDIT (cli/sync_menus.py)")
    print("=" * 70)
    broken = 0
    checked = 0

    for rel in CONTEXT_FILES:
        path = BASE_DIR / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        urls = re.findall(r"['\"](/api/v1/[^'\"]+)['\"]", text)
        print(f"\n[{rel}] ({len(urls)} URLs)")
        for u in urls:
            checked += 1
            clean_path = u.split("?", 1)[0]
            try:
                resolve(clean_path)
                print(f"  [OK]   {u}")
            except Resolver404:
                broken += 1
                print(f"  [404]  {u}")

    print(f"\nSummary: Checked {checked} menu URLs, {broken} broken.")


if __name__ == "__main__":
    main()