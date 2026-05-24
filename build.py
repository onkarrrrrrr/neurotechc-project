#!/usr/bin/env python
"""Build script for Vercel deployment"""
import os
import sys
import subprocess

def run_command(cmd):
    """Run a command and exit on failure"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "neurotechc.settings")
    
    # Install dependencies
    print("Installing dependencies...")
    run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Collect static files
    print("Collecting static files...")
    run_command([sys.executable, "manage.py", "collectstatic", "--noinput"])
    
    # Run migrations
    print("Running migrations...")
    run_command([sys.executable, "manage.py", "migrate", "--noinput"])
    
    print("Build completed successfully!")

if __name__ == "__main__":
    main()
