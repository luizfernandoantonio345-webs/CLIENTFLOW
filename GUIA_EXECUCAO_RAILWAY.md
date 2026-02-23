# GUIA DE EXECUÇÃO - CLIENTFLOW COM CORREÇÕES

## EXECUTAR LOCALMENTE

### 1. Setup do Ambiente
```bash
cd c:\Users\Sueli\Desktop\ClientFlow

# Criar virtual environment (se não existir)
python -m venv .venv
.venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Variáveis de Ambiente (local)
Criar arquivo `.env`:
```
ENVIRONMENT=development
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
DATABASE_URL=postgresql://clientflow:clientflow@localhost:5432/clientflow
JWT_SECRET_KEY=sua-chave-super-secreta-desenvolvimento
CORS_ALLOW_CREDENTIALS=true
```

### 3. Database Setup (se PostgreSQL está rodando)
```bash
# Aplicar migrations
alembic upgrade head

# Ou criar schema manualmente
python init_prod.py
```

### 4. Rodar Backend Localmente

#### Opção A: Gunicorn (como em produção)
```bash
gunicorn backend.main:app \
  -k uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --workers 1 \
  --timeout 120
```

#### Opção B: Uvicorn direto (mais rápido para dev)
```bash
uvicorn backend.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
```

#### Opção C: Script Python direto
```bash
python -c "from backend.main import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)"
```

### 5. Validar Endpoints Localmente
```bash
# GET /
curl http://localhost:8000/

# GET /status (readiness - Railway uses this)
curl http://localhost:8000/status

# GET /public/health (sem auth)
curl http://localhost:8000/public/health

# GET /api/health (API health)
curl http://localhost:8000/api/health

# Swagger Docs
open http://localhost:8000/docs
```

---

## EXECUTAR EM RAILWAY

### Pré-requisitos
```bash
# 1. Instalar Railway CLI
npm install -g @railway/cli

# 2. Login no Railway
railway login

# 3. Link projeto (substitua PROJECT_ID)
railway link c15ea1ba-d177-40b4-8b6f-ed071aeeef08
```

### Deployment

#### Opção 1: Railway CLI (Recomendado)
```bash
# Fazer push do código
railway up

# Verificar logs em tempo real
railway logs -f

# Ver variáveis de environment
railway env
```

#### Opção 2: Push GitHub
```bash
git push origin main
# Railway faz deploy automático se CI/CD estiver configurado
```

### Configurar Variáveis de Ambiente no Railway

No dashboard Railway, adicionar:
```
ENVIRONMENT=production
ALLOWED_ORIGINS=https://seu-frontend.vercel.app
DATABASE_URL=postgresql://user:password@host:5432/dbname
JWT_SECRET_KEY=gerar-uma-chave-aleatoria-forte
RUN_MIGRATIONS_ON_STARTUP=true
```

### Health Checks no Railway

Railway usa este endpoint para verificar se app está up:
```
GET /status
```

Se retornar 200 com `"status": "ready"` → App considerad healthy

### Verificar Deploy

```bash
# 1. Pegar URL do Railway
railway domain

# 2. Testar root
curl https://seu-domain.railway.app/

# 3. Testar status
curl https://seu-domain.railway.app/status

# 4. Testar public endpoint
curl https://seu-domain.railway.app/public/health

# 5. Ver logs
railway logs --follow
```

---

## INTEGRAÇÃO VERCEL + RAILWAY

### Frontend (Vercel) Configuration

Arquivo `vercel.json`:
```json
{
  "builds": [
    {"src": "clientflow-frontend/package.json", "use": "@vercel/static-build"}
  ],
  "env": {
    "VITE_API_URL": "@api-url"
  },
  "routes": [
    {"handle": "filesystem"},
    {"src": "/.*", "dest": "/index.html"}
  ]
}
```

### Enviroçment Variables do Vercel

Adicionar no Vercel Dashboard:
```
VITE_API_URL=https://seu-railway-domain.railway.app
```

### Frontend Code (React/fetch)

```javascript
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Login
fetch(`${API_URL}/api/empresas/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email_login, senha })
})
  .then(r => r.json())
  .then(data => {
    localStorage.setItem('access_token', data.access_token);
  });

// Fetch protegido
fetch(`${API_URL}/api/dashboard`, {
  headers: {
    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
  }
})
  .then(r => r.json());
```

---

## TROUBLESHOOTING

### Problema: 502 Bad Gateway no Railway

**Checklist:**
1. ✓ APP iniciou? Ver `railway logs -f`
2. ✓ DATABASE_URL está set? `railway env | grep DATABASE_URL`
3. ✓ PORT está correto? Railway seta `$PORT` env var
4. ✓ App ouve em `0.0.0.0:${PORT}`? Verificar Procfile
5. ✓ Migrations rodaram? Ver logs após `release` phase

**Comum:** Migrations travadas por conexão DB lenta
```
RUN_MIGRATIONS_ON_STARTUP=false
# Rodar manualmente depois:
railway run alembic upgrade head
```

### Problema: 404 nos endpoints /public/*

**Checklist:**
1. ✓ Router public.py existe?
2. ✓ Importado em main.py? `from backend.routers import public`
3. ✓ Incluído router? `app.include_router(public.router)`
4. ✓ Verificar logs de rotas: `/docs` lista todas?

### Problema: CORS error from Vercel

**Checklist:**
1. ✓ ALLOWED_ORIGINS inclui domínio Vercel?
```
ALLOWED_ORIGINS=https://seu-projeto.vercel.app
```
2. ✓ CORSMiddleware adicionado?
3. ✓ allow_origins é lista, não string única?
4. ✓ Endpoint é /public/* (sem auth)? Requer Access-Control headers

### Problema: DatabaseError "connection refused"

**Checklist:**
1. ✓ DATABASE_URL está válido? Testar em psql
2. ✓ Banco está online? `psql $DATABASE_URL -c "SELECT 1"`
3. ✓ IP está whitelisted no Postgres?
4. ✓ Credentials corretos?

**Para Railway PostgreSQL:**
- Railway cria DB automático
- DATABASE_URL é fornecido automaticamente
- Não precisa criar manualmente

### Problema: "SECRET_KEY not set" em produção

**Solução:**
```
JWT_SECRET_KEY=sua-chave-aleatoria-512-bits
```

Gerar chave:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## SCRIPTS ÚTEIS

### Testar Localmente (sem banco de dados)
```bash
python test_system.py      # Valida imports
python check_routes.py     # Lista todas as rotas
python test_endpoints.py   # Testa HTTP endpoints
```

### Gerar Secrets
```bash
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_hex(32))"
```

### Reset Local Database
```bash
# Deletar todos dados
alembic downgrade base

# Recriar schema
alembic upgrade head

# Inicializar
python init_prod.py
```

### Ver Logs Railway
```bash
railway logs -f              # Real-time
railway logs --since 1h      # Últimas 1 hora
railway logs | grep ERROR    # Apenas erros
```

---

## CHECKLIST PRÉ-DEPLOY

- [ ] test_system.py passa (6/6)
-[ ] test_endpoints.py passa (8/9 ou mais)
- [ ] check_routes.py mostra todas as rotas
- [ ] Sem warnings de "Duplicate Operation ID"
- [ ] ALLOWED_ORIGINS está correto no .env
- [ ] DATABASE_URL está correto
- [ ] JWT_SECRET_KEY é uma string forte
- [ ] RUN_MIGRATIONS_ON_STARTUP está definido
- [ ] Procfile aponta correto: `backend.main:app`
- [ ] requirements.txt tem gunicorn + uvicorn
- [ ] Git status está limpo (sem uncommitted changes)

---

## PÓS-DEPLOY VALIDATION

Após deploy no Railway, executar:

```bash
# 1. Health check
curl https://seu-railway-domain.railway.app/status

# 2. Verificar CORS headers
curl -H "Origin: https://seu-vercel-app.vercel.app" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: authorization" \
     -X OPTIONS https://seu-railway-domain.railway.app/api/empresas/login

# 3. Testar login mock
curl -X POST https://seu-railway-domain.railway.app/api/empresas/login \
  -H "Content-Type: application/json" \
  -d '{"email_login":"test@example.com","senha":"password"}' \\
  -v

# 4. Ver últimos logs
railway logs --limit 100
```

Se tudo retornar status 200/401 (não 502), **deploy foi sucesso**.

---

## Contato Rápido

- Railway Dashboard: https://railway.app/project/c15ea1ba-d177-40b4-8b6f-ed071aeeef08
- Railway CLI Docs: https://docs.railway.app/reference/cli
- FastAPI Docs Local: http://localhost:8000/docs
