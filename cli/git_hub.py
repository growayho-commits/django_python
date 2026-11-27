import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from cli.common import PROJECT_ROOT, ensure_documents_dir
except ImportError:
    from common import PROJECT_ROOT, ensure_documents_dir

CLOUD_HOST = "ubuntu@130.210.8.93"
CLOUD_DIR = "/home/ubuntu/django_python"


def _find_ssh_key() -> str:
    downloads = Path.home() / "Downloads"
    keys = sorted(downloads.glob("*.key"), key=lambda p: p.stat().st_mtime, reverse=True)
    if keys:
        return str(keys[0])
    return input("Enter path to Oracle Cloud .key file: ").strip().strip('"')


def _ask_yes_no(prompt_text: str) -> bool:
    ans = input(f"{prompt_text} [y/N]: ").strip().lower()
    return ans in ("y", "yes")


def deploy_to_oracle_cloud() -> None:
    key = _find_ssh_key()
    print(f"\nDeploying latest GitHub code to Oracle Cloud ({CLOUD_HOST})...")
    cmd = (
        f"cd {CLOUD_DIR} && git pull origin main && "
        "source venv/bin/activate && "
        "DJANGO_SETTINGS_MODULE=settings.production python manage.py migrate && "
        "DJANGO_SETTINGS_MODULE=settings.production python manage.py collectstatic --noinput && "
        "sudo systemctl restart hybrid_marketplace && "
        "echo 'ORACLE CLOUD DEPLOYED SUCCESSFULLY!'"
    )
    subprocess.run(["ssh", "-i", key, CLOUD_HOST, cmd], stdin=subprocess.DEVNULL)


def push_local_users_to_cloud() -> None:
    key = _find_ssh_key()
    print("\nExporting local users from db.sqlite3 (One-Way -> Oracle Cloud PostgreSQL)...")
    export_code = """
import json, os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.local")
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
rows = []
for u in User.objects.all():
    role = "member"
    for attr, rname in [
        ("superuser_profile", "superuser"),
        ("executive_profile", "executive"),
        ("merchants_profile", "merchant"),
        ("seller_profile", "seller"),
        ("member_profile", "member"),
    ]:
        try:
            if getattr(u, attr, None) is not None:
                role = rname
                break
        except Exception:
            pass
    if u.is_superuser:
        role = "superuser"
    rows.append({
        "email": u.email,
        "password": u.password,
        "first_name": getattr(u, "first_name", "") or "",
        "last_name": getattr(u, "last_name", "") or "",
        "is_active": u.is_active,
        "is_staff": u.is_staff,
        "is_superuser": u.is_superuser,
        "role": role,
    })
print(json.dumps(rows))
"""
    res = subprocess.run([sys.executable, "-c", export_code], cwd=PROJECT_ROOT, capture_output=True, text=True)
    if res.returncode != 0:
        print("Export failed:", res.stderr)
        return
    tmp_local = PROJECT_ROOT / "tmp_users_sync.json"
    tmp_local.write_text(res.stdout.strip(), encoding="utf-8")

    print("Uploading user list to Oracle Cloud...")
    subprocess.run(["scp", "-i", key, str(tmp_local), f"{CLOUD_HOST}:/tmp/tmp_users_sync.json"], check=False)

    remote_import = f"""
cd {CLOUD_DIR}
source venv/bin/activate
DJANGO_SETTINGS_MODULE=settings.production python - << 'PYEOF'
import json, os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.production')
django.setup()
from django.contrib.auth import get_user_model
from apps.users.members.models.member_profile import MemberProfile
from apps.users.sellers.models.seller_profile import SellerProfile
from apps.users.merchants.models.merchants_profile import MerchantProfile
from apps.users.executives.models.executive_profile import ExecutiveProfile
from apps.users.superusers.models.superuser_models import SuperuserProfile

User = get_user_model()
data = json.load(open("/tmp/tmp_users_sync.json", encoding="utf-8"))
added, skipped = 0, 0
profile_map = {{
    "member": MemberProfile,
    "seller": SellerProfile,
    "merchant": MerchantProfile,
    "executive": ExecutiveProfile,
    "superuser": SuperuserProfile,
}}
for item in data:
    email = item["email"]
    if User.objects.filter(email__iexact=email).exists():
        skipped += 1
        continue
    u = User(
        email=email,
        first_name=item["first_name"],
        last_name=item["last_name"],
        is_active=item["is_active"],
        is_staff=item["is_staff"],
        is_superuser=item["is_superuser"],
    )
    u.password = item["password"]
    u.save()
    p_cls = profile_map.get(item.get("role"), MemberProfile)
    p_cls.objects.get_or_create(user=u)
    added += 1
print(f"One-Way Sync Complete -> Added: {{added}} new users | Skipped existing: {{skipped}}")
PYEOF
rm -f /tmp/tmp_users_sync.json
"""
    subprocess.run(["ssh", "-i", key, CLOUD_HOST, "bash -s"], input=remote_import.replace("\r\n", "\n").encode("utf-8"))
    if tmp_local.exists():
        tmp_local.unlink()


def append_work_log(tag_name: str, summary: str) -> None:
    docs_dir = ensure_documents_dir()
    log_file = docs_dir / "WORK_LOG.md"
    if not log_file.exists():
        log_file.write_text("# Hybrid Marketplace - Date-Wise Work Log\n\n", encoding="utf-8")
    entry = f"## {tag_name}\n- {summary}\n\n"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(entry)
    print(f"Updated work log: {log_file.relative_to(PROJECT_ROOT)}")


def git_manager():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - GIT & GITHUB UTILITY (cli/git_hub.py)")
    print("=" * 65)

    print("\nSelect Git Action:")
    print("  [1] Check Git Status")
    print("  [2] Quick Commit & Push (All changes)")
    print("  [3] Pull latest changes from GitHub")
    print("  [4] Create & Push yyyy.mm.dd Version Tag + Update WORK_LOG.md")
    print("  [5] Compress Local Git Space (git gc)")
    print("  [6] Deploy to Oracle Cloud (130.210.8.93) [Pull + Migrate + Restart]")
    print("  [7] Push Local Registered Users -> Oracle Cloud PostgreSQL (One-Way)")
    choice = input("Enter choice [1-7]: ").strip()

    if choice == "1":
        subprocess.run(["git", "status"], cwd=PROJECT_ROOT)

    elif choice == "2":
        msg = input("\nEnter commit message: ").strip() or "Update project files"
        if subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT).returncode == 0:
            if subprocess.run(["git", "commit", "-m", msg], cwd=PROJECT_ROOT).returncode == 0:
                if subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT).returncode == 0:
                    if _ask_yes_no("\nDeploy pushed code to Oracle Cloud (130.210.8.93)?"):
                        deploy_to_oracle_cloud()
                    if _ask_yes_no("Push newly registered local users to Oracle Cloud PostgreSQL (One-Way)?"):
                        push_local_users_to_cloud()

    elif choice == "3":
        subprocess.run(["git", "pull", "origin", "main"], cwd=PROJECT_ROOT)

    elif choice == "4":
        default_tag = datetime.now().strftime("%Y.%m.%d")
        tag_name = input(f"\nEnter version tag [Default: {default_tag}]: ").strip() or default_tag
        summary = input("Enter release summary: ").strip() or f"Release {tag_name}"
        append_work_log(tag_name, summary)
        subprocess.run(["git", "add", "."], cwd=PROJECT_ROOT)
        subprocess.run(["git", "commit", "-m", f"Release {tag_name}: {summary}"], cwd=PROJECT_ROOT)
        subprocess.run(["git", "tag", "-a", tag_name, "-m", f"Version {tag_name}: {summary}"], cwd=PROJECT_ROOT)
        subprocess.run(["git", "push", "origin", "main"], cwd=PROJECT_ROOT)
        subprocess.run(["git", "push", "origin", tag_name], cwd=PROJECT_ROOT)

    elif choice == "5":
        print("\nCompressing local .git repository space...")
        subprocess.run(["git", "gc", "--aggressive", "--prune=now"], cwd=PROJECT_ROOT)
        print("Done! Local Git space compressed.")

    elif choice == "6":
        if _ask_yes_no("Deploy latest GitHub main branch to Oracle Cloud (130.210.8.93)?"):
            deploy_to_oracle_cloud()

    elif choice == "7":
        if _ask_yes_no("Push new local users (db.sqlite3) to Oracle Cloud PostgreSQL (One-Way)?"):
            push_local_users_to_cloud()

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    git_manager()
