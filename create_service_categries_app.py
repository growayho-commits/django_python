import os

sub_app_path = "/workspaces/django_python/apps/professional_network/service_categries"
sub_app = "service_categries"

# 1. Sub-App Root Files
os.makedirs(sub_app_path, exist_ok=True)
root_files = [
    "__init__.py", "admin.py", "apps.py", "choices.py", 
    "constants.py", "conf.py", "urls.py"
]
for file_name in root_files:
    open(os.path.join(sub_app_path, file_name), "a").close()
    
# 2. Sub-App Folders & Specific Standard Files
folders_with_files = {
    "dtos": f"{sub_app}_dtos.py",
    "exceptions": f"{sub_app}_exceptions.py",
    "filters": f"{sub_app}_filters.py",
    "forms": f"{sub_app}_forms.py",
    "interfaces": None,
    "listeners": None,
    "managers": f"{sub_app}_managers.py",
    "middleware": None,
    "migrations": "0001_initial.py",
    "models": f"{sub_app}_model.py",
    "permissions": f"{sub_app}_permissions.py",
    "presenters": None,
    "selectors": f"{sub_app}_selectors.py",
    "serializers": f"{sub_app}_serializer.py",
    "services": f"{sub_app}_service.py",
    "signals": f"{sub_app}_signals.py",
    "tasks": f"{sub_app}_tasks.py",
    "tests": f"test_{sub_app}.py",
    "utils": f"{sub_app}_utils.py",
    "validators": f"{sub_app}_validators.py",
    "views": f"{sub_app}_views.py",
}

for folder_name, file_name in folders_with_files.items():
    folder_path = os.path.join(sub_app_path, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    open(os.path.join(folder_path, "__init__.py"), "a").close()
    if file_name:
        open(os.path.join(folder_path, file_name), "a").close()
        
# 3. Templates Nested Structure
templates_path = os.path.join(sub_app_path, "templates", sub_app)
os.makedirs(templates_path, exist_ok=True)
open(os.path.join(sub_app_path, "templates", "__init__.py"), "a").close()
open(os.path.join(templates_path, f"{sub_app}_dashboard.html"), "a").close()
open(os.path.join(templates_path, f"{sub_app}_manage.html"), "a").close()

print(f"✨ Successfully created Enterprise DDD structure for Sub-App: [{sub_app}] inside professional_network!")