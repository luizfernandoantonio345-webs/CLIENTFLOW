# 🚀 DEPLOYMENT PARA PRODUÇÃO - CLIENTFLOW

**Data:** 19 de Fevereiro de 2026  
**Status:** ✅ Pronto para Deploy  
**Repositório:** https://github.com/santossod345-lang/CLIENTFLOW-Dev

---

## 📋 CHECKLIST PRÉ-DEPLOYMENT

- ✅ Backend limpo (sem arquivos legados)
- ✅ Frontend React Vite pronto
- ✅ Dockerfile otimizado
- ✅ railway.toml configurado
- ✅ vercel.json configurado
- ✅ Git commit feito e pushed
- ✅ Banco SQLite local funcional (test.db)

---

## 🚂 DEPLOY NO RAILWAY (Backend + Database)

### Passo 1: Acessar Railway
1. Abra: **https://railway.app**
2. Faça login com sua conta GitHub
3. Clique em **"Create New Project"**

### Passo 2: Conectar GitHub
1. Selecione **"Deploy from GitHub"**
2. Selecione o repositório: **santossod345-lang/CLIENTFLOW-Dev**
3. Selecione a branch: **main**
4. Clique em **"Deploy"**

### Passo 3: Configurar PostgreSQL
1. No dashboard Railway, clique em **"+ Create"**
2. Selecione **"Database"** → **"PostgreSQL 15"**
3. Selecione a conexão com seu projeto
4. Copie a variável de ambiente `DATABASE_URL` (Railroad fornecerá automaticamente)

### Passo 4: Configurar Variáveis de Ambiente

No Railway, vá para **Settings** → **Variables** e adicione:

```
# JWT & Security
JWT_SECRET_KEY=seu-secret-key-super-seguro-aqui-prod-2026
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Database (GERADO AUTOMATICAMENTE - não altere)
# DATABASE_URL=postgresql+psycopg2://user:password@host:port/dbname

# Environment
ENVIRONMENT=production
LOG_LEVEL=info
PYTHONUNBUFFERED=1

# API Config
API_PORT=8000
API_HOST=0.0.0.0

# CORS (ajuste para seus domínios)
CORS_ORIGINS=["https://seu-dominio-frontend.vercel.app","https://seu-dominio.com"]

# Redis (opcional - Railway fornecerá)
# REDIS_URL=redis://...

# Email (se usar)
# SMTP_SERVER=...
# SMTP_PORT=...
```

### Passo 5: Monitorar Build

1. Vá para a aba **"Deployments"** no Railway
2. Aguarde o build completar (deve levar ~3-5 minutos)
3. Verifique os logs:
   - Se verde ✅ = Deploy bem-sucedido
   - Se vermelho ❌ = Verifique os logs

### Resultado Esperado
```
✅ Build completado
✅ Aplicação rodando na porta 8000
✅ PostgreSQL conectado
✅ URL pública gerada (exemplo: https://clientflow-prod.railway.app)
```

---

## 🌐 DEPLOY NO VERCEL (Frontend)

### Passo 1: Acessar Vercel
1. Abra: **https://vercel.com/new**
2. Faça login com sua conta GitHub
3. Selecione o repositório: **CLIENTFLOW-Dev**

### Passo 2: Configuração de Build
Vercel detectará automaticamente:
```
Build Command: npm run build (no clientflow-frontend/)
Output Directory: clientflow-frontend/dist
```

Se não auto-detectar, configure manualmente:
1. Framework: **Vite**
2. Root Directory: **clientflow-frontend/**
3. Build Command: `npm run build`
4. Output Directory: `dist`

### Passo 3: Configurar Variáveis de Ambiente

Adicione no Vercel:
```
VITE_API_URL=https://seu-backend-railway.railway.app
```

Substitua `seu-backend-railway` pela URL que o Railway forneceu.

### Passo 4: Deploy
1. Clique em **"Deploy"**
2. Aguarde o build completar (~2-3 minutos)
3. Você receberá uma URL pública (exemplo: `https://clientflow-prod.vercel.app`)

---

## 🔗 CONECTAR FRONTEND AO BACKEND

Após ambos os deploys:

1. **URL do Backend Railway:** 
   - Copie de: https://railway.app → seu projeto → Settings
   - Exemplo: `https://clientflow-prod.railway.app`

2. **Atualizar Vercel com Backend URL:**
   - Vá para Vercel → seu projeto → Settings → Environment Variables
   - Atualize: `VITE_API_URL=<sua-url-railway>`
   - Clique em **"Redeploy"** para aplicar

3. **Testar Conexão:**
   ```
   Frontend: https://seu-dominio.vercel.app
   Backend API: https://seu-dominio.railway.app/api/health
   ```

---

## 🗄️ BANCO DE DADOS - MIGRAÇÃO

Após Railway estar rodando, o `init_prod.py` executará automaticamente:
1. Verificar conexão com PostgreSQL
2. Executar migrações Alembic (`alembic upgrade head`)
3. Criar tabelas necessárias

**Se precisar de manual:**
```bash
# No Railway SSH Terminal
alembic upgrade head
```

---

## 🧪 TESTES APÓS DEPLOY

### 1. Verificar Backend
```bash
curl https://seu-backend.railway.app/api/health
# Esperado: {"status":"ok"}
```

### 2. Verificar Frontend
Abra no navegador:
```
https://seu-frontend.vercel.app
```

### 3. Testar Login
1. Acesse o frontend
2. Faça login com credenciais de teste
3. Verifique se conecta ao backend

### 4. Monitorar Logs

**Railway:**
- Dashboard → Logs → veja output do servidor

**Vercel:**
- Deployments → Logs → veja build e serverless logs

---

## ⚠️ TROUBLESHOOTING

### Railway não consegue conectar ao PostgreSQL
```
Solução:
1. Verifique se DATABASE_URL está correta
2. Reinicie a aplicação no Railway (Restart Deploy)
3. Verifique firewall/network policies
```

### Frontend não conecta ao Backend
```
Solução:
1. Verifique VITE_API_URL no Vercel
2. Verifique CORS_ORIGINS no Railway
3. Tente manualmente: fetch('https://backend.url/api/health')
```

### Build falha no Railway
```
Solução:
1. Verifique requirements.txt (compatibilidade Python)
2. Verifique Dockerfile (caminhos corretos)
3. Limpe o cache: Railway → Trigger Redeploy → Clear cache
```

### Build falha no Vercel
```
Solução:
1. Verifique package.json no clientflow-frontend/
2. Verifique npm run build localmente
3. Limpe cache: Vercel → Redeployments → Redeploy
```

---

## 📊 URLs FINAIS

Após sucesso:

| Serviço | URL | Tipo |
|---------|-----|------|
| **Frontend** | https://seu-app.vercel.app | React SPA |
| **Backend** | https://seu-app.railway.app | FastAPI |
| **API Docs** | https://seu-app.railway.app/docs | Swagger |
| **Database** | PostgreSQL (internamente) | SQL |

---

## 🔐 SEGURANÇA EM PRODUÇÃO

Verifique:
- ✅ `.env` **NÃO** está no repo (em .gitignore)
- ✅ JWT_SECRET_KEY é único e forte
- ✅ CORS_ORIGINS têm domínios específicos (não `*`)
- ✅ Banco de dados está em servidor seguro
- ✅ HTTPS ativado em ambas plataformas (automático)
- ✅ Senhas hasheadas com bcrypt

---

## 📞 SUPORTE

Se encontrar problemas:

1. **Logs Railway:** https://railway.app → Logs
2. **Logs Vercel:** https://vercel.com → Deployments → Logs
3. **GitHub:** https://github.com/santossod345-lang/CLIENTFLOW-Dev/issues

---

## ✨ RESUMO RÁPIDO

```
1. Railway:
   - Conectar GitHub
   - Adicionar PostgreSQL
   - Configurar variáveis
   - Aguardar build (3-5 min)
   - Copiar URL pública

2. Vercel:
   - Conectar GitHub
   - Adicionar VITE_API_URL
   - Aguardar build (2-3 min)
   - Testar frontend

3. Conectar:
   - Atualizar VITE_API_URL no Vercel
   - Verificar CORS no Railway
   - Redeploy ambos

4. Testar:
   - Acessar frontend
   - Acessar backend /docs
   - Fazer login
   - 🎉 LIVE!
```

---

**Tempo total estimado:** 15-20 minutos  
**Dificuldade:** Fácil (apenas cliques e cópias)  
**Resultado:** SaaS em produção 🚀

