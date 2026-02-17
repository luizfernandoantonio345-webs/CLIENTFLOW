#!/usr/bin/env python3
"""
Railway startup script - Runs Alembic migrations before starting the server
"""
import os
import sys
import subprocess

def main():
    print("🔄 Running Alembic migrations...")
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        print("✅ Migrations completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Migration warning: {e}", file=sys.stderr)
        print(e.stdout)
        print(e.stderr, file=sys.stderr)
        # Don't fail if migrations have issues - let the app start
        print("⏭️  Continuing with server startup...")
    except FileNotFoundError:
        print("⚠️  Alembic not found, skipping migrations", file=sys.stderr)
    
    print("🚀 Starting Gunicorn server...")
    port = os.getenv("PORT", "8000")
    
    os.execvp("gunicorn", [
        "gunicorn",
        "backend.main:app",
        "--bind", f"0.0.0.0:{port}",
        "--workers", "2",
        "--worker-class", "uvicorn.workers.UvicornWorker",
        "--timeout", "120",
        "--access-logfile", "-",
        "--error-logfile", "-"
    ])

if __name__ == "__main__":
    main()
