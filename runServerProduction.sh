#!/usr/bin/env bash
cd core/ || exit
gunicorn -k uvicorn.workers.UvicornWorker main:app -b :8000
