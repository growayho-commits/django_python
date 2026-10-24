import os

def generate_tree(dir_path, prefix=""):
    lines = []
    try:
        entries = sorted(os.listdir(dir_path))
    except Exception as e:
        return [f"Error accessing {dir_path}: {e}"]
    
    entries = [e for e in entries if e not in [".git", "__pycache__"]]
    
    for i, entry in enumerate(entries):
        path = os.path.join(dir_path, entry)
        is_last = (i == len(entries) - 1)
        connector = "└── " if is_last else "├── "
        lines.append(f"{prefix}{connector}{entry}")
        
        if os.path.isdir(path):
            extension = "    " if is_last else "│   "
            lines.extend(generate_tree(path, prefix + extension))
            
    return lines

target_dir = "/workspaces/django_python/apps/professional_network"
output_file = "/workspaces/django_python/professional_network_tree.txt"

if os.path.exists(target_dir):
    tree_lines = [target_dir] + generate_tree(target_dir)
    tree_text = "\n".join(tree_lines)
    with open(output_file, "w") as f:
        f.write(tree_text)
    print(f"✨ Successfully generated tree view and saved to {output_file}")
else:
    print(f"❌ Error: Directory not found at {target_dir}")
