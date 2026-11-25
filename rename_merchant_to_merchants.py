# Dry-run: python rename_merchant_to_merchants.py
# Apply  : python rename_merchant_to_merchants.py --apply
# Verify : python manage.py check

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

BASE_DIR = Path.cwd()
OLD_APP_DIR = BASE_DIR / "apps" / "users" / "merchant"
NEW_APP_DIR = BASE_DIR / "apps" / "users" / "merchants"

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules"}
SKIP_FILES = {"rename_merchant_to_merchants.py", "db.sqlite3"}
TEXT_EXTS = {".py", ".html", ".txt", ".md", ".json", ".yml", ".yaml", ".env", ".cfg", ".ini"}

# Regex replacements (safe against double-pluralizing 'merchants' -> 'merchantss')
REGEX_REPLACEMENTS: list[tuple[str, str]] = [
    (r"apps\.users\.merchant(?!s)\b", "apps.users.merchants"),
    (r"apps/users/merchant(?!s)\b", "apps/users/merchants"),
    (r"apps\\users\\merchant(?!s)\b", r"apps\\users\\merchants"),
    (r"users\.merchant(?!s)\b", "users.merchants"),
    (r"/api/v1/users/merchant(?!s)/", "/api/v1/users/merchants/"),
    (r"templates/merchant(?!s)/", "templates/merchants/"),
    (r"templates\\merchant(?!s)\\", r"templates\\merchants\\"),
    (r"'merchant(?!s)/", "'merchants/"),
    (r'"merchant(?!s)/', '"merchants/'),
    (r"'merchant(?!s):", "'merchants:"),
    (r'"merchant(?!s):', '"merchants:'),
    (r"app_name\s*=\s*'merchant(?!s)'", "app_name = 'merchants'"),
    (r'app_name\s*=\s*"merchant(?!s)"', 'app_name = "merchants"'),
    (r"path\('merchant(?!s)/'", "path('merchants/'"),
    (r'path\("merchant(?!s)/"', 'path("merchants/"'),
    (r"\bmerchant_views\b", "merchants_views"),
    (r"\bmerchant_profile\b", "merchants_profile"),
    (r"\bmerchant_service\b", "merchants_service"),
    (r"\bmerchant_serializer\b", "merchants_serializer"),
    (r"\bmerchant_forms\b", "merchants_forms"),
    (r"\bmerchant_navigation_context\b", "merchants_navigation_context"),
    (r"\bMerchantConfig\b", "MerchantsConfig"),
]


def is_text_file(p: Path) -> bool:
    return (
        p.is_file()
        and p.name not in SKIP_FILES
        and p.suffix.lower() in TEXT_EXTS
        and not any(d in SKIP_DIRS for d in p.parts)
    )


def rename_inner_files_and_dirs(root: Path, apply: bool) -> list[tuple[Path, Path]]:
    """Rename inner files/folders containing 'merchant' (skipping migrations)."""
    ops: list[tuple[Path, Path]] = []
    all_entries = sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True)
    for entry in all_entries:
        if "migrations" in entry.parts:
            continue
        if "merchant" in entry.name and "merchants" not in entry.name:
            new_name = entry.name.replace("merchant", "merchants")
            target = entry.with_name(new_name)
            ops.append((entry, target))
            if apply and entry.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                entry.rename(target)
    return ops


def update_text_references(apply: bool) -> list[Path]:
    """Update imports, URLs, template paths, and config references across the project."""
    changed_files: list[Path] = []
    compiled = [(re.compile(pattern), repl) for pattern, repl in REGEX_REPLACEMENTS]

    for p in sorted(BASE_DIR.rglob("*")):
        if not is_text_file(p):
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        updated = raw
        for pattern, repl in compiled:
            updated = pattern.sub(repl, updated)

        if updated != raw:
            changed_files.append(p)
            if apply:
                p.write_text(updated, encoding="utf-8")
    return changed_files


def ensure_app_label(apps_py_path: Path, apply: bool) -> None:
    """Keep label = 'merchant' in MerchantsConfig so existing db.sqlite3 migrations stay valid."""
    if not apps_py_path.exists():
        return
    content = apps_py_path.read_text(encoding="utf-8", errors="replace")
    if "label =" not in content and "class MerchantsConfig" in content:
        updated = content.replace(
            "name = 'apps.users.merchants'",
            "name = 'apps.users.merchants'\n    label = 'merchant'",
        ).replace(
            'name = "apps.users.merchants"',
            'name = "apps.users.merchants"\n    label = "merchant"',
        )
        if updated != content and apply:
            apps_py_path.write_text(updated, encoding="utf-8")
            print("   Added label = 'merchant' in apps/users/merchants/apps.py (protects DB migrations).")


def main() -> None:
    apply = "--apply" in sys.argv
    mode_label = "APPLY" if apply else "DRY-RUN"
    print(f"\n=== Merchant -> Merchants Migration [{mode_label}] ===\n")

    if not OLD_APP_DIR.exists() and not NEW_APP_DIR.exists():
        print("Error: 'apps/users/merchant' not found.")
        return

    if OLD_APP_DIR.exists():
        print(f"App folder rename: {OLD_APP_DIR.relative_to(BASE_DIR)} -> {NEW_APP_DIR.relative_to(BASE_DIR)}")
        if apply:
            if NEW_APP_DIR.exists():
                print("Warning: 'apps/users/merchants' already exists. Aborting folder move.")
                return
            shutil.move(str(OLD_APP_DIR), str(NEW_APP_DIR))

    scan_root = NEW_APP_DIR if (apply or NEW_APP_DIR.exists()) else OLD_APP_DIR
    if scan_root.exists():
        inner_ops = rename_inner_files_and_dirs(scan_root, apply=apply)
        print(f"Inner files/folders to rename: {len(inner_ops)}")
        for src, dst in inner_ops[:25]:
            print(f"   - {src.relative_to(BASE_DIR)} -> {dst.name}")

    changed = update_text_references(apply=apply)
    print(f"\nText/Import/URL/Template references updated in {len(changed)} file(s):")
    for cf in changed[:30]:
        print(f"   - {cf.relative_to(BASE_DIR)}")

    ensure_app_label(NEW_APP_DIR / "apps.py", apply=apply)

    if not apply:
        print("\nRun with --apply to execute:")
        print("   python rename_merchant_to_merchants.py --apply")
    else:
        print("\nDone! Now run: python manage.py check")


if __name__ == "__main__":
    main()