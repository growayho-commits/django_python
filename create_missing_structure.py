import os

def create_missing_folders_and_files():
    required_folders = [
        'dtos', 'exceptions', 'filters', 'forms', 'managers', 
        'migrations', 'models', 'permissions', 'selectors', 
        'serializers', 'services', 'signals', 'tasks', 
        'templates', 'tests', 'utils', 'validators', 'views'
    ]
    
    apps_dir = 'apps'
    if not os.path.exists(apps_dir):
        print("பிழை: 'apps' ஃபோல்டர் கிடைக்கவில்லை!")
        return

    for group_name in os.listdir(apps_dir):
        group_path = os.path.join(apps_dir, group_name)
        if not os.path.isdir(group_path):
            continue
            
        for app_name in os.listdir(group_path):
            app_path = os.path.join(group_path, app_name)
            if not os.path.isdir(app_path):
                continue
                
            print(f"Checking app: {group_name}/{app_name}")
            
            for folder in required_folders:
                folder_path = os.path.join(app_path, folder)
                os.makedirs(folder_path, exist_ok=True)
                
                init_file = os.path.join(folder_path, '__init__.py')
                if not os.path.exists(init_file):
                    with open(init_file, 'w', encoding='utf-8') as f:
                        f.write("")
                        
                if folder == 'templates':
                    sub_template_dir = os.path.join(folder_path, app_name)
                    os.makedirs(sub_template_dir, exist_ok=True)

    print("\n வெற்றி! அனைத்து ஆப்புகளிலும் விடுபட்ட போல்டர்கள் மற்றும் __init__.py சேர்க்கப்பட்டுவிட்டன!")

if __name__ == "__main__":
    create_missing_folders_and_files()
