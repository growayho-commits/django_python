import os
import ast
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "apps"
CORE_URLS_FILE = BASE_DIR / "core" / "urls.py"


def extract_views_via_ast(file_path: pathlib.Path) -> list[dict]:
    views_found = []
    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(file_path))

        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                args = [arg.arg for arg in node.args.args]
                if args and args[0] == "request":
                    param_name = next((a for a in args[1:] if a in ("pk", "id", "slug")), None)
                    views_found.append({
                        "name": node.name,
                        "type": "fbv",
                        "param": param_name,
                    })
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
        print(f"[பிழை] {file_path}: {e}")

    return views_found


def to_url_slug(name: str, sub_app: str) -> str:
    slug = name
    for suffix in ("View", "views", "view", "ViewSet", "ViewSet"):
        if slug.endswith(suffix) and len(slug) > len(suffix):
            slug = slug[: -len(suffix)]
    snake = "".join(["_" + c.lower() if c.isupper() else c for c in slug]).lstrip("_")
    snake = snake.replace(f"{sub_app}_", "").strip("_")
    return snake.replace("_", "-")


def build_sub_app_urls(sub_app_dir: pathlib.Path, domain_name: str) -> bool:
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
            else:
                route = f"{slug}/<int:pk>/" if v["param"] in ("pk", "id") else (
                    f"{slug}/<slug:slug>/" if v["param"] == "slug" else f"{slug}/"
                )
                callable_expr = f"{v_name}.as_view()" if v["type"] == "cbv" else v_name

            route_name = to_url_slug(v_name, sub_app_name).replace("-", "_") or v_name.lower()
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
                for v in extract_views_via_ast(py_file):
                    v_name = v["name"]
                    extra_imports.append(f"from .views.{py_file.stem} import {v_name}")
                    slug = to_url_slug(v_name, domain_name)
                    
                    if v["type"] == "viewset":
                        expr = f"{v_name}.as_view({{'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}})"
                    elif v["type"] == "cbv":
                        expr = f"{v_name}.as_view()"
                    else:
                        expr = v_name
                        
                    patterns.append(f"    path('{slug}/', {expr}, name='{slug.replace('-', '_')}'),")
            except Exception as e:
                print(f"[எச்சரிக்கை] {py_file} கோப்பைப் படிப்பதில் பிழை: {e}")

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
    print(f"[Domain]  apps/{domain_name}/urls.py ({len(active_sub_apps)} sub-apps) - Updated")
    return True


def find_home_view():
    """புராஜெக்ட்டில் உள்ள ஹோம் வியூவை (GuestHomeView போன்றவற்றை) தானாகத் தேடுதல்"""
    for root, dirs, files in os.walk(APPS_DIR):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                file_path = pathlib.Path(root) / file
                try:
                    source = file_path.read_text(encoding="utf-8")
                    tree = ast.parse(source, filename=str(file_path))
                    for node in tree.body:
                        if isinstance(node, ast.ClassDef) and ("Home" in node.name or "Index" in node.name):
                            # மாட்யூல் பாதையைக் கண்டறிதல் (எ.கா: apps.users.superusers.views.superuser_views)
                            relative = file_path.relative_to(BASE_DIR)
                            module_path = str(relative.with_suffix('')).replace(os.sep, '.')
                            return module_path, node.name
                except Exception:
                    pass
    return None, None


def update_core_urls(active_domains: list[str]):
    if not active_domains:
        return

    CORE_URLS_FILE.parent.mkdir(parents=True, exist_ok=True)
    domain_lines = [
        f"    path('{dom}/', include('apps.{dom}.urls')),"
        for dom in sorted(active_domains)
    ]

    home_module, home_class = find_home_view()
    
    if home_module and home_class:
        import_stmt = f"from {home_module} import {home_class}"
        root_path = f"    path('', {home_class}.as_view(), name='guest_home'),"
        msg = f"GuestHomeView ({home_class}) ரூட் பக்கமாக இணைக்கப்பட்டது"
    else:
        import_stmt = "from django.views.generic import RedirectView"
        root_path = "    path('', RedirectView.as_view(url='/admin/', permanent=False)),"
        msg = "ஹோம் வியூ கிடைக்கவில்லை, Admin-க்கு Redirect செய்யப்படுகிறது"

    content = (
        "from django.contrib import admin\n"
        "from django.urls import path, include\n"
        f"{import_stmt}\n\n"
        "urlpatterns = [\n"
        f"{root_path}\n"
        "    path('admin/', admin.site.urls),\n"
        + "\n".join(domain_lines)
        + "\n]\n"
    )
    CORE_URLS_FILE.write_text(content, encoding="utf-8")
    print(f"[Core]    core/urls.py புதுப்பிக்கப்பட்டது ({msg})")


def run_all():
    if not APPS_DIR.is_dir():
        print(f"'apps' ஃபோல்டர் காணப்படவில்லை: {APPS_DIR}")
        return

    print("--- 3-அடுக்கு URL உருவாக்கம் தொடங்குகிறது ---")
    
    for root, dirs, files in os.walk(APPS_DIR):
        if "urls.py" in files:
            old_url_path = pathlib.Path(root) / "urls.py"
            try:
                old_url_path.unlink()
            except Exception as e:
                print(f"நீக்குவதில் சிக்கல் {old_url_path}: {e}")

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

        if build_domain_urls(domain_dir, active_sub_apps):
            active_domains.append(domain_dir.name)

    update_core_urls(active_domains)
    print("\n--- அனைத்து URL கோப்புகளும் வெற்றிகரமாகப் புதுப்பிக்கப்பட்டன ---")


if __name__ == "__main__":
    run_all()