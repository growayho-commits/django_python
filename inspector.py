import os
import re
import subprocess
from pathlib import Path

def count_file_lines(file_path):
    """Utility to count lines in a python file for statistics"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def extract_url_endpoints(file_path):
    """Extracts url patterns from urls.py or urls folder"""
    endpoints = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = re.findall(r"(path|re_path)\s*\(\s*['\"]([^'\"]*)['\"]", content)
            for m in matches:
                endpoints.append(m[1])
    except Exception:
        pass
    return endpoints

def extract_django_models(file_path):
    """Extracts database model class names from models py file or folder"""
    models = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            matches = re.findall(r"class\s+([A-Za-z0-9_]+)\s*\(\s*.*Model.*\s*\):", content)
            models.extend(matches)
    except Exception:
        pass
    return models

def extract_app_dependencies(file_path):
    """Extracts import statements to map cross-app workflows/dependencies"""
    dependencies = set()
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line.startswith(('from', 'import')) and 'apps.' in line:
                    matches = re.findall(r"apps\.([A-Za-z0-9_]+)", line)
                    for m in matches:
                        dependencies.add(m)
    except Exception:
        pass
    return list(dependencies)

def get_git_status():
    """Gets modified or untracked files from Git"""
    git_files = {"modified": [], "untracked": []}
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if len(line) > 3:
                status_code = line[:2].strip()
                file_path = line[3:].strip()
                if status_code in ['M', 'MM']:
                    git_files["modified"].append(file_path)
                elif status_code == '??':
                    git_files["untracked"].append(file_path)
    except Exception:
        pass
    return git_files

def generate_mermaid_flowchart(workflow_data, model_data):
    """Generates a Mermaid.js Architecture Flow Chart syntax for the report"""
    mermaid_lines = ["```mermaid", "graph TD"]
    mermaid_lines.append("    classDef appStyle fill:#f9f,stroke:#333,stroke-width:2px;")
    mermaid_lines.append("    classDef modelStyle fill:#bbf,stroke:#333,stroke-width:1px;")
    
    added_links = set()
    for path, deps in workflow_data.items():
        parts = Path(path).parts
        source_app = parts[1] if len(parts) > 1 and parts[0] == 'apps' else parts[0]
        for dep in deps:
            if source_app != dep:
                link = f"    {source_app} -->|depends on| {dep}"
                if link not in added_links:
                    added_links.add(link)
                    mermaid_lines.append(link)
                    
    for path, mods in model_data.items():
        parts = Path(path).parts
        app_name = parts[1] if len(parts) > 1 and parts[0] == 'apps' else parts[0]
        for mod in mods:
            mermaid_lines.append(f"    {app_name} --- {mod}[Model: {mod}]")
            
    mermaid_lines.append("```")
    return "\n".join(mermaid_lines)

def generate_inspection_report(root_dir, search_term="", exact_match=False, view_flags="all", is_markdown=False):
    tree_lines = []
    stats_data = {"total_files": 0, "py_files": 0, "total_lines": 0}
    endpoint_data = {}
    model_data = {}
    workflow_data = {}
    
    root_path = Path(root_dir).resolve()
    search_term = search_term.strip().lower()
    is_full_mode = len(search_term) == 0

    matched_paths = set()
    found_any_match = False

    for current_root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv', 'env', '.idea', '.vscode', 'node_modules']]
        
        rel_path = os.path.relpath(current_root, root_path)
        dir_name = os.path.basename(current_root).lower()
        
        if is_full_mode:
            include_dir = True
            matching_files = [f for f in files if not f.endswith(('.pyc', '.pyo'))]
        else:
            if exact_match:
                dir_matches = (search_term == dir_name or search_term in [p.lower() for p in Path(rel_path).parts])
                matching_files = [f for f in files if not f.endswith(('.pyc', '.pyo')) and (dir_matches or search_term == f.lower())]
            else:
                dir_matches = (search_term in dir_name or search_term in rel_path.lower())
                matching_files = [f for f in files if not f.endswith(('.pyc', '.pyo')) and (dir_matches or search_term in f.lower())]
            
            include_dir = dir_matches or len(matching_files) > 0

        if include_dir:
            found_any_match = True
            depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
            
            if is_markdown:
                indent = "    " * (depth - 1) + "- " if depth > 0 else ""
                original_dir_name = os.path.basename(current_root)
                if depth == 0:
                    tree_lines.append(f"# {original_dir_name}/")
                else:
                    tree_lines.append(f"{indent}**{original_dir_name}/**")
            else:
                indent = "│   " * (depth - 1) + "├── " if depth > 0 else ""
                original_dir_name = os.path.basename(current_root)
                if depth == 0:
                    tree_lines.append(f"{original_dir_name}/")
                else:
                    tree_lines.append(f"{indent}{original_dir_name}/")
                
            for file in files:
                if file.endswith(('.pyc', '.pyo')):
                    continue
                    
                if not is_full_mode and not dir_matches:
                    if exact_match and search_term != file.lower():
                        continue
                    if not exact_match and search_term not in file.lower():
                        continue
                
                stats_data["total_files"] += 1
                full_file_path = os.path.join(current_root, file)
                
                file_display = file
                if file.endswith('.py'):
                    stats_data["py_files"] += 1
                    lines = count_file_lines(full_file_path)
                    stats_data["total_lines"] += lines
                    file_display = f"{file}  [Lines: {lines}]"
                    
                    if file == 'urls.py' or 'urls' in Path(rel_path).parts:
                        endpoints = extract_url_endpoints(full_file_path)
                        if endpoints:
                            endpoint_data.setdefault(rel_path, []).extend(endpoints)
                            
                    if file == 'models.py' or 'models' in Path(rel_path).parts:
                        extracted_models = extract_django_models(full_file_path)
                        if extracted_models:
                            model_data.setdefault(rel_path, []).extend(extracted_models)

                    deps = extract_app_dependencies(full_file_path)
                    if deps:
                        workflow_data.setdefault(rel_path, set()).update(deps)

                if is_markdown:
                    file_indent = "    " * depth + "- "
                    tree_lines.append(f"{file_indent}`{file_display}`")
                else:
                    file_indent = "│   " * depth + "└── "
                    tree_lines.append(f"{file_indent}{file_display}")
                    
                matched_paths.add(full_file_path)

    if not is_full_mode and not found_any_match:
        return generate_inspection_report(root_dir, "", False, view_flags, is_markdown)

    if not view_flags:
        view_flags = "all"

    final_output_parts = []
    
    if is_markdown:
        final_output_parts.append("# 🤖 AI PROJECT CONTEXT & HANDSHAKE REPORT")
        final_output_parts.append(f"> Mode: {'COMPLETE PROJECT' if is_full_mode else search_term} | Views: {view_flags.upper()}\n")
    else:
        final_output_parts.append("==================================================")
        final_output_parts.append(" WORLD-CLASS ULTIMATE DJANGO INSPECTION REPORT")
        final_output_parts.append(f" Mode: {'COMPLETE PROJECT' if is_full_mode else search_term} | Views: {view_flags.upper()}")
        final_output_parts.append("==================================================\n")
    
    # 0. Statistics & Metrics [s]
    if view_flags == 'all' or 's' in view_flags:
        final_output_parts.append("=== 0. PROJECT METRICS & STATISTICS ===")
        final_output_parts.append(f" • Total Files Scanned : {stats_data['total_files']}")
        final_output_parts.append(f" • Python (.py) Files  : {stats_data['py_files']}")
        final_output_parts.append(f" • Total Lines of Code : {stats_data['total_lines']} lines")
        final_output_parts.append("==================================================\n" if not is_markdown else "\n---")

    # 1. Tree View Structure [t]
    if view_flags == 'all' or 't' in view_flags:
        final_output_parts.append("=== 1. TREE VIEW STRUCTURE ===")
        final_output_parts.extend(tree_lines)
    
    # 2. Path View [p]
    if view_flags == 'all' or 'p' in view_flags:
        final_output_parts.append("\n=== 2. FULL PATH VIEWS ===")
        final_output_parts.extend(sorted(list(matched_paths)))

    # 3. URL Endpoints [u]
    if view_flags == 'all' or 'u' in view_flags:
        final_output_parts.append("\n=== 3. URL ENDPOINTS EXTRACTED ===")
        if endpoint_data:
            for path, eps in endpoint_data.items():
                final_output_parts.append(f" • {path} -> {eps}")
        else:
            final_output_parts.append(" • No endpoints found.")

    # 4. Django Models Summary [m]
    if view_flags == 'all' or 'm' in view_flags:
        final_output_parts.append("\n=== 4. DJANGO MODELS SUMMARY (Folder/File) ===")
        if model_data:
            for path, mods in model_data.items():
                final_output_parts.append(f" • {path} -> Models: {mods}")
        else:
            final_output_parts.append(" • No models found.")

    # 5. Workflow & Dependencies [w]
    if view_flags == 'all' or 'w' in view_flags:
        final_output_parts.append("\n=== 5. WORKFLOW & CROSS-APP DEPENDENCY VIEW ===")
        if workflow_data:
            for path, deps in workflow_data.items():
                final_output_parts.append(f" • {path} ──> Depends on Apps: {list(deps)}")
        else:
            final_output_parts.append(" • No cross-app dependencies found.")

    # 6. Flow Chart View [f]
    if view_flags == 'all' or 'f' in view_flags:
        final_output_parts.append("\n=== 6. FLOW CHART / ARCHITECTURE DIAGRAM (Mermaid) ===")
        chart_code = generate_mermaid_flowchart(workflow_data, model_data)
        final_output_parts.append(chart_code)

    # 7. Git Integration Status [g]
    if view_flags == 'all' or 'g' in view_flags:
        final_output_parts.append("\n=== 7. GIT INTEGRATION STATUS ===")
        git_info = get_git_status()
        final_output_parts.append(f" • Modified Files  : {git_info['modified']}")
        final_output_parts.append(f" • Untracked Files : {git_info['untracked']}")

    return "\n".join(final_output_parts)

def update_readme_mermaid(chart_code):
    """Automatically updates or inserts the Mermaid flowchart inside README.md"""
    readme_path = Path("README.md")
    
    if not readme_path.exists():
        # Create a basic README if it doesn't exist
        initial_content = f"# HYBRID MARKETPLACE - Django Project\n\n## Architecture Flow Chart\n\n{chart_code}\n"
        readme_path.write_text(initial_content, encoding="utf-8")
        return

    content = readme_path.read_text(encoding="utf-8", errors="ignore")
    
    # Check if a mermaid block already exists in README.md
    if "```mermaid" in content:
        # Replace existing mermaid block
        pattern = r"```mermaid.*?```"
        new_content = re.sub(pattern, chart_code, content, flags=re.DOTALL)
        readme_path.write_text(new_content, encoding="utf-8")
    else:
        # Append mermaid block at the end of README.md
        appended_content = content + f"\n\n## Architecture Flow Chart\n\n{chart_code}\n"
        readme_path.write_text(appended_content, encoding="utf-8")

def main():
    print("==================================================")
    print("  WORLD-CLASS ULTIMATE DJANGO PROJECT INSPECTOR   ")
    print("==================================================")
    search_term = input("Search term (or press [ENTER] for Full View) -> ").strip()
    
    exact_match = False
    if search_term:
        choice_exact = input("Do you want EXACT MATCH? (y/n): ").strip().lower()
        if choice_exact == 'y':
            exact_match = True

    print("\nAvailable View Flags:")
    print("  [t] Tree View       [p] Path View       [s] Stats")
    print("  [u] URL Endpoints   [m] Models Summary  [w] Workflow")
    print("  [f] Flow Chart      [g] Git Status")
    print("\nTip: Combine letters (e.g., 'tp') or simply press [ENTER] for ALL features.")
    
    view_flags = input("Select options -> ").strip().lower()
    if not view_flags:
        view_flags = "all"

    # 1. Generate normal TXT Report
    txt_content = generate_inspection_report(".", search_term, exact_match, view_flags, is_markdown=False)
    txt_filename = "project_tree_path_view.txt"
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(txt_content)

    # 2. Generate Markdown AI Context Report
    md_content = generate_inspection_report(".", search_term, exact_match, view_flags, is_markdown=True)
    md_filename = "AI_PROJECT_CONTEXT.md"
    with open(md_filename, "w", encoding="utf-8") as f:
        f.write(md_content)

    # 3. Automatically Update README.md with latest Mermaid Flow Chart
    workflow_data = {}
    model_data = {}
    for current_root, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.venv', 'venv', 'env', '.idea', '.vscode', 'node_modules']]
        rel_path = os.path.relpath(current_root, ".")
        for file in files:
            if file.endswith('.py'):
                full_path = os.path.join(current_root, file)
                if file == 'models.py' or 'models' in Path(rel_path).parts:
                    extracted_models = extract_django_models(full_path)
                    if extracted_models:
                        model_data.setdefault(rel_path, []).extend(extracted_models)
                deps = extract_app_dependencies(full_path)
                if deps:
                    workflow_data.setdefault(rel_path, set()).update(deps)

    latest_chart = generate_mermaid_flowchart(workflow_data, model_data)
    update_readme_mermaid(latest_chart)
        
    print("\n==================================================")
    print(f"SUCCESS: All updates completed automatically!")
    print(f" 1. Personal TXT Report : '{txt_filename}'")
    print(f" 2. AI Context File     : '{md_filename}'")
    print(f" 3. README.md Flowchart : Auto-updated successfully!")
    print("==================================================")

if __name__ == "__main__":
    main()