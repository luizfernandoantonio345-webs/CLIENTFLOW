#!/usr/bin/env python
"""Teste de requisições HTTP para validar endpoints"""
import sys
from fastapi.testclient import TestClient

try:
    from backend.main import app
    
    client = TestClient(app)
    
    print("=" * 60)
    print("TESTE DE REQUISIÇÕES HTTP")
    print("=" * 60)
    
    tests = [
        ("GET", "/", 200, "Root endpoint"),
        ("GET", "/health", 200, "Health check"),
        ("GET", "/status", 200, "Status endpoint"),
        ("GET", "/api/health", 200, "API health"),
        ("GET", "/public/health", 200, "Public health"),
        ("GET", "/public/status", 200, "Public status"),
        ("GET", "/public/barbershop/test", 200, "Public barbershop"),
        ("GET", "/docs", 200, "Swagger docs"),
        ("GET", "/openapi.json", 200, "OpenAPI schema"),
    ]
    
    passed = 0
    failed = 0
    
    for method, path, expected_status, description in tests:
        try:
            if method == "GET":
                response = client.get(path)
            else:
                response = client.post(path)
            
            if response.status_code == expected_status:
                print(f"✓ {method:4s} {path:30s} {response.status_code} {description}")
                passed += 1
            else:
                print(f"✗ {method:4s} {path:30s} {response.status_code} (expected {expected_status}) {description}")
                failed += 1
        except Exception as e:
            print(f"✗ {method:4s} {path:30s} ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTADO: {passed}/{len(tests)} testes passaram")
    print("=" * 60)
    
    if failed == 0:
        print("✓ TODOS OS ENDPOINTS FUNCIONANDO")
        sys.exit(0)
    else:
        print("✗ ALGUNS ENDPOINTS FALHARAM")
        sys.exit(1)
        
except Exception as e:
    print(f"✗ Erro: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
