#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}   FileFlow Application Startup${NC}"
echo -e "${BLUE}=====================================${NC}"
echo

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check for --fastapi flag
USE_FASTAPI=false
for arg in "$@"; do
    case $arg in
        --fastapi)
            USE_FASTAPI=true
            shift
            ;;
    esac
done

# Create user_files directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/user_files"

if [ "$USE_FASTAPI" = true ]; then
    echo -e "${YELLOW}Using FastAPI backend${NC}"
    echo
    
    # Activate virtual environment
    if [ -d "$SCRIPT_DIR/backend_fastapi/venv" ]; then
        source "$SCRIPT_DIR/backend_fastapi/venv/bin/activate"
    else
        echo -e "${YELLOW}Creating virtual environment...${NC}"
        python3 -m venv "$SCRIPT_DIR/backend_fastapi/venv"
        source "$SCRIPT_DIR/backend_fastapi/venv/bin/activate"
        pip install -r "$SCRIPT_DIR/backend_fastapi/requirements.txt"
    fi
    
    echo -e "${GREEN}Starting FastAPI backend on port 5000...${NC}"
    cd "$SCRIPT_DIR/backend_fastapi"
    uvicorn main:app --host 0.0.0.0 --port 5000 --reload &
    BACKEND_PID=$!
else
    echo -e "${YELLOW}Using Flask backend (default)${NC}"
    echo -e "${YELLOW}Use --fastapi flag for FastAPI backend${NC}"
    echo
    
    # Check if database is initialized
    if [ ! -f "$SCRIPT_DIR/backend/instance/fileflow.db" ]; then
        echo -e "${GREEN}Initializing database...${NC}"
        cd "$SCRIPT_DIR"
        export FLASK_APP=backend.app
        flask init-db
    fi
    
    echo -e "${GREEN}Starting Flask backend on port 5000...${NC}"
    cd "$SCRIPT_DIR"
    export FLASK_APP=backend.app
    export FLASK_ENV=development
    flask run --host=0.0.0.0 --port=5000 &
    BACKEND_PID=$!
fi

echo -e "${GREEN}Backend started with PID: $BACKEND_PID${NC}"
echo

# Wait a moment for backend to start
sleep 2

echo -e "${GREEN}Starting React frontend on port 3000...${NC}"
cd "$SCRIPT_DIR/frontend"
npm start &
FRONTEND_PID=$!

echo -e "${GREEN}Frontend started with PID: $FRONTEND_PID${NC}"
echo

echo -e "${BLUE}=====================================${NC}"
echo -e "${BLUE}   Application is starting up!${NC}"
echo -e "${BLUE}=====================================${NC}"
echo -e "Backend:  ${GREEN}http://localhost:5000${NC}"
echo -e "Frontend: ${GREEN}http://localhost:3000${NC}"
if [ "$USE_FASTAPI" = true ]; then
    echo -e "API Docs: ${GREEN}http://localhost:5000/api/docs${NC}"
fi
echo
echo "Press Ctrl+C to stop both servers"
echo

# Trap Ctrl+C to kill both processes
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
