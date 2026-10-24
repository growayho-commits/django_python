import os
import sys

def get_detailed_file_content(file_path):
    """பைதான் கோப்பிற்குள் உள்ள கிளாஸ்கள் மற்றும் ஃபங்ஷன்களைப் படித்து வழங்கும்"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return ["      ↳ (கோப்பை படிக்க முடியவில்லை)"]

    details = []
    classes = []
    functions = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('class '):
            class_name = stripped.split('(')[0].replace('class ', '').strip(':')
            classes.append(class_name)
        elif stripped.startswith('def '):
            func_name = stripped.split('(')[0].replace('def ', '').strip()
            if not func_name.startswith('_'):
                functions.append(func_name)

    if classes:
        details.append(f"      ↳ [Classes]: {', '.join(classes)}")
    if functions:
        details.append(f"      ↳ [Functions]: {', '.join(functions)}")
    
    details.append(f"      ↳ [Total Lines]: {len(lines)} வரிகள்")
    return details

def print_tree(directory, prefix="", exclude_dirs=None, file_handle=None):
    if exclude_dirs is None:
        exclude_dirs = {'venv', '__pycache__', '.git', 'staticfiles', 'media', 'node_modules'}
    
    try:
        entries = sorted(os.listdir(directory))
    except PermissionError:
        return

    # கோப்புகளையும் ஃபோல்டர்களையும் தரம் பிரித்தல்
    entries = [e for e in entries if e not in exclude_dirs and not e.endswith('_summary.txt') and e != 'create_summary.py']
    
    pointers = [rapp := '├── '] * (len(entries) - 1) + ['└── '] if entries else []
    
    for pointer, entry in zip(pointers, entries):
        path = os.path.join(directory, entry)
        file_handle.write(f"{prefix}{pointer}{entry}\n")
        if os.path.isdir(path):
            extension = '│   ' if pointer == '├── ' else '    '
            print_tree(path, prefix=prefix + extension, exclude_dirs=exclude_dirs, file_handle=file_handle)

def generate_tree_and_details(target_path):
    if target_path == '.' or target_path == '':
        output_filename = "code_summary.txt"
        target_path = '.'
    else:
        safe_name = target_path.replace('/', '_').replace('\\', '_').strip('./')
        output_filename = f"{safe_name}_summary.txt"
    
    EXCLUDE_DIRS = {'venv', '__pycache__', '.git', 'staticfiles', 'media', 'node_modules'}
    
    if not os.path.exists(target_path):
        print(f"மன்னிக்கவும், '{target_path}' என்ற பாதை கிடைக்கவில்லை.")
        return

    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write("=" * 65 + "\n")
        f.write(f"   TARGET PATH: {target_path} (Proper Tree View & Details)\n")
        f.write("=" * 65 + "\n\n")
        
        # 1. சரியான மர அமைப்பு (Proper Tree Structure)
        f.write("【 1. TREE VIEW STRUCTURE 】\n")
        f.write("-" * 40 + "\n")
        f.write(f"{target_path}/\n")
        print_tree(target_path, prefix="", exclude_dirs=EXCLUDE_DIRS, file_handle=f)
        
        f.write("\n" + "=" * 65 + "\n\n")
        
        # 2. விரிவான விளக்கங்கள் (Detailed Descriptions)
        f.write("【 2. DETAILED FILE DESCRIPTIONS 】\n")
        f.write("-" * 40 + "\n")
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in sorted(files):
                if file.endswith('.pyc') or file == 'create_summary.py' or file.endswith('_summary.txt'):
                    continue
                
                file_path = os.path.join(root, file)
                f.write(f"📄 File: {file_path}\n")
                
                if file.endswith('.py'):
                    file_details = get_detailed_file_content(file_path)
                    for detail in file_details:
                        f.write(f"{detail}\n")
                else:
                    f.write(f"      ↳ இதர கோப்பு அல்லது டெம்ப்ளேட்\n")
                f.write("\n")
                
    print(f"வெற்றி! மாஸ்டர் ஸ்டைல் Tree View மற்றும் Details இரண்டும் '{output_filename}' ஃபைலில் சேமிக்கப்பட்டுவிட்டது.")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    generate_tree_and_details(target)