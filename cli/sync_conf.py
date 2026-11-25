from pathlib import Path

try:
    from cli.common import APPS_DIR, PROJECT_ROOT, ask_dry_run, backup_file, create_backup_root
except ImportError:
    from common import APPS_DIR, PROJECT_ROOT, ask_dry_run, backup_file, create_backup_root

SKIP_DIRS = {"__pycache__", "migrations", "management", "templates", "static", "docs", "tests"}

USER_APP_EXTRAS = {
    "superusers": {
        "role": "superuser",
        "dashboard_url": "/api/v1/users/superusers/dashboard/",
        "context_processor": "apps.users.superusers.context_processors.enterprise_navigation_context",
    },
    "executives": {
        "role": "executive",
        "dashboard_url": "/api/v1/users/executives/dashboard/",
        "context_processor": "apps.users.executives.context_processors.executive_navigation_context",
    },
    "sellers": {
        "role": "seller",
        "dashboard_url": "/api/v1/users/sellers/overview/",
        "context_processor": "apps.users.sellers.context_processors.seller_navigation_context",
    },
    "merchants": {
        "role": "merchant",
        "dashboard_url": "/api/v1/users/merchants/overview/",
        "context_processor": "apps.users.merchants.context_processors.merchants_navigation_context",
    },
    "members": {
        "role": "member",
        "dashboard_url": "/api/v1/users/members/dashboard/",
        "context_processor": "apps.users.members.context_processors.member_navigation_context",
    },
}


def render_conf_py(app_path: str, domain: str, sub_name: str) -> str:
    lines = [
        "# App configuration",
        "APP_CONFIG = {",
        f'    "app_path": "{app_path}",',
        f'    "domain": "{domain}",',
        f'    "name": "{sub_name}",',
        f'    "title": "{sub_name.replace("_", " ").title()}",',
        '    "enabled": True,',
    ]
    if domain == "users" and sub_name in USER_APP_EXTRAS:
        extras = USER_APP_EXTRAS[sub_name]
        lines.append(f'    "role": "{extras["role"]}",')
        lines.append(f'    "dashboard_url": "{extras["dashboard_url"]}",')
        lines.append(f'    "context_processor": "{extras["context_processor"]}",')
    lines.append("}")
    lines.append("")
    return "\n".join(lines)


def sync_all_conf():
    print("=" * 70)
    print("   HYBRID MARKETPLACE - SAFE CONF.PY SYNC (cli/sync_conf.py)")
    print("=" * 70)

    dry_run = ask_dry_run(default_yes=True)
    backup_root = None if dry_run else create_backup_root("conf_backup")
    changed = 0

    for domain_dir in sorted(APPS_DIR.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name in SKIP_DIRS or domain_dir.name.startswith("_"):
            continue

        domain = domain_dir.name
        targets = []
        if (domain_dir / "apps.py").exists():
            targets.append((domain_dir / "conf.py", f"apps.{domain}", domain, domain))

        for sub_dir in sorted(domain_dir.iterdir()):
            if sub_dir.is_dir() and sub_dir.name not in SKIP_DIRS and (sub_dir / "apps.py").exists():
                targets.append((sub_dir / "conf.py", f"apps.{domain}.{sub_dir.name}", domain, sub_dir.name))

        for conf_path, app_path, dom, sub_name in targets:
            new_content = render_conf_py(app_path, dom, sub_name)
            old_content = conf_path.read_text(encoding="utf-8", errors="ignore") if conf_path.exists() else ""
            if old_content == new_content:
                continue

            if dry_run:
                print(f"  [DRY-RUN] Would sync: {conf_path.relative_to(PROJECT_ROOT)}")
            else:
                backup_file(conf_path, backup_root)
                conf_path.write_text(new_content, encoding="utf-8")
                print(f"  [UPDATED] Synced: {conf_path.relative_to(PROJECT_ROOT)}")
            changed += 1

    print(f"\nSummary: {changed} conf.py file(s) {'need sync' if dry_run else 'synced'}.")


if __name__ == "__main__":
    sync_all_conf()