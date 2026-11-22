import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))

APPS_DIR = os.path.join(PROJECT_ROOT, "apps")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
ADMIN_MAP_PATH = os.path.join(DOCS_DIR, "ADMIN_MAP.md")

EXCLUDED_SUB_DIRS = {
    'migrations', 'tests', 'utils', 'validators', 'serializers', 
    'selectors', 'services', 'permissions', 'middleware', 'listeners', 
    'interfaces', 'forms', 'filters', 'exceptions', 'dtos', 'presenters', 
    'signals', 'tasks', 'templates', 'views', '__pycache__'
}

def get_models_from_sub_app(sub_path):
    models_found = []
    models_file_path = os.path.join(sub_path, "models.py")
    models_dir_path = os.path.join(sub_path, "models")
    
    target_files = []
    if os.path.exists(models_file_path):
        target_files.append(models_file_path)
        
    if os.path.exists(models_dir_path) and os.path.isdir(models_dir_path):
        for root, _, files in os.walk(models_dir_path):
            for file in files:
                if file.endswith(".py"):
                    target_files.append(os.path.join(root, file))

    for file_path in target_files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                classes = re.findall(r"class\s+([A-Za-z0-9_]+)\s*\(\s*(?:models\.)?Model\s*\)", content)
                for cls_name in classes:
                    if cls_name not in models_found and cls_name != "Meta":
                        models_found.append(cls_name)
        except Exception:
            pass
            
    return models_found

def sync_and_generate_advanced_admin():
    print("=" * 70)
    print("   HYBRID MARKETPLACE - CLEAN SMART ADMIN SYNC")
    print("=" * 70 + "\n")
    
    if not os.path.exists(APPS_DIR):
        print(f"⚠️ Error: 'apps/' directory not found at path: {APPS_DIR}!")
        return

    print("🗑️ [Step 1] Purging old `admin.py` files...")
    deleted_count = 0
    for root, dirs, files in os.walk(APPS_DIR):
        if "admin.py" in files:
            try:
                os.remove(os.path.join(root, "admin.py"))
                deleted_count += 1
            except Exception:
                pass
    print(f"  ✔️ Purged {deleted_count} old admin files.\n" + "-" * 70)

    print("✨ [Step 2] Scanning models & generating clean `admin.py` files...")
    
    total_sub_apps = 0
    created_admin_files = 0
    total_models_mapped = 0
    
    markdown_map_lines = [
        "# 🛡️ Hybrid Marketplace - Enterprise Admin Registration Map\n",
        "*Auto-generated via clean sync_admin.py*\n"
    ]

    for group_app in sorted(os.listdir(APPS_DIR)):
        group_path = os.path.join(APPS_DIR, group_app)
        if not os.path.isdir(group_path):
            continue
            
        markdown_map_lines.append(f"## 📂 Group App: `{group_app.upper()}`\n")

        for sub_name in sorted(os.listdir(group_path)):
            sub_path = os.path.join(group_path, sub_name)
            
            if not os.path.isdir(sub_path) or sub_name in EXCLUDED_SUB_DIRS:
                continue
                
            total_sub_apps += 1
            sub_admin_path = os.path.join(sub_path, "admin.py")
            
            extracted_models = get_models_from_sub_app(sub_path)
            
            admin_code_lines = [
                "from django.contrib import admin"
            ]
            
            if extracted_models:
                admin_code_lines.append(f"from .models import {', '.join(extracted_models)}")
                admin_code_lines.append("\n# --- Auto-Generated Model Registrations ---")
                for model in extracted_models:
                    admin_code_lines.append(f"@admin.register({model})")
                    admin_code_lines.append(f"class {model}Admin(admin.ModelAdmin):")
                    admin_code_lines.append(f"    list_display = [f.name for f in {model}._meta.fields]")
                    admin_code_lines.append(f"    search_fields = [f.name for f in {model}._meta.fields if f.get_internal_type() in ('CharField', 'TextField')]\n")
                total_models_mapped += len(extracted_models)
            else:
                admin_code_lines.append("\n# Register your models here if needed")

            try:
                with open(sub_admin_path, "w", encoding="utf-8") as f_admin:
                    f_admin.write("\n".join(admin_code_lines))
                created_admin_files += 1
            except Exception as e:
                print(f"  ❌ Error writing {sub_admin_path}: {e}")

            print(f"  🛡️ [Smart Admin] {group_app}/{sub_name} ──> {len(extracted_models)} models mapped.")

            markdown_map_lines.append(f"- **Sub-App**: `{sub_name}`")
            if extracted_models:
                markdown_map_lines.append(f"  - Registered Models: `{', '.join(extracted_models)}`")
            else:
                markdown_map_lines.append(f"  - Registered Models: *None / Utility Sub-app*")
            markdown_map_lines.append("")

        markdown_map_lines.append("")

    print("-" * 70)

    try:
        os.makedirs(DOCS_DIR, exist_ok=True)
        with open(ADMIN_MAP_PATH, "w", encoding="utf-8") as f_doc:
            f_doc.write("\n".join(markdown_map_lines))
        print(f"📝 [Documentation] Smart Admin Map generated at: docs/ADMIN_MAP.md")
    except Exception as e:
        print(f"  ⚠️ Warning generating doc map: {e}")

    print("\n" + "=" * 70)
    print(f"🎉 Admin Sync & Smart Generation Completed Successfully!")
    print(f"   - Sub-Apps Processed: {total_sub_apps}")
    print(f"   - Fresh Admin Files Created: {created_admin_files}")
    print(f"   - Total Models Registered: {total_models_mapped}")
    print("=" * 70)

if __name__ == "__main__":
    sync_and_generate_advanced_admin()