#!/bin/bash
set -e

echo "=== Smoke Test: Agentic Legal Assistant ==="

# Start backend in background
cd src/backend
uvicorn app:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
cd ../..

# Wait for backend to start
sleep 5

# Test backend health
curl -f http://127.0.0.1:8000/api/health

# Kill backend
kill $BACKEND_PID

echo "=== Smoke Test Passed ==="