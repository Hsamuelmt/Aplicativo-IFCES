#!/usr/bin/env python
"""
Local Production Testing Script
Tests the application with a production server.

On Windows it uses Waitress.
On Linux/macOS it uses Gunicorn (same as Render.com).

Usage:
    python scripts/run_local_production.py
    
Then visit: http://127.0.0.1:8000
"""

import os
import argparse
import subprocess
import sys
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
ENV_FILE = PROJECT_ROOT / ".env"
IS_WINDOWS = os.name == "nt"

def print_header(text):
    """Print formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_requirements():
    """Verify all requirements are met."""
    print_header("Checking Requirements")
    
    # Check .env file
    if not ENV_FILE.exists():
        print(".env file not found")
        print("Creating from .env.example...")
        env_example = PROJECT_ROOT / ".env.example"
        if env_example.exists():
            import shutil
            shutil.copy(env_example, ENV_FILE)
            print(f"Created {ENV_FILE}")
        else:
            print(".env.example not found")
            return False
    else:
        print(".env file exists")
    
    # Check required server package by OS.
    print("\nChecking Python packages...")
    if IS_WINDOWS:
        try:
            import waitress  # noqa: F401
            print("waitress installed")
        except ImportError:
            print("waitress not installed - installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "waitress"])
            print("waitress installed")
    else:
        try:
            import gunicorn  # noqa: F401
            print("gunicorn installed")
        except ImportError:
            print("gunicorn not installed - installing...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "gunicorn"])
            print("gunicorn installed")
    
    try:
        import flask
        print("flask installed")
    except ImportError:
        print("Missing dependencies - run: pip install -r requirements.txt")
        return False
    
    return True

def run_server():
    """Run the production-like server for the current OS."""
    server_name = "Waitress" if IS_WINDOWS else "Gunicorn"
    print_header(f"Starting {server_name} Server")

    cmd = [
        sys.executable,
        "-m",
        "waitress" if IS_WINDOWS else "gunicorn",
    ]

    if IS_WINDOWS:
        cmd.extend([
            "--listen=0.0.0.0:8000",
            "app:app",
        ])
    else:
        cmd.extend([
            "--workers", "4",
            "--bind", "0.0.0.0:8000",
            "--timeout", "120",
            "--access-logfile", "-",
            "--error-logfile", "-",
            "app:app",
        ])
    
    print("Command:")
    print(" ".join(cmd))
    print("\nServer will run at: http://127.0.0.1:8000")
    if IS_WINDOWS:
        print("Using Waitress for local Windows validation")
    else:
        print("Using Gunicorn (Render-compatible)")
    print("Press Ctrl+C to stop\n")
    
    try:
        os.chdir(PROJECT_ROOT)
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        print("\n\nServer stopped")
        return True
    except Exception as e:
        print(f"Error running server: {e}")
        return False
    return True

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Local production server validation")
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Validate configuration and dependencies without starting the server",
    )
    args = parser.parse_args()

    print("""
============================================================
 Flask RBAC - Local Production Test Environment
============================================================

This script simulates production deployment:
- Windows: Waitress
- Linux/macOS: Gunicorn (same model used on Render)
    """)
    
    # Check requirements
    if not check_requirements():
        print("Requirements check failed")
        return 1

    if args.check_only:
        server_name = "Waitress" if IS_WINDOWS else "Gunicorn"
        print(f"Validation OK. Local server backend: {server_name}")
        return 0
    
    # Run production-like server
    if run_server():
        return 0
    return 1

if __name__ == "__main__":
    sys.exit(main())
