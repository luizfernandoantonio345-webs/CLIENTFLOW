#!/usr/bin/env python
"""Verify app structure"""
import sys

try:
    from backend.main import app
    print("✓ App imported successfully")
    print(f"  Total routes: {len(app.routes)}")
    print("\nRoutes:")
    for i, route in enumerate(app.routes[:30]):
        if hasattr(route, 'path'):
            methods = route.methods if hasattr(route, 'methods') else 'unknown'
            print(f"  {i+1}. {route.path}: {methods}")
    
    print("\n✓ App structure is valid")
    sys.exit(0)
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
