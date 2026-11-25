# Dry-run: python generate_app_configs.py
# Apply  : python generate_app_configs.py --apply --force

from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path.cwd()
APPS_DIR = BASE_DIR / "apps"
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


def write_conf(path: Path, content: str, apply: bool, force: bool) -> str:
    if path.exists() and path.read_text(encoding="utf-8", errors="ignore").strip() and not force:
        return "SKIPPED (already populated)"
    if apply:
        path.write_text(content, encoding="utf-8")
        return "WRITTEN"
    return "WOULD WRITE"


def main() -> None:
    apply = "--apply" in sys.argv
    force = "--force" in sys.argv
    print(f"\n=== Updating conf.py files [{'APPLY' if apply else 'DRY-RUN'}] ===\n")

    for domain_dir in sorted(APPS_DIR.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name in SKIP_DIRS or domain_dir.name == "common":
            continue

        domain = domain_dir.name
        if (domain_dir / "apps.py").exists():
            conf_path = domain_dir / "conf.py"
            status = write_conf(conf_path, render_conf_py(f"apps.{domain}", domain, domain), apply, force)
            print(f"[{status}] {conf_path.relative_to(BASE_DIR)}")

        for sub_dir in sorted(domain_dir.iterdir()):
            if not sub_dir.is_dir() or sub_dir.name in SKIP_DIRS:
                continue
            if (sub_dir / "apps.py").exists():
                sub_name = sub_dir.name
                conf_path = sub_dir / "conf.py"
                status = write_conf(conf_path, render_conf_py(f"apps.{domain}.{sub_name}", domain, sub_name), apply, force)
                print(f"[{status}] {conf_path.relative_to(BASE_DIR)}")

    if not apply:
        print("\nRun: python generate_app_configs.py --apply --force")


if __name__ == "__main__":
    main()