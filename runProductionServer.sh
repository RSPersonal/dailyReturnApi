source env/bin/activate
cd core/
gunicorn -k uvicorn.workers.UvicornWorker main:app -b :8000
