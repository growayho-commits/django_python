import os

APPS_DIR = "/workspaces/django_python/apps"

ROOT_FILES = [
    "__init__.py", 
    "admin.py", 
    "apps.py", 
    "choices.py",
    "constants.py", 
    "conf.py", 
    "urls.py"
]

DDD_FOLDERS = [
    "dtos",
    "exceptions",
    "filters",
    "forms",
    "interfaces",
    "listeners",
    "managers",
    "middleware",
    "migrations",
    "models",
    "permissions",
    "presenters",
    "selectors",
    "serializers",
    "services",
    "signals",
    "tasks",
    "tests",
    "utils",
    "validators",
    "views"
]

def restructure_and_preserve():
    if not os.path.exists(APPS_DIR):
        print(f"❌ Error: Apps directory not found at {APPS_DIR}")
        return

    print("🚀 Scanning apps, enforcing Enterprise DDD structure, and preserving all .py files...")

    for domain in os.listdir(APPS_DIR):
        domain_path = os.path.join(APPS_DIR, domain)
        if not os.path.isdir(domain_path) or domain.startswith("__") or domain.startswith("."):
            continue

        os.makedirs(domain_path, exist_ok=True)
        open(os.path.join(domain_path, "__init__.py"), "a").close()
        open(os.path.join(domain_path, "urls.py"), "a").close()

        for sub_app in os.listdir(domain_path):
            sub_app_path = os.path.join(domain_path, sub_app)
            if not os.path.isdir(sub_app_path) or sub_app.startswith("__") or sub_app.startswith("."):
                continue

            print(f"📁 Processing Sub-App: [{domain} -> {sub_app}]")

            for file_name in ROOT_FILES:
                file_path = os.path.join(sub_app_path, file_name)
                if not os.path.exists(file_path):
                    open(file_path, "a").close()

            for folder_name in DDD_FOLDERS:
                folder_path = os.path.join(sub_app_path, folder_name)
                os.makedirs(folder_path, exist_ok=True)
                init_file = os.path.join(folder_path, "__init__.py")
                if not os.path.exists(init_file):
                    open(init_file, "a").close()

            templates_path = os.path.join(sub_app_path, "templates", sub_app)
            os.makedirs(templates_path, exist_ok=True)
            templates_init = os.path.join(sub_app_path, "templates", "__init__.py")
            if not os.path.exists(templates_init):
                open(templates_init, "a").close()

    print("\n✨ Success! Structure updated successfully to Enterprise DDD standards, and all existing .py files & code remain 100% safe and untouched!")

if __name__ == "__main__":
    restructure_and_preserve()