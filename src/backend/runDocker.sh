#!/bin/sh

uvicorn appDocker:app --host 0.0.0.0 --port 3012 &

sleep 150

python populateWeaviate.py

wait
