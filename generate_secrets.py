#!/usr/bin/env python3
"""
Generate secure secrets for production
"""
import secrets
import json
from pathlib import Path

def generate_secret_key(length=32):
    """Generate a cryptographically secure SECRET_KEY"""
    return secrets.token_urlsafe(length)

def main():
    # Generate SECRET_KEY
    secret_key = generate_secret_key()
    
    # Create prod_secrets.json
    secrets_data = {
        "SECRET_KEY": secret_key,
    }
    
    secrets_file = Path("prod_secrets.json")
    secrets_file.write_text(json.dumps(secrets_data, indent=2))
    
    print("✓ Secrets generated successfully!")
    print(f"  SECRET_KEY: {secret_key}")
    print(f"  Saved to: prod_secrets.json")
    print("\n⚠ IMPORTANT: Add prod_secrets.json to .gitignore and never commit it!")
    print("  Keep SECRET_KEY secure and add it to your Railway environment variables")

if __name__ == "__main__":
    main()
