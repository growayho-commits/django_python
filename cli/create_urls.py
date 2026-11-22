import os
import ast
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "apps"
CORE_URLS_FILE = BASE_DIR / "core" / "urls.py"


def extract_views_via_ast(file_path: pathlib.Path) -> list[dict]:
    """Extracts function-based views, class-based views, and viewsets from a python file using AST."""
    views_found = []
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))

        for node in tree.body:
            # Check for Function-Based Views (FBVs)
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                args = [arg.arg for arg in node.args.args]
                if args and args[0] == "request":
                    param_name = next((a for a in args[1:] if a in ("pk", "id", "slug")), None)
                    views_found.append({
                        "name": node.name,
                        "type": "fbv",
                        "param": param_name,
                    })
            # Check for Class-Based Views (CBVs) and ViewSets
            elif isinstance(node, ast.ClassDef):
                base_names = []
                for base in node.bases:
                    if isinstance(base, ast.Name):
                        base_names.append(base.id)
                    elif isinstance(base, ast.Attribute):
                        base_names.append(base.attr)

                combined_bases = "".join(base_names)
                if any("View" in b or "ViewSet" in b for b in base_names):
                    is_viewset = "ViewSet" in combined_bases or "ViewSet" in node.name
                    needs_pk = any(
                        kw in combined_bases
                        for kw in ("Detail", "Update", "Delete", "Retrieve", "Destroy")
                    )
                    views_found.append({
                        "name": node.name,
                        "type": "viewset" if is_viewset else "cbv",
                        "param": "pk" if needs_pk else None,
                    })
    except Exception as e:
        print(f"[Error] {file_path}: {e}")

    return views_found


def to_url_slug(name: str, app_name: str) -> str:
    """Converts a view name into a URL-friendly slug."""
    slug = name
    for suffix in ("View", "views", "view", "ViewSet"):
        if slug.endswith(suffix) and len(slug) > len(suffix):
            slug = slug[: -len(suffix)]
    snake = "".join(["_" + c.lower() if c.isupper() else c for c in slug]).lstrip("_")
    snake = snake.replace(f"{app_name}_", "").strip("_")
    
    # Custom rule: if 'member_dashboard' or 'member-dashboard' appears inside the 'members' app, map it to 'dashboard'
    if app_name == "members" and "dashboard" in snake.lower():
        return "dashboard"
        
    return snake.replace("_", "-")


def build_sub_app_urls(sub_app_dir: pathlib.Path, domain_name: str) -> bool:
    """Builds urls.py for individual sub-apps by scanning their views directory."""
    views_dir = sub_app_dir / "views"
    if not views_dir.is_dir():
        return False

    sub_app_name = sub_app_dir.name
    imports = []
    patterns = []

    for py_file in sorted(views_dir.glob("*.py")):
        if py_file.name == "__init__.py":
            continue

        extracted = extract_views_via_ast(py_file)
        if not extracted:
            continue

        view_names = [v["name"] for v in extracted]
        imports.append(f"from .views.{py_file.stem} import {', '.join(view_names)}")

        for v in extracted:
            v_name = v["name"]
            slug = to_url_slug(v_name, sub_app_name)
            
            if v["type"] == "viewset":
                callable_expr = f"{v_name}.as_view({{'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}})"
                route = f"{slug}/"
            elif v["type"] == "cbv":
                route = f"{slug}/"
                callable_expr = f"{v_name}.as_view()"
            else:
                route = f"{slug}/<int:pk>/" if v["param"] in ("pk", "id") else (
                    f"{slug}/<slug:slug>/" if v["param"] == "slug" else f"{slug}/"
                )
                callable_expr = v_name

            route_name = v_name if v_name == "logout_view" else (to_url_slug(v_name, sub_app_name).replace("-", "_") or v_name.lower())
            patterns.append(f"    path('{route}', {callable_expr}, name='{route_name}'),")

    if not patterns:
        return False

    content = (
        "from django.urls import path\n"
        + "\n".join(imports)
        + f"\n\napp_name = '{sub_app_name}'\n\n"
        + "urlpatterns = [\n"
        + "\n".join(patterns)
        + "\n]\n"
    )

    urls_file = sub_app_dir / "urls.py"
    urls_file.write_text(content, encoding="utf-8")
    print(f"  [Sub-App] {domain_name}/{sub_app_name}/urls.py ({len(patterns)} paths) - Updated")
    return True


def build_domain_urls(domain_dir: pathlib.Path, active_sub_apps: list[str]) -> bool:
    """Builds the group-level domain urls.py including sub-apps and direct domain views."""
    domain_name = domain_dir.name
    patterns = [
        f"    path('{sub}/', include('apps.{domain_name}.{sub}.urls')),"
        for sub in sorted(active_sub_apps)
    ]

    domain_views_dir = domain_dir / "views"
    extra_imports = []
    if domain_views_dir.is_dir():
        for py_file in sorted(domain_views_dir.glob("*.py")):
            if py_file.name == "__init__.py":
                continue
            try:
                extracted = extract_views_via_ast(py_file)
                if extracted:
                    view_names = [v["name"] for v in extracted]
                    extra_imports.append(f"from .views.{py_file.stem} import {', '.join(view_names)}")

                    for v in extracted:
                        v_name = v["name"]
                        slug = to_url_slug(v_name, domain_name)
                        
                        if v["type"] == "viewset":
                            expr = f"{v_name}.as_view({{'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}})"
                            route = f"{slug}/"
                        elif v["type"] == "cbv":
                            route = f"{slug}/"
                            expr = f"{v_name}.as_view()"
                        else:
                            route = f"{slug}/<int:pk>/" if v["param"] in ("pk", "id") else (
                                f"{slug}/<slug:slug>/" if v["param"] == "slug" else f"{slug}/"
                            )
                            expr = v_name
                            
                        route_name = v_name if v_name == "logout_view" else (slug.replace('-', '_') or v_name.lower())
                        patterns.append(f"    path('{route}', {expr}, name='{route_name}'),")
            except Exception as e:
                print(f"[Warning] Error reading file {py_file}: {e}")

    import_block = "\n".join(extra_imports) + ("\n" if extra_imports else "")
    content = (
        "from django.urls import path, include\n"
        + import_block
        + f"\napp_name = '{domain_name}'\n\n"
        + "urlpatterns = [\n"
        + "\n".join(patterns)
        + "\n]\n"
    )

    domain_urls_file = domain_dir / "urls.py"
    domain_urls_file.write_text(content, encoding="utf-8")
    print(f"[Domain]  apps/{domain_name}/urls.py (Group app) - Updated")
    return True


def find_home_view():
    """Searches for a Home or Index view across apps to map as the root URL."""
    for root, dirs, files in os.walk(APPS_DIR):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = pathlib.Path(root) / file
                try:
                    source = file_path.read_text(encoding="utf-8")
                    tree = ast.parse(source, filename=str(file_path))
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef) and ("Home" in node.name or "Index" in node.name):
                            relative = file_path.relative_to(BASE_DIR)
                            module_path = str(relative.with_suffix('')).replace(os.sep, '.')
                            return module_path, node.name
                except Exception:
                    pass
    return None, None


def update_core_urls(active_domains: list[str]):
    """Updates the main project core/urls.py file with domain routers and root mapping."""
    if not active_domains:
        return

    CORE_URLS_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    domain_lines = []
    for dom in sorted(active_domains):
        domain_lines.append(f"    path('api/v1/{dom}/', include(('apps.{dom}.urls', '{dom}'))),")
        if dom == 'users':
            domain_lines.append("    path('api/v1/users/superusers/', include(('apps.users.superusers.urls', 'superusers'))),")

    home_module, home_class = find_home_view()
    
    if home_module and home_class:
        import_stmt = f"from {home_module} import {home_class}"
        root_path = f"    path('', {home_class}.as_view(), name='guest_home'),"
        msg = f"GuestHomeView ({home_class}) mapped successfully as root page"
    else:
        import_stmt = "from django.views.generic import RedirectView"
        root_path = "    path('', RedirectView.as_view(url='/api/v1/users/superusers/guest-home/', permanent=False)),"
        msg = "Home view not found, redirecting..."

    content = (
        '"""\n'
        'Tier-1 Core Main URL Configuration — 9-Tier Enterprise Architecture\n'
        'Auto-synchronized by cli/create_urls.py (Namespaced & Root Handled)\n'
        '"""\n'
        "from django.contrib import admin\n"
        "from django.urls import path, include\n"
        f"{import_stmt}\n\n"
        "urlpatterns = [\n"
        f"    # Direct Root mapping to Guest Home page view\n"
        f"{root_path}\n"
        "    # Django Admin Panel\n"
        "    path('admin/', admin.site.urls),\n"
        "    # --- Tier-3: Group App API Routers ---\n"
        + "\n".join(domain_lines)
        + "\n]\n"
    )
    CORE_URLS_FILE.write_text(content, encoding="utf-8")
    print(f"[Core]    core/urls.py updated ({msg}) [api/v1/ connected]")


def run_all():
    """Main execution entry point to discover apps and regenerate all URL routes."""
    if not APPS_DIR.is_dir():
        print(f"'apps' folder not found: {APPS_DIR}")
        return

    print("--- Starting 9-Tier URL Generation ---")
    
    # Remove existing urls.py files to ensure clean regeneration
    for root, dirs, files in os.walk(APPS_DIR):
        if "urls.py" in files:
            old_url_path = pathlib.Path(root) / "urls.py"
            try:
                old_url_path.unlink()
            except Exception as e:
                print(f"Error deleting {old_url_path}: {e}")

    active_domains = []

    for domain_dir in sorted(APPS_DIR.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith("__"):
            continue

        active_sub_apps = []
        for sub_dir in sorted(domain_dir.iterdir()):
            if not sub_dir.is_dir() or sub_dir.name.startswith("__"):
                continue
            if build_sub_app_urls(sub_dir, domain_dir.name):
                active_sub_apps.append(sub_dir.name)

        if (domain_dir / "urls.py").exists() or active_sub_apps:
            build_domain_urls(domain_dir, active_sub_apps)
            active_domains.append(domain_dir.name)

    update_core_urls(active_domains)
    print("\n--- All URL configuration files updated successfully ---")


if __name__ == "__main__":
    run_all()