import os

def create_guest_structure():
    base_dir = "apps/users/guests"
    
    # உருவாக்கப்பட வேண்டிய சப்-ஃபோல்டர்கள் (Sub-directories)
    subdirectories = [
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
        "templates/guests",
        "tests",
        "utils",
        "validators",
        "views",
    ]
    
    # சப்-ஆப் ரூட் கோப்பறையில் இருக்க வேண்டிய அடிப்படை பைதான் கோப்புகள்
    root_files = [
        "__init__.py",
        "admin.py",
        "apps.py",
        "choices.py",
        "constants.py",
        "conf.py",
        "urls.py",
    ]
    
    # ஃபோல்டர்களை உருவாக்குதல் மற்றும் __init__.py சேர்ப்பது
    os.makedirs(base_dir, exist_ok=True)
    
    for sub in subdirectories:
        dir_path = os.path.join(base_dir, sub)
        os.makedirs(dir_path, exist_ok=True)
        
        # templates தவிர மற்ற அனைத்து ஃபோல்டர்களிலும் __init__.py கோப்பை உருவாக்குதல்
        if "templates" not in sub:
            init_file = os.path.join(dir_path, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write("# Python Package\n")

    # ரூட் பைதான் கோப்புகளை உருவாக்குதல்
    for file_name in root_files:
        file_path = os.path.join(base_dir, file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f"# {file_name} for guests app\n")

    print("SUCCESS: Guests app folder structure created perfectly!")

if __name__ == "__main__":
    create_guest_structure()