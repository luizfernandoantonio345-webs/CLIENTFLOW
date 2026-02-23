#!/usr/bin/env python
"""Verificar rotas registradas no app"""
import sys
import json

try:
    from backend.main import app
    
    routes = []
    for route in app.routes:
        if hasattr(route, 'path') and hasattr(route, 'methods'):
            routes.append({
                "path": route.path,
                "methods": list(route.methods) if route.methods else ["*"]
            })
    
    print("=" * 60)
    print("ROTAS REGISTRADAS NO CLIENTFLOW")
    print("=" * 60)
    print(f"Total: {len(routes)} rotas\n")
    
    # Group by path
    by_prefix = {}
    for r in routes:
        prefix = r['path'].split('/')[1] if '/' in r['path'] else ''
        if prefix not in by_prefix:
            by_prefix[prefix] = []
        by_prefix[prefix].append(r)
    
    for prefix in sorted(by_prefix.keys()):
        print(f"\n/{prefix}/ ({len(by_prefix[prefix])} rotas)")
        for r in by_prefix[prefix]:
            print(f"  {' '.join(r['methods']):15s} {r['path']}")
    
    # Check critical routes
    critical = [
        '/',
        '/health', 
        '/api/health',
        '/status',
        '/public/health',
        '/api/empresas/login',
        '/api/clientes',
        '/api/atendimentos',
        '/api/dashboard'
    ]
    
    print("\n" + "=" * 60)
    print("ROTAS CRÍTICAS")
    print("=" * 60)
    
    all_paths = [r['path'] for r in routes]
    for route in critical:
        found = route in all_paths
        status = "✓" if found else "✗"
        print(f"{status} {route}")
    
    print("\n✓ Verificação concluída")
    sys.exit(0)
    
except Exception as e:
    print(f"✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
