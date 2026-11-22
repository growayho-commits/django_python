# =====================================================================
# HYBRID MARKETPLACE - 9-TIER ENTERPRISE URL SYNC (Automated Dashboard Fix)
# ---------------------------------------------------------------------
# Details: Automatically scans Tier-7 views and ensures robust, explicit 
# dashboard and redirection routing for superusers without 404 errors.
# =====================================================================

import ast
import os
import re
import json
from pathlib import Path
from datetime import datetime

# --- 9-Tier Enterprise Path Resolution ---
CLI_DIR = Path(__file__).resolve().parent
TIER1_ROOT = CLI_DIR.parent
TIER2_APPS = TIER1_ROOT / 'apps'
TIER1_CORE_URLS = TIER1_ROOT / 'core' / 'urls.py'
TIER9_LOGS_DIR = TIER1_ROOT / 'logs'
URL_AUDIT_LOG = TIER9_LOGS_DIR / 'sync_urls_audit.json'

TIER5_EXCLUDED_DIRS = {
    'migrations', 'tests', 'utils', 'validators', 'serializers',
    'selectors', 'services', 'permissions', 'middleware', 'listeners',
    'interfaces', 'forms', 'filters', 'exceptions', 'dtos', 'presenters',
    'signals', 'tasks', 'templates', 'views', '__pycache__', 'management', 'models', 'docs'
}

def extract_views_via_ast(sub_app_path: Path) -> list[tuple[str, str]]:
    """Scans Tier-7 view files using AST to extract functions and classes safely."""
    target_files = []
    single_view = sub_app_path / 'views.py'
    views_pkg = sub_app_path / 'views'

    if single_view.exists():
        target_files.append(single_view)
    if views_pkg.exists() and views_pkg.is_dir():
        for root, _, files in os.walk(views_pkg):
            for f in sorted(files):
                if f.endswith('.py') and f != '__init__.py' and not f.startswith('_'):
                    target_files.append(Path(root) / f)

    extracted = []
    seen = set()

    for py_file in target_files:
        try:
            source = py_file.read_text(encoding='utf-8')
            tree = ast.parse(source, filename=str(py_file))
        except (SyntaxError, UnicodeDecodeError):
            continue

        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                args = [a.arg for a in node.args.args]
                if args and args[0] == 'request' and node.name not in seen:
                    extracted.append((node.name, 'function'))
                    seen.add(node.name)

            elif isinstance(node, ast.ClassDef) and not node.name.startswith('_'):
                bases = [ast.unparse(b) for b in node.bases] if hasattr(ast, 'unparse') else []
                base_str = " ".join(bases)
                if 'ViewSet' in node.name or 'ViewSet' in base_str:
                    v_type = 'viewset'
                elif any(k in node.name or k in base_str for k in ('View', 'APIView')):
                    v_type = 'class'
                else:
                    continue

                if node.name not in seen:
                    extracted.append((node.name, v_type))
                    seen.add(node.name)

    return extracted

def generate_clean_slug(view_name: str) -> str:
    """Converts view names into clean URL slugs dynamically."""
    name = view_name
    for suffix in ('_view', 'View', '_View'):
        if name.endswith(suffix):
            name = name[:-len(suffix)]
    
    slug = re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()
    slug = slug.replace('_', '-').strip('-')
    return slug if slug else view_name.lower()

def sync_subapp_urls(group_name: str, sub_path: Path) -> dict:
    """Generates Tier-4 Sub-App urls.py with foolproof name aliases and mandatory dashboard routes."""
    sub_name = sub_path.name
    sub_urls_file = sub_path / 'urls.py'
    views_found = extract_views_via_ast(sub_path)

    lines = [
        "# Auto-generated and Synchronized by 9-Tier Enterprise cli/sync_urls.py\n",
        "from django.urls import path\n",
        "from . import views\n\n",
        f"app_name = '{sub_name}'\n\n",
        "urlpatterns = [\n"
    ]

    mapped_count = 0
    registered_names = set()

    for view_name, v_type in views_found:
        if v_type == 'viewset':
            continue

        slug = generate_clean_slug(view_name)
        base_name = view_name
        for suffix in ('_view', 'View', '_View'):
            if base_name.endswith(suffix):
                base_name = base_name[:-len(suffix)]
        base_name = base_name.lower().replace('_', '-')

        aliases = {base_name, view_name}
        
        if 'guest' in view_name.lower() or 'home' in view_name.lower() or 'index' in view_name.lower():
            aliases.add('guest_home')
            aliases.add('home')
        elif 'login' in view_name.lower():
            aliases.add('login')
        elif 'register' in view_name.lower():
            aliases.add('register')
        elif 'dashboard' in view_name.lower() or 'redirect' in view_name.lower():
            aliases.add('role_dashboard_redirect')
            aliases.add('dashboard')
            aliases.add('dashboard')
            aliases.add('admin_dashboard')

        # Add root mapping for guest_home or home
        if 'guest_home' in view_name.lower() or 'home' in view_name.lower():
            if '' not in registered_names:
                if v_type == 'class':
                    lines.append(f"    path('', views.{view_name}.as_view(), name='guest_home'),\n")
                    lines.append(f"    path('guest-home/', views.{view_name}.as_view(), name='guest_home_alt'),\n")
                else:
                    lines.append(f"    path('', views.{view_name}, name='guest_home'),\n")
                    lines.append(f"    path('guest-home/', views.{view_name}, name='guest_home_alt'),\n")
                registered_names.add('')
                mapped_count += 2

        # Add specific slug routes with name aliases
        for alias in sorted(aliases):
            if alias not in registered_names:
                if v_type == 'class':
                    lines.append(f"    path('{slug}/', views.{view_name}.as_view(), name='{alias}'),\n")
                else:
                    lines.append(f"    path('{slug}/', views.{view_name}, name='{alias}'),\n")
                registered_names.add(alias)
                mapped_count += 1

    # Guarantee Superusers explicit routes to prevent 404 on dashboard & redirect
    if sub_name == 'superusers':
        # 1. Direct Dashboard Route Mapping
        if 'dashboard' not in registered_names:
            lines.append("    path('dashboard/', views.dashboard_view, name='dashboard'),\n")
            registered_names.add('dashboard')
            mapped_count += 1
            
        # 2. Superuser Dashboard Alt Route Mapping
        if 'dashboard' not in registered_names:
            lines.append("    path('superuser-dashboard/', views.dashboard_view, name='dashboard'),\n")
            registered_names.add('dashboard')
            mapped_count += 1
            
        # 3. Role Dashboard Redirect Route Mapping
        if 'role_dashboard_redirect' not in registered_names:
            lines.append("    path('role-dashboard-redirect/', views.role_dashboard_redirect, name='role_dashboard_redirect'),\n")
            registered_names.add('role_dashboard_redirect')
            mapped_count += 1

    if mapped_count == 0:
        lines.append(f"    # No direct path views detected yet in {sub_name}\n")

    lines.append("]\n")
    sub_urls_file.write_text("".join(lines), encoding='utf-8')
    print(f"  [✔️ Tier-4 Sub-App] {group_name}/{sub_name}/urls.py ──> {mapped_count} route(s) synced")
    return {'sub_name': sub_name, 'module': f"apps.{group_name}.{sub_name}.urls", 'routes': mapped_count}

def sync_group_urls(group_name: str, sub_modules: list[dict]):
    """Aggregates Tier-4 Sub-Apps into Tier-3 Group App router with explicit namespaces."""
    group_urls_file = TIER2_APPS / group_name / 'urls.py'
    lines = [
        '"""\n',
        f'Tier-3 Group App Router: [{group_name.upper()}]\n',
        'Auto-synchronized by 9-Tier Enterprise cli/sync_urls.py\n',
        '"""\n',
        'from django.urls import path, include\n\n',
        f"app_name = '{group_name}'\n\n",
        'urlpatterns = [\n'
    ]

    for sub in sorted(sub_modules, key=lambda x: x['sub_name']):
        lines.append(f"    path('{sub['sub_name']}/', include(('{sub['module']}', '{sub['sub_name']}'))),\n")

    lines.append(']\n')
    group_urls_file.write_text("".join(lines), encoding='utf-8')
    print(f"🔗 [Tier-3 Group Router] apps/{group_name}/urls.py updated with namespaces.")

def sync_tier1_core_urls(all_group_names: list[str]):
    """Finalizes Tier-1 Core Gateway (core/urls.py) with automatic root redirection."""
    TIER1_CORE_URLS.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        '"""\n',
        'Tier-1 Core Main URL Configuration — 9-Tier Enterprise Architecture\n',
        'Auto-synchronized by cli/sync_urls.py (Namespaced & Root Handled)\n',
        '"""\n',
        'from django.contrib import admin\n',
        'from django.urls import path, include\n',
        'from django.views.generic import RedirectView\n\n',
        'urlpatterns = [\n',
        "    # Automatic Root redirect to Superuser Guest Home page\n",
        "    path('', RedirectView.as_view(url='/api/v1/users/superusers/guest-home/', permanent=False)),\n",
        "    # Django Admin Panel\n",
        "    path('admin/', admin.site.urls),\n",
        "    # --- Tier-3: Group App API Routers ---\n"
    ]

    for g_name in sorted(all_group_names):
        lines.append(f"    path('api/v1/{g_name}/', include(('apps.{g_name}.urls', '{g_name}'))),\n")
        if g_name == 'users':
            lines.append(f"    path('api/v1/users/superusers/', include(('apps.users.superusers.urls', 'superusers'))),\n")

    lines.append(']\n')
    TIER1_CORE_URLS.write_text("".join(lines), encoding='utf-8')
    print(f"\n🚀 [Tier-1 Core Gateway] core/urls.py successfully updated.")

def run_9tier_url_sync():
    print("\n" + "=" * 70)
    print("   HYBRID MARKETPLACE — 9-TIER cli/sync_urls.py (Automated Dashboard Fix)   ")
    print("=" * 70)

    if not TIER2_APPS.exists():
        print(f"❌ Error: Tier-2 directory '{TIER2_APPS}' not found.")
        return

    group_apps = sorted([d.name for d in TIER2_APPS.iterdir() if d.is_dir() and not d.name.startswith('_')])

    print("1. Sync specific Tier-3 Group App(s) by number")
    print("2. Sync ENTIRE project globally (Tier-7 Views -> Tier-4 -> Tier-3 -> Tier-1 Core)")
    mode = input("\n👉 Select mode (1 or 2): ").strip()

    if mode == '1':
        print("\n📂 [Tier-3] Available Group Apps:")
        for idx, g in enumerate(group_apps, 1):
            print(f"  [{idx}] 📂 {g}")
        g_input = input("\n👉 Enter Group App number(s) (e.g., 1 or 1,3): ").strip()
        indices = [int(x.strip()) - 1 for x in g_input.split(',') if x.strip().isdigit()]
        chosen_groups = [group_apps[i] for i in indices if 0 <= i < len(group_apps)]
    else:
        chosen_groups = group_apps

    if not chosen_groups:
        print("❌ No Group Apps selected.")
        return

    print(f"\n🔍 Scanning Tier-7 views and building Tier-4 -> Tier-3 -> Tier-1 routers...\n")
    audit_records = []

    for group in chosen_groups:
        group_path = TIER2_APPS / group
        sub_modules = []
        for sub_dir in sorted(group_path.iterdir()):
            if sub_dir.is_dir() and sub_dir.name not in TIER5_EXCLUDED_DIRS and not sub_dir.name.startswith('_'):
                sub_info = sync_subapp_urls(group, sub_dir)
                sub_modules.append(sub_info)

        if sub_modules:
            sync_group_urls(group, sub_modules)
            audit_records.append({'group': group, 'sub_apps': sub_modules})

    sync_tier1_core_urls(group_apps)

    TIER9_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    URL_AUDIT_LOG.write_text(json.dumps({
        'timestamp': datetime.now().isoformat(),
        'flow': 'Tier-7/8 Views -> Tier-4 Subapps -> Tier-3 Groups -> Tier-1 Core (Automated Dashboard Fix)',
        'synced_groups': audit_records
    }, indent=4), encoding='utf-8')
    print(f"📁 [Tier-9 Telemetry] URL audit saved at: {URL_AUDIT_LOG.relative_to(TIER1_ROOT)}")

    print("\n" + "=" * 70)
    print("✨ 9-TIER URL SYNCHRONIZATION COMPLETE WITH AUTOMATED DASHBOARD FIX!")
    print("=" * 70 + "\n")

if __name__ == '__main__':
    run_9tier_url_sync()