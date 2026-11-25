from pathlib import Path

try:
    from cli.common import APPS_DIR, PROJECT_ROOT, ask_dry_run, backup_file, create_backup_root
except ImportError:
    from common import APPS_DIR, PROJECT_ROOT, ask_dry_run, backup_file, create_backup_root

SKIP_DIRS = {"__pycache__", "migrations", "management", "templates", "static", "docs", "tests"}


def to_pascal_case(name: str) -> str:
    return "".join(part.capitalize() for part in name.split("_") if part)


def render_apps_py(app_path: str, app_name: str, keep_merchant_label: bool = False) -> str:
    cls_name = f"{to_pascal_case(app_name)}Config"
    lines = [
        "from django.apps import AppConfig",
        "",
        "",
        f"class {cls_name}(AppConfig):",
        "    default_auto_field = 'django.db.models.BigAutoField'",
        f"    name = '{app_path}'",
    ]
    if keep_merchant_label:
        lines.append("    label = 'merchant'")
    lines.append("")
    return "\n".join(lines)


def sync_empty_apps():
    print("=" * 70)
    print("   HYBRID MARKETPLACE - SAFE APPS.PY SYNC (cli/sync_apps.py)")
    print("=" * 70)

    dry_run = ask_dry_run(default_yes=True)
    backup_root = None if dry_run else create_backup_root("apps_backup")
    updated = 0

    for domain_dir in sorted(APPS_DIR.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name in SKIP_DIRS or domain_dir.name.startswith("_"):
            continue

        candidates = []
        if (domain_dir / "apps.py").exists() or domain_dir.name == "common":
            candidates.append((domain_dir, f"apps.{domain_dir.name}", domain_dir.name))

        for sub_dir in sorted(domain_dir.iterdir()):
            if sub_dir.is_dir() and sub_dir.name not in SKIP_DIRS and not sub_dir.name.startswith("_"):
                if (sub_dir / "models").is_dir() or (sub_dir / "views").is_dir() or (sub_dir / "apps.py").exists():
                    candidates.append((sub_dir, f"apps.{domain_dir.name}.{sub_dir.name}", sub_dir.name))

        for target_dir, app_path, app_name in candidates:
            apps_file = target_dir / "apps.py"
            existing = apps_file.read_text(encoding="utf-8", errors="ignore").strip() if apps_file.exists() else ""
            if existing:
                continue

            content = render_apps_py(app_path, app_name, keep_merchant_label=(app_name == "merchants"))
            if dry_run:
                print(f"  [DRY-RUN] Would populate: {apps_file.relative_to(PROJECT_ROOT)}")
            else:
                backup_file(apps_file, backup_root)
                apps_file.write_text(content, encoding="utf-8")
                print(f"  [UPDATED] Populated: {apps_file.relative_to(PROJECT_ROOT)}")
            updated += 1

    print(f"\nSummary: {updated} empty apps.py file(s) {'detected' if dry_run else 'populated'}.")


if __name__ == "__main__":
    sync_empty_apps()