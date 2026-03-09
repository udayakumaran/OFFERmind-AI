#!/bin/bash
echo "Starting Backend API..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
echo "Backend running at http://localhost:8000"

echo "Starting Frontend..."
cd ../frontend
export NG_CLI_ANALYTICS=false
npm start &
FRONTEND_PID=$!
echo "Frontend running at http://localhost:4200"

echo "Press Ctrl+C to stop both servers."

trap "kill $BACKEND_PID $FRONTEND_PID" SIGINT

wait $BACKEND_PID $FRONTEND_PID
