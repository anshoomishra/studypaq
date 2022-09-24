#!/bin/bash

RUN_PORT  = ${PORT:-8000}

/usr/local/bin/gunicorn --worker-temp-dir /dev/shm -k uvicorn.workers.UvicornWorker app.main:app --reload --bind "0.0.0.0:${RUN_PORT}"