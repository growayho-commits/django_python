import os
import re
import subprocess
from pathlib import Path

try:
    from cli.common import PROJECT_ROOT, README_FILE, SKIP_DIRS, ensure_documents_dir
except ImportError:
    from common import PROJECT_ROOT, README_FILE, SKIP_DIRS, ensure_documents_dir


def count_file_lines(file_path: str) -> int:
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return sum(1 for _ in f)
    except Exception:
        return 0


def extract_url_endpoints(file_path: str) -> list[str]:
    try:
        content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        return [m[1] for m in re.findall(r"(path|re_path)\s*\(\s*['\"]([^'\"]*)['\"]", content)]
    except Exception:
        return []


def extract_django_models(file_path: str) -> list[str]:
    try:
        content = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        return re.findall(r"class\s+([A-Za-z0-9_]+)\s*\(\s*.*Model.*\s*\):", content)
    except Exception:
        return []


def extract_app_dependencies(file_path: str) -> list[str]:
    deps = set()
    try:
        for line in Path(file_path).read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if s.startswith(("from", "import")) and "apps." in s:
                deps.update(re.findall(r"apps\.([A-Za-z0-9_]+)", s))
    except Exception:
        pass
    return list(deps)


def get_git_status() -> dict:
    git_files = {"modified": [], "untracked": []}
    try:
        res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, cwd=PROJECT_ROOT, check=True)
        for line in res.stdout.splitlines():
            if len(line) > 3:
                code, fpath = line[:2].strip(), line[3:].strip()
                if code in ("M", "MM"):
                    git_files["modified"].append(fpath)
                elif code == "??":
                    git_files["untracked"].append(fpath)
    except Exception:
        pass
    return git_files


def generate_mermaid_flowchart(workflow_data: dict, model_data: dict) -> str:
    lines = ["```mermaid", "graph TD"]
    added = set()
    for path, deps in workflow_data.items():
        parts = Path(path).parts
        src = parts[1] if len(parts) > 1 and parts[0] == "apps" else parts[0]
        for dep in deps:
            if src != dep:
                link = f"    {src} -->|depends on| {dep}"
                if link not in added:
                    added.add(link)
                    lines.append(link)
    for path, mods in model_data.items():
        parts = Path(path).parts
        app_name = parts[1] if len(parts) > 1 and parts[0] == "apps" else parts[0]
        for mod in mods:
            lines.append(f"    {app_name} --- {mod}[Model: {mod}]")
    lines.append("```")
    return "\n".join(lines)


def generate_inspection_report(root_path: Path, search_term="", exact_match=False, view_flags="all", is_markdown=False):
    tree_lines, matched_paths = [], set()
    stats = {"total_files": 0, "py_files": 0, "total_lines": 0}
    endpoint_data, model_data, workflow_data = {}, {}, {}
    term = search_term.strip().lower()
    is_full = len(term) == 0

    for current_root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        rel_path = os.path.relpath(current_root, root_path)
        dir_name = os.path.basename(current_root).lower()

        if is_full:
            dir_matches = True
            matching_files = [f for f in files if not f.endswith((".pyc", ".pyo"))]
        else:
            if exact_match:
                dir_matches = term == dir_name or term in [p.lower() for p in Path(rel_path).parts]
                matching_files = [f for f in files if not f.endswith((".pyc", ".pyo")) and (dir_matches or term == f.lower())]
            else:
                dir_matches = term in dir_name or term in rel_path.lower()
                matching_files = [f for f in files if not f.endswith((".pyc", ".pyo")) and (dir_matches or term in f.lower())]

        if not (dir_matches or matching_files):
            continue

        depth = 0 if rel_path == "." else rel_path.count(os.sep) + 1
        orig = os.path.basename(current_root)
        if is_markdown:
            tree_lines.append(f"# {orig}/" if depth == 0 else f"{'    ' * (depth - 1)}- **{orig}/**")
        else:
            tree_lines.append(f"{orig}/" if depth == 0 else f"{'│   ' * (depth - 1)}├── {orig}/")

        for file in sorted(matching_files):
            stats["total_files"] += 1
            full_path = os.path.join(current_root, file)
            display = file
            if file.endswith(".py"):
                stats["py_files"] += 1
                lc = count_file_lines(full_path)
                stats["total_lines"] += lc
                display = f"{file}  [Lines: {lc}]"
                if file == "urls.py" or "urls" in Path(rel_path).parts:
                    eps = extract_url_endpoints(full_path)
                    if eps:
                        endpoint_data.setdefault(rel_path, []).extend(eps)
                if file == "models.py" or "models" in Path(rel_path).parts:
                    mods = extract_django_models(full_path)
                    if mods:
                        model_data.setdefault(rel_path, []).extend(mods)
                deps = extract_app_dependencies(full_path)
                if deps:
                    workflow_data.setdefault(rel_path, set()).update(deps)

            tree_lines.append(f"{'    ' * depth}- `{display}`" if is_markdown else f"{'│   ' * depth}└── {display}")
            matched_paths.add(full_path)

    parts = [
        f"# AI PROJECT CONTEXT & HANDSHAKE REPORT\n> Mode: {'COMPLETE PROJECT' if is_full else search_term} | Views: {view_flags.upper()}\n"
        if is_markdown
        else f"==================================================\n WORLD-CLASS ULTIMATE DJANGO INSPECTION REPORT\n Mode: {'COMPLETE PROJECT' if is_full else search_term} | Views: {view_flags.upper()}\n==================================================\n"
    ]
    if view_flags == "all" or "s" in view_flags:
        parts.append(f"=== 0. PROJECT METRICS & STATISTICS ===\n • Total Files Scanned : {stats['total_files']}\n • Python (.py) Files  : {stats['py_files']}\n • Total Lines of Code : {stats['total_lines']} lines\n")
    if view_flags == "all" or "t" in view_flags:
        parts.append("=== 1. TREE VIEW STRUCTURE ===\n" + "\n".join(tree_lines))
    if view_flags == "all" or "p" in view_flags:
        parts.append("\n=== 2. FULL PATH VIEWS ===\n" + "\n".join(sorted(matched_paths)))
    if view_flags == "all" or "u" in view_flags:
        parts.append("\n=== 3. URL ENDPOINTS EXTRACTED ===\n" + ("\n".join(f" • {k} -> {v}" for k, v in endpoint_data.items()) or " • No endpoints found."))
    if view_flags == "all" or "m" in view_flags:
        parts.append("\n=== 4. DJANGO MODELS SUMMARY ===\n" + ("\n".join(f" • {k} -> Models: {v}" for k, v in model_data.items()) or " • No models found."))
    if view_flags == "all" or "w" in view_flags:
        parts.append("\n=== 5. WORKFLOW & CROSS-APP DEPENDENCIES ===\n" + ("\n".join(f" • {k} -> Depends on Apps: {list(v)}" for k, v in workflow_data.items()) or " • No cross-app dependencies found."))
    if view_flags == "all" or "f" in view_flags:
        parts.append("\n=== 6. FLOW CHART / ARCHITECTURE DIAGRAM (Mermaid) ===\n" + generate_mermaid_flowchart(workflow_data, model_data))
    if view_flags == "all" or "g" in view_flags:
        git_info = get_git_status()
        parts.append(f"\n=== 7. GIT INTEGRATION STATUS ===\n • Modified Files  : {git_info['modified']}\n • Untracked Files : {git_info['untracked']}")

    return "\n".join(parts), workflow_data, model_data


def update_readme_mermaid(chart_code: str):
    if not README_FILE.exists():
        README_FILE.write_text(f"# HYBRID MARKETPLACE - Django Project\n\n## Architecture Flow Chart\n\n{chart_code}\n", encoding="utf-8")
        return
    content = README_FILE.read_text(encoding="utf-8", errors="ignore")
    if "```mermaid" in content:
        new_content = re.sub(r"```mermaid.*?```", chart_code, content, flags=re.DOTALL)
    else:
        new_content = content + f"\n\n## Architecture Flow Chart\n\n{chart_code}\n"
    README_FILE.write_text(new_content, encoding="utf-8")


def main():
    docs_dir = ensure_documents_dir()

    print("==================================================")
    print("  WORLD-CLASS ULTIMATE DJANGO PROJECT INSPECTOR   ")
    print("==================================================")
    search_term = input("Search term (or press [ENTER] for Full View) -> ").strip()

    exact_match = False
    if search_term:
        choice_exact = input("Do you want EXACT MATCH? (y/n): ").strip().lower()
        if choice_exact == "y":
            exact_match = True

    print("\nAvailable View Flags:")
    print("  [t] Tree View       [p] Path View       [s] Stats")
    print("  [u] URL Endpoints   [m] Models Summary  [w] Workflow")
    print("  [f] Flow Chart      [g] Git Status")
    print("\nTip: Combine letters (e.g., 'tp') or simply press [ENTER] for ALL features.")

    view_flags = input("Select options -> ").strip().lower() or "all"

    txt_content, _, _ = generate_inspection_report(PROJECT_ROOT, search_term, exact_match, view_flags, is_markdown=False)
    md_content, wf_data, mod_data = generate_inspection_report(PROJECT_ROOT, search_term, exact_match, view_flags, is_markdown=True)

    txt_file = docs_dir / "project_tree_path_view.txt"
    md_file = docs_dir / "AI_PROJECT_CONTEXT.md"
    txt_file.write_text(txt_content, encoding="utf-8")
    md_file.write_text(md_content, encoding="utf-8")
    update_readme_mermaid(generate_mermaid_flowchart(wf_data, mod_data))

    print("\n==================================================")
    print("SUCCESS: All updates completed automatically!")
    print(f" 1. Personal TXT Report : {txt_file.relative_to(PROJECT_ROOT)}")
    print(f" 2. AI Context File     : {md_file.relative_to(PROJECT_ROOT)}")
    print(f" 3. README.md Flowchart : {README_FILE.relative_to(PROJECT_ROOT)}")
    print("==================================================")


if __name__ == "__main__":
    main()