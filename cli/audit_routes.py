import os
import re
import sys
import traceback

CLI_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CLI_DIR)
sys.path = [p for p in sys.path if os.path.abspath(p) != CLI_DIR]
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

manage_path = os.path.join(BASE_DIR, "manage.py")
with open(manage_path, "r", encoding="utf-8") as f:
    m = re.search(r"DJANGO_SETTINGS_MODULE['\"],\s*['\"]([^'\"]+)['\"]", f.read())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", m.group(1) if m else "settings.local")

import django
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory

User = get_user_model()
rf = RequestFactory()


def extract_urls(obj):
    urls = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("url", "href", "link") and isinstance(v, str) and v.startswith("/"):
                urls.append(v)
            else:
                urls.extend(extract_urls(v))
    elif isinstance(obj, (list, tuple)):
        for item in obj:
            urls.extend(extract_urls(item))
    return urls


def extract_html_links(html_text):
    links = re.findall(r'href=["\'](/[^"\'#]+)["\']', html_text)
    cleaned = []
    for link in links:
        if any(skip in link for skip in ("/logout", "/static/", "/media/", "/admin/")):
            continue
        cleaned.append(link)
    return cleaned


ROLE_CONFIG = [
    ("member", "/api/v1/users/members/dashboard/", "apps.users.members.context_processors"),
    ("seller", "/api/v1/users/sellers/overview/", "apps.users.sellers.context_processors"),
    ("merchant", "/api/v1/users/merchants/overview/", "apps.users.merchants.context_processors"),
    ("executive", "/api/v1/users/executives/dashboard/", "apps.users.executives.context_processors"),
    ("superuser", "/api/v1/users/superusers/dashboard/", "apps.users.superusers.context_processors"),
]


def find_user_for_role(role_name):
    if role_name == "superuser":
        u = User.objects.filter(is_superuser=True).first()
        if u:
            return u
    for field in ("role", "user_type", "account_type"):
        if hasattr(User, field):
            u = User.objects.filter(**{f"{field}__iexact": role_name}).first()
            if u:
                return u
    return User.objects.filter(email__icontains=role_name).first()


print("=" * 70)
print("  HYBRID MARKETPLACE - FULL E2E DASHBOARD & MENU AUDIT")
print("=" * 70)

total_checked = 0
total_errors = 0

for role_name, home_url, cp_module_path in ROLE_CONFIG:
    user = find_user_for_role(role_name)
    if not user:
        print(f"\n[SKIP] No user found for role: {role_name}")
        continue

    print(f"\n>>> ROLE: {role_name.upper()} (User: {user.email})")
    client = Client(raise_request_exception=True)
    client.force_login(user)

    queue = [home_url]
    try:
        mod = __import__(cp_module_path, fromlist=["*"])
        req = rf.get("/")
        req.user = user
        for attr in dir(mod):
            fn = getattr(mod, attr)
            if callable(fn) and not attr.startswith("_"):
                try:
                    ctx = fn(req)
                    if isinstance(ctx, dict):
                        queue.extend(extract_urls(ctx))
                except Exception:
                    pass
    except Exception as e:
        print(f"  [CP ERROR] {cp_module_path}: {e}")

    visited = set()
    idx = 0
    while idx < len(queue):
        url = queue[idx]
        idx += 1
        if url in visited:
            continue
        visited.add(url)
        total_checked += 1

        try:
            resp = client.get(url, HTTP_HOST="127.0.0.1", follow=False)
            ctype = resp.get("Content-Type", "")
            if resp.status_code >= 400:
                total_errors += 1
                print(f"  [FAIL {resp.status_code}] {url}")
            elif "application/json" in ctype and "a-p-i" in url:
                total_errors += 1
                print(f"  [WARN JSON-IN-MENU] {url} -> returns JSON instead of HTML UI")
            elif resp.status_code == 200 and "text/html" in ctype:
                body = resp.content.decode("utf-8", errors="ignore")
                for found_link in extract_html_links(body):
                    if found_link not in visited:
                        queue.append(found_link)
        except Exception as exc:
            total_errors += 1
            tb = traceback.format_exc().strip().splitlines()
            short_tb = " | ".join(tb[-3:])
            print(f"  [CRASH] {url}\n      -> {type(exc).__name__}: {exc}\n      -> {short_tb}")

print("\n" + "=" * 70)
print(f"SUMMARY: Checked {total_checked} URLs across all roles | Errors/Warnings: {total_errors}")
print("=" * 70)