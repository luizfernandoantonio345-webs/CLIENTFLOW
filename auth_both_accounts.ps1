# Script de Autenticacao para Ambas as Contas GitHub
# Configuracao automatica de credenciais

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "  Autenticacao para Duas Contas GitHub" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configurando Git para funcionar com ambas as contas..." -ForegroundColor Yellow
Write-Host ""

# Configurar Git Credential Manager para armazenar credenciais
Write-Host "[1/3] Configurando Git Credential Manager..." -ForegroundColor Cyan
git config --global credential.helper wincred
git config --global credential.useHttpPath true

Write-Host "OK - Credential Manager ativado" -ForegroundColor Green
Write-Host ""

# Configurar URLs para usar credenciais específicas
Write-Host "[2/3] Configurando URLs dos repositorios..." -ForegroundColor Cyan

git remote set-url origin "https://github.com/santossod345-lang/CLIENTFLOW-Dev.git"
git remote set-url upstream "https://github.com/luizfernandoantonio345-webs/CLIENTFLOW.git"

Write-Host "OK - URLs configuradas" -ForegroundColor Green
Write-Host ""

# Testar conexões
Write-Host "[3/3] Testando conexoes..." -ForegroundColor Cyan
Write-Host ""

Write-Host "Testando acesso a santossod345-lang..." -ForegroundColor Yellow
$testOrigin = & git ls-remote "https://github.com/santossod345-lang/CLIENTFLOW-Dev.git" 2>&1 | Select-Object -First 1
if ($testOrigin -and -not ($testOrigin -match "fatal")) {
    Write-Host "OK - Repositorio de Santos acessivel" -ForegroundColor Green
} else {
    Write-Host "! - Pode ser necessario autenticar ao sincronizar" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Testando acesso a luizfernandoantonio345-webs..." -ForegroundColor Yellow
$testUpstream = & git ls-remote "https://github.com/luizfernandoantonio345-webs/CLIENTFLOW.git" 2>&1 | Select-Object -First 1
if ($testUpstream -and -not ($testUpstream -match "fatal")) {
    Write-Host "OK - Repositorio de Luiz acessivel" -ForegroundColor Green
} else {
    Write-Host "! - Pode ser necessario autenticar ao sincronizar" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host "Configuracao concluida!" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Quando o Git pedir autenticacao:" -ForegroundColor Cyan
Write-Host "- Para origin (Santos): Use usuario 'santossod345-lang'" -ForegroundColor White
Write-Host "- Para upstream (Luiz): Use usuario 'luizfernandoantonio345-webs'" -ForegroundColor White
Write-Host ""
Write-Host "Use seu GitHub PAT como password" -ForegroundColor Yellow
Write-Host ""

Read-Host "Pressione Enter para sair"
