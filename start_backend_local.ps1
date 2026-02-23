Set-Location 'c:\Users\Sueli\Desktop\ClientFlow'
$env:DATABASE_URL='sqlite:///./clientflow.db'
$env:RUN_MIGRATIONS_ON_STARTUP='false'
$env:ENVIRONMENT='development'
$env:ALLOWED_ORIGINS='http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000'
$env:JWT_SECRET_KEY='dev-local-key'
.\.venv313\Scripts\python.exe -m uvicorn backend.main:app --host 0.0.0.0 --port 8001
