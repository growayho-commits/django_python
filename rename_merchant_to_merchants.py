#python rename_merchant_to_merchants.py
#python rename_merchant_to_merchants.py --apply
#python manage.py check



from __future__ import annotations

import shutil
import sys
from pathlib import Path

BASE_DIR = Path.cwd()
OLD_APP_DIR = BASE_DIR / "apps" / "users" / "merchant"
NEW_APP_DIR = BASE_DIR / "apps" / "users" / "merchants"

SKIP_DIRS = {".git", "__pycache__", "venv", ".venv", "node_modules"}
TEXT_EXTS = {".py", ".html", ".txt", ".md", ".json", ".yml", ".yaml", ".env", ".cfg", ".ini"}

# உள்ளே உள்ள கோப்புகளில் மாற்ற வேண்டிய முக்கிய reference-கள்
REPLACEMENTS: list[tuple[str, str]] = [
    ("apps.users.merchant", "apps.users.merchants"),
    ("apps/users/merchant", "apps/users/merchants"),
    ("apps\\users\\merchant", "apps\\users\\merchants"),
    ("users.merchant", "users.merchants"),
    ("templates/merchant/", "templates/merchants/"),
    ("templates\\merchant\\", "templates\\merchants\\"),
    ("'merchant/", "'merchants/"),
    ('"merchant/', '"merchants/'),
]


def is_text_file(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in TEXT_EXTS and not any(d in SKIP_DIRS for d in p.parts)


def rename_inner_files_and_dirs(root: Path, apply: bool) -> list[tuple[Path, Path]]:
    """உள்ளே உள்ள 'merchant' என்ற பெயர்கொண்ட ஃபோல்டர்/ஃபைல்களை 'merchants' என மாற்றுகிறது (bottom-up)."""
    ops: list[tuple[Path, Path]] = []
    # ஆழமான பாதைகளிலிருந்து (deepest first) தொடங்குவதால் parent மாறும்போது child path உடையாது
    all_entries = sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True)
    for entry in all_entries:
        if "merchant" in entry.name and "merchants" not in entry.name:
            new_name = entry.name.replace("merchant", "merchants")
            target = entry.with_name(new_name)
            ops.append((entry, target))
            if apply and entry.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                entry.rename(target)
    return ops


def update_text_references(apply: bool) -> list[Path]:
    """திட்டம் முழுவதும் (settings, urls, apps, views, templates, docs போன்றவற்றில்) references அப்டேட் செய்கிறது."""
    changed_files: list[Path] = []
    for p in sorted(BASE_DIR.rglob("*")):
        if not is_text_file(p):
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        updated = raw
        for old_str, new_str in REPLACEMENTS:
            updated = updated.replace(old_str, new_str)

        if updated != raw:
            changed_files.append(p)
            if apply:
                p.write_text(updated, encoding="utf-8")
    return changed_files


def main() -> None:
    apply = "--apply" in sys.argv
    mode_label = "APPLY (உண்மையாக மாற்றும்)" if apply else "DRY-RUN (சோதனை மட்டும் - எதுவும் மாறாது)"
    print(f"\n=== Merchant -> Merchants Migration [{mode_label}] ===\n")

    if not OLD_APP_DIR.exists() and not NEW_APP_DIR.exists():
        print("❌ 'apps/users/merchant' காணப்படவில்லை.")
        return

    if OLD_APP_DIR.exists():
        print(f"📁 App folder rename: {OLD_APP_DIR.relative_to(BASE_DIR)} -> {NEW_APP_DIR.relative_to(BASE_DIR)}")
        if apply:
            if NEW_APP_DIR.exists():
                print("⚠️ எச்சரிக்கை: 'apps/users/merchants' ஏற்கனவே உள்ளது; கவனமாகச் சரிபார்க்கவும்.")
                return
            shutil.move(str(OLD_APP_DIR), str(NEW_APP_DIR))

    scan_root = NEW_APP_DIR if (apply or NEW_APP_DIR.exists()) else OLD_APP_DIR
    if scan_root.exists():
        inner_ops = rename_inner_files_and_dirs(scan_root, apply=apply)
        print(f"📄 Inner files/folders with 'merchant': {len(inner_ops)}")
        for src, dst in inner_ops[:20]:
            print(f"   • {src.relative_to(BASE_DIR)}  -->  {dst.name}")
        if len(inner_ops) > 20:
            print(f"   ... மற்றும் {len(inner_ops) - 20} உருப்படிகள்.")

    changed = update_text_references(apply=apply)
    print(f"\n✏️ Text/Import/Template references updated in {len(changed)} file(s):")
    for cf in changed[:25]:
        print(f"   • {cf.relative_to(BASE_DIR)}")
    if len(changed) > 25:
        print(f"   ... மற்றும் {len(changed) - 25} கோப்புகள்.")

    if not apply:
        print("\n👉 மாற்றங்களை உறுதியாகச் செய்ய இந்தக் கமெண்ட்டை இயக்கவும்:")
        print("   python rename_merchant_to_merchants.py --apply")
    else:
        print("\n✅ முடிந்தது! இப்போது கீழ்க்கண்ட சரிபார்ப்புகளைச் செய்யவும்:")
        print("   1. python manage.py check")
        print("   2. தேவைப்பட்டால் migrations / app label சரிபார்க்கவும்")


if __name__ == "__main__":
    main()


