PORT="${PORT:-8080}"
uvicorn open_webui.main:app --port $PORT --host 0.0.0.0 --forwarded-allow-ips '*' --reload
export CORS_ALLOW_ORIGIN="http://localhost:5173;http://localhost:8080;http://10.204.16.67:5173"