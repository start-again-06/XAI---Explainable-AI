#!/usr/bin/env python3
"""XAI-IDS unified application starter."""

import subprocess
import sys
import os
import shutil
from pathlib import Path

LOCAL_API_TOKEN = "local-dev-auth-token-12345"
LOCAL_INGEST_TOKEN = "local-dev-ingest-token-67890"

def get_local_port() -> int:
    """Resolve API port from environment with a safe default."""
    raw_port = os.getenv("API_PORT", "8000").strip()
    try:
        port = int(raw_port)
    except ValueError:
        port = 8000
    return max(1, min(65535, port))


def print_local_links() -> None:
    """Print clean localhost links that are easy to find in terminal output."""
    port = get_local_port()
    print("\n====================================================")
    print("LOCAL LINKS")
    print(f"APP_URL=http://localhost:{port}")
    print(f"API_DOCS_URL=http://localhost:{port}/docs")
    print("====================================================\n")


def run_command(cmd, cwd=None, shell=False):
    """Run a command and return success status."""
    use_shell = shell if isinstance(cmd, str) else False
    resolved_cmd = cmd
    cmd_display = cmd if isinstance(cmd, str) else " ".join(str(part) for part in cmd)

    if isinstance(cmd, list) and cmd:
        executable = str(cmd[0])
        if not Path(executable).is_absolute():
            resolved_executable = resolve_command(executable)
            if resolved_executable:
                resolved_cmd = [resolved_executable, *cmd[1:]]

    try:
        result = subprocess.run(
            resolved_cmd,
            shell=use_shell, 
            check=True, 
            cwd=cwd,
            capture_output=True, 
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {cmd_display}")
        print(f"Error output: {e.stderr}")
        return False
    except OSError as e:
        print(f"❌ Failed to run command: {cmd_display}")
        print(f"System error: {e}")
        return False


def resolve_command(command: str) -> str | None:
    """Resolve an executable path, including Windows command shims."""
    resolved = shutil.which(command)
    if resolved:
        return resolved

    if os.name == "nt" and "." not in Path(command).name:
        for suffix in (".cmd", ".exe", ".bat"):
            resolved = shutil.which(f"{command}{suffix}")
            if resolved:
                return resolved

    return None


def has_command(command: str) -> bool:
    """Return True when a CLI command exists on PATH."""
    return resolve_command(command) is not None


def _latest_mtime(path: Path) -> float:
    """Return latest modification timestamp for a file or directory tree."""
    if not path.exists():
        return 0.0
    if path.is_file():
        return path.stat().st_mtime

    latest = 0.0
    for item in path.rglob("*"):
        if item.is_file():
            latest = max(latest, item.stat().st_mtime)
    return latest


def frontend_needs_rebuild(frontend_dir: Path, index_file: Path) -> bool:
    """Detect whether frontend sources changed after the last static build."""
    if not index_file.exists():
        return True

    build_time = index_file.stat().st_mtime
    source_paths = [
        frontend_dir / "src",
        frontend_dir / "index.html",
        frontend_dir / "package.json",
        frontend_dir / "package-lock.json",
        frontend_dir / "vite.config.js",
    ]
    latest_source_change = max((_latest_mtime(path) for path in source_paths), default=0.0)
    return latest_source_change > build_time


def ensure_frontend_assets(project_root: Path) -> bool:
    """Use bundled frontend assets when available; build only if tooling exists."""
    frontend_dir = project_root / "frontend"
    static_dir = project_root / "backend" / "static"
    index_file = static_dir / "index.html"

    needs_rebuild = frontend_dir.exists() and frontend_needs_rebuild(frontend_dir, index_file)

    if index_file.exists() and not needs_rebuild:
        print("Using bundled frontend assets from backend/static")
        return True

    if not frontend_dir.exists():
        print("Frontend directory not found and no bundled assets available")
        return False

    if not has_command("npm"):
        if index_file.exists():
            print("Frontend source changed but npm is unavailable; using existing bundled assets")
            return True
        print("No bundled frontend assets found and npm is unavailable")
        print("   Install Node.js and run `npm install && npm run build` in frontend/ once.")
        return False

    if needs_rebuild:
        print("Frontend changes detected. Rebuilding frontend assets...")
    else:
        print("Building frontend assets...")
    if not run_command(["npm", "install"], cwd=frontend_dir):
        print("Failed to install frontend dependencies")
        return False
    if not run_command(["npm", "run", "build"], cwd=frontend_dir):
        print("Failed to build frontend")
        return False

    return index_file.exists()

def main():
    """Main startup sequence"""
    project_root = Path(__file__).parent
    backend_dir = project_root / "backend"
    
    print("Starting XAI-IDS Unified Application...")
    if not ensure_frontend_assets(project_root):
        return 1
    
    # Start backend
    print("Starting backend server (includes frontend)...")
    if not backend_dir.exists():
        print("Backend directory not found")
        return 1
    
    venv_dir = backend_dir / "venv"
    backend_python = sys.executable
    requirements_file = project_root / "requirements.txt"
    backend_pip_cmd = [sys.executable, "-m", "pip"]

    if venv_dir.exists():
        if sys.platform == "win32":
            venv_python = venv_dir / "Scripts" / "python.exe"
            venv_pip = venv_dir / "Scripts" / "pip.exe"
        else:
            venv_python = venv_dir / "bin" / "python"
            venv_pip = venv_dir / "bin" / "pip"

        if not venv_python.exists() or not venv_pip.exists():
            print("Virtual environment found but python/pip executables are missing")
            return 1

        backend_python = str(venv_python)
        backend_pip_cmd = [str(venv_pip)]
        print("Virtual environment found")
    
    if not requirements_file.exists():
        print("requirements.txt not found at project root")
        return 1

    print("Ensuring Python dependencies are installed...")
    if not run_command(backend_pip_cmd + ["install", "-r", str(requirements_file)], cwd=project_root):
        print("Failed to install backend dependencies")
        return 1
    
    # Start the unified application
    port = get_local_port()
    print(f"Starting XAI-IDS on http://localhost:{port}")
    print(f"Access the application at: http://localhost:{port}")
    print(f"API docs available at: http://localhost:{port}/docs")
    print(f"Local API token: {LOCAL_API_TOKEN}")
    print("\nThe frontend and backend are served from a single port.")
    print_local_links()
    
    try:
        env = os.environ.copy()
        env.setdefault("DATABASE_URL", "sqlite:///./data/xai_ids.db")
        env.setdefault("API_AUTH_TOKEN", LOCAL_API_TOKEN)
        env.setdefault("INGEST_API_TOKEN", LOCAL_INGEST_TOKEN)
        subprocess.run([backend_python, "main.py"], cwd=backend_dir, check=True, env=env)
    except KeyboardInterrupt:
        print("\nXAI-IDS application stopped")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"Application failed to start: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
