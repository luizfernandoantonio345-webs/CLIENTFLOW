#!/usr/bin/env python3
"""
Railway Environment Setup Script
Configures production environment variables on Railway via GraphQL API
"""
import os
import sys
import json
import subprocess
from pathlib import Path

# Railway Project ID (from previous setup)
PROJECT_ID = "c15ea1ba-d177-40b4-8b6f-ed071aeeef08"

def get_railway_token():
    """Get Railway authentication token from local config"""
    token_paths = [
        Path.home() / ".railway" / "token",
        Path.home() / ".railwayrc",
        Path(os.getenv("RAILWAY_TOKEN_PATH", "")),
    ]
    
    for path in token_paths:
        if path.exists():
            try:
                token = path.read_text().strip()
                if token:
                    return token
            except:
                pass
    
    # Check environment variable
    token = os.getenv("RAILWAY_TOKEN")
    if token:
        return token
    
    return None

def run_command(cmd, capture_output=True):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            text=True,
            timeout=30
        )
        return result.returncode, result.stdout, result.stderr
    except Exception as e:
        return 1, "", str(e)

def setup_variables():
    """Setup environment variables via railway CLI"""
    variables = {
        "ENVIRONMENT": "production",
        "LOG_LEVEL": "info",
        "PYTHONUNBUFFERED": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "SECRET_KEY": os.getenv("SECRET_KEY", "kzxouAjw2KFlgN8moMLLVg7l1IPoFBlOAoiB_mD17uc"),
        "ALLOWED_ORIGINS": "https://clientflow.vercel.app,http://localhost:3000",
    }
    
    print("\n=== Setting up Railway Environment Variables ===\n")
    
    for key, value in variables.items():
        print(f"Setting {key}...")
        cmd = f'railway variable set {key}="{value}"'
        returncode, stdout, stderr = run_command(cmd, capture_output=False)
        
        if returncode != 0:
            print(f"  ⚠ Error setting {key}: {stderr}")
        else:
            print(f"  ✓ {key} set successfully")
    
    print("\n=== Variable Setup Complete ===\n")

def add_postgres_service():
    """Add PostgreSQL service via Railway"""
    print("\n=== Adding PostgreSQL Service ===\n")
    
    # Try to add postgres service
    cmd = 'railway add --name postgres --plugin postgres'
    returncode, stdout, stderr = run_command(cmd, capture_output=False)
    
    if returncode == 0:
        print("✓ PostgreSQL service added successfully")
    else:
        print(f"⚠ Could not auto-add PostgreSQL (you may need to add it manually)")
        print(f"  Visit: https://railway.app/project/{PROJECT_ID}")
        print(f"  Click 'Add Service' → 'Postgres Database'")
    
    print("\n=== Service Setup Complete ===\n")

def trigger_deployment():
    """Trigger a new deployment after configuration"""
    print("\n=== Triggering Deployment ===\n")
    
    cmd = 'railway up'
    print("Starting deployment...")
    returncode, stdout, stderr = run_command(cmd, capture_output=False)
    
    if returncode == 0:
        print("✓ Deployment triggered successfully")
    else:
        print(f"⚠ Deployment encountered issues")
        print(f"  Check logs: https://railway.app/project/{PROJECT_ID}")
    
    print("\n=== Deployment Complete ===\n")

def main():
    """Main setup routine"""
    print("""
╔════════════════════════════════════════╗
║   ClientFlow Railway Setup Script      ║
║   Production Environment Configuration ║
╚════════════════════════════════════════╝
    """)
    
    # Check if railway CLI is available
    returncode, _, _ = run_command('railway --version')
    if returncode != 0:
        print("✗ Railway CLI not found. Please install it:")
        print("  npm install -g @railway/cli")
        sys.exit(1)
    
    print("✓ Railway CLI found\n")
    
    # Check authentication
    token = get_railway_token()
    if token:
        print("✓ Railway authentication detected\n")
    else:
        print("⚠ Railway token not found")
        print("  Run 'railway login' to authenticate\n")
    
    # Run setup steps
    try:
        setup_variables()
        add_postgres_service()
        trigger_deployment()
        
        print("""
╔════════════════════════════════════════╗
║          Setup Complete!              ║
║  Monitor deployment at:               ║
║  https://railway.app/project/{PROJECT_ID}
╚════════════════════════════════════════╝
        """.format(PROJECT_ID=PROJECT_ID))
        
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
