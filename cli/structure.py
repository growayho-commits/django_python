#


import os

def generate_tree_view(start_path):
    """கொடுக்கப்பட்ட பாதையின் மர அமைப்பை (Tree View) உருவாக்கும்"""
    tree_lines = [f"* **{os.path.basename(os.path.abspath(start_path))}/**"]
    
    for root, dirs, files in os.walk(start_path):
        # தேவையற்ற ஃபோல்டர்களைத் தவிர்த்தல்
        dirs[:] = [d for d in dirs if d not in ('__pycache__', '.git', 'migrations', 'venv', '.venv', 'cli', 'docs', 'logs', 'backups')]
        
        level = root.replace(start_path, '').count(os.sep)
        indent = '    ' * (level + 1)
        
        if root != start_path:
            sub_indent = '    ' * level
            tree_lines.append(f"{sub_indent}* **{os.path.basename(root)}/**")
            
        for f in sorted(files):
            if f.endswith(('.py', '.html', '.md')):
                file_path = os.path.join(root, f)
                try:
                    with open(file_path, 'r', encoding='utf-8') as fp:
                        line_count = sum(1 for _ in fp)
                except Exception:
                    line_count = 0
                tree_lines.append(f"{indent}* {f} [Lines: {line_count}]")
                
    return "\n".join(tree_lines)

def main():
    print("=" * 65)
    print("   HYBRID MARKETPLACE - STRUCTURE VIEWER (structure.py)")
    print("=" * 65)
    
    target_path = "."
    output_filename = "project_structure_view.txt"
    
    print(f"\n🔍 Scanning project structure from '{os.path.abspath(target_path)}'...")
    
    try:
        tree_output = generate_tree_view(target_path)
        
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write("=== HYBRID MARKETPLACE PROJECT STRUCTURE ===\n\n")
            f.write(tree_output)
            
        print(f"\n✅ Success! Structure successfully generated and saved to: {output_filename}")
    except Exception as e:
        print(f"\n❌ Error generating structure: {e}")

if __name__ == "__main__":
    main()