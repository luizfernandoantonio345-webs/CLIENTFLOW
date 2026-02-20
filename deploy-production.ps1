#!/usr/bin/env powershell
<#
.SYNOPSIS
  Script de Deploy Automático para ClientFlow em Railway + Vercel
  
.DESCRIPTION
  Este script automatiza o processo de deploy para produção
  
.USAGE
  .\deploy-production.ps1
#>

$RED = "`e[31m"
$GREEN = "`e[32m"
$YELLOW = "`e[33m"
$BLUE = "`e[34m"
$RESET = "`e[0m"

Write-Host "`n$BLUE╔════════════════════════════════════════════════════╗$RESET"
Write-Host "$BLUE║  🚀 ClientFlow - Deploy para Produção             ║$RESET"
Write-Host "$BLUE╚════════════════════════════════════════════════════╝$RESET`n"

# Verificar status git
Write-Host "$YELLOW[1/5]$RESET Verificando status do repositório..."
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "$RED✗ Há alterações não commitadas:$RESET"
    git status --short
    Write-Host "`n$RED Faça commit antes de deployar!$RESET"
    exit 1
}
Write-Host "$GREEN✓ Repositório limpo$RESET`n"

# Verificar branch
Write-Host "$YELLOW[2/5]$RESET Verificando branch..."
$currentBranch = git rev-parse --abbrev-ref HEAD
if ($currentBranch -ne "main") {
    Write-Host "$RED✗ Você não está na branch 'main' (está em: $currentBranch)$RESET"
    exit 1
}
Write-Host "$GREEN✓ Branch main ativa$RESET`n"

# Verificar último commit
Write-Host "$YELLOW[3/5]$RESET Últimos commits:"
git log --oneline -3
Write-Host ""

# Resumo do que será deployado
Write-Host "$YELLOW[4/5]$RESET Resumo do Projeto:"
Write-Host "  📦 Backend: FastAPI (backend/)"
Write-Host "  🎨 Frontend: React Vite (clientflow-frontend/)"
Write-Host "  🗄️  Database: PostgreSQL (Railway)"
Write-Host "  🌐 Hosting: Railway + Vercel"
Write-Host ""

# Instruções
Write-Host "$YELLOW[5/5]$RESET Próximas Etapas:$RESET`n"

Write-Host "$BLUE═══════ 🚂 RAILWAY (Backend + Database) ═══════$RESET"
Write-Host "  1. Abra: https://railway.app"
Write-Host "  2. Clique: 'Create New Project'"
Write-Host "  3. Selecione: 'Deploy from GitHub'"
Write-Host "  4. Repositório: santossod345-lang/CLIENTFLOW-Dev"
Write-Host "  5. Branch: main"
Write-Host "  6. Aguarde o build completar"
Write-Host "  7. Copie a URL pública (ex: https://app.railway.app)"
Write-Host ""

Write-Host "$BLUE═══════ 🌐 VERCEL (Frontend) ═══════$RESET"
Write-Host "  1. Abra: https://vercel.com/new"
Write-Host "  2. Selecione repositório: CLIENTFLOW-Dev"
Write-Host "  3. Configure:"
Write-Host "     - Framework: Vite"
Write-Host "     - Root Directory: clientflow-frontend/"
Write-Host "     - Build Command: npm run build"
Write-Host "     - Output: dist"
Write-Host "  4. Adicione variável de ambiente:"
Write-Host "     - VITE_API_URL=<sua-url-railway>"
Write-Host "  5. Clique: Deploy"
Write-Host ""

Write-Host "$BLUE═══════ 🔗 CONECTAR ═══════$RESET"
Write-Host "  1. Copie URL do Railway"
Write-Host "  2. Vá para Vercel → Projeto → Settings"
Write-Host "  3. Atualize: VITE_API_URL=<railway-url>"
Write-Host "  4. Redeploy no Vercel"
Write-Host ""

Write-Host "$GREEN╔════════════════════════════════════════════════════╗$RESET"
Write-Host "$GREEN║  ✅ Tudo pronto para deploy!                     ║$RESET"
Write-Host "$GREEN║  Tempo estimado: 15-20 minutos                   ║$RESET"
Write-Host "$GREEN╚════════════════════════════════════════════════════╝$RESET`n"

# Opção de abrir recursos
$openBrowser = Read-Host "Deseja abrir as URLs no navegador? (S/N)"
if ($openBrowser -eq "S") {
    Write-Host "`nAbrindo navegadores...`n"
    Start-Process "https://railway.app"
    Start-Sleep -Seconds 2
    Start-Process "https://vercel.com/new"
}

Write-Host "$GREEN✨ Instruções completas em: DEPLOYMENT_INSTRUCTIONS.md$RESET`n"
