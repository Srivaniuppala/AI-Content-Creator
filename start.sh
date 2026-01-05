#!/bin/bash
# AI Content Creator - Quick Start Script
# Run this script to set up and start the application

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color
BG_BLUE='\033[44m'

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  AI Content Creator - Quick Start${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# Check if Docker is installed
echo -e "${YELLOW}[1/4] Checking Docker installation...${NC}"
if ! command -v docker &> /dev/null; then
    echo -e "${RED}[ERROR] Docker is not installed or not running!${NC}"
    echo -e "${RED}Please install Docker from: https://www.docker.com/get-docker/${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Docker found: $(docker --version)${NC}"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}[ERROR] Docker Compose is not available!${NC}"
    exit 1
fi
echo -e "${GREEN}[OK] Docker Compose found: $(docker-compose --version)${NC}"

echo ""

# Check if .env file exists
echo -e "${YELLOW}[2/4] Checking configuration...${NC}"
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}[INFO] .env file not found!${NC}"
    echo -e "${YELLOW}Creating .env from template...${NC}"
    cp ".env.example" ".env"
    echo -e "${GREEN}[OK] .env file created${NC}"
    echo ""
    echo -e "${YELLOW}[IMPORTANT] Please edit .env and add your Groq API key:${NC}"
    echo -e "${WHITE}  GROQ_API_KEY=your_api_key_here${NC}"
    echo ""
    echo -e "${CYAN}Get your free API key at: https://console.groq.com${NC}"
    echo ""
    read -p "Press Enter after adding your API key to .env, or type 'exit' to quit: " continue
    if [ "$continue" = "exit" ]; then
        exit 0
    fi
fi

# Check if API key is configured
if ! grep -q "GROQ_API_KEY=gsk_" ".env" && ! grep -qE "GROQ_API_KEY=.{30,}" ".env"; then
    echo -e "${YELLOW}[WARNING] Groq API key may not be configured in .env${NC}"
    echo -e "${YELLOW}The application may not work without a valid API key.${NC}"
    echo ""
fi

echo -e "${GREEN}[OK] Configuration ready${NC}"
echo ""

# Stop any existing containers
echo -e "${YELLOW}[3/4] Cleaning up old containers...${NC}"
docker-compose down > /dev/null 2>&1
echo -e "${GREEN}[OK] Cleanup complete${NC}"

echo ""

# Start services
echo -e "${YELLOW}[4/4] Starting services...${NC}"
echo -e "${CYAN}   - PostgreSQL Database${NC}"
echo -e "${CYAN}   - Streamlit Application${NC}"
echo ""

docker-compose up -d

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK] Services started successfully${NC}"
else
    echo -e "${RED}[ERROR] Failed to start services${NC}"
    echo -e "${YELLOW}Check logs with: docker-compose logs${NC}"
    exit 1
fi

echo ""

# Wait for services to be ready
echo -e "${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

max_retries=30
retry=0
all_healthy=false

while [ $retry -lt $max_retries ] && [ "$all_healthy" = false ]; do
    if docker-compose ps | grep -q "Up"; then
        unhealthy=$(docker-compose ps | grep -v "Up" | grep -v "NAME" | wc -l)
        if [ $unhealthy -eq 0 ]; then
            all_healthy=true
        else
            retry=$((retry + 1))
            echo -e "${GRAY}   Waiting for services... ($retry/$max_retries)${NC}"
            sleep 2
        fi
    else
        retry=$((retry + 1))
        echo -e "${GRAY}   Waiting for services... ($retry/$max_retries)${NC}"
        sleep 2
    fi
done

if [ "$all_healthy" = true ]; then
    echo -e "${GREEN}[OK] All services are healthy${NC}"
else
    echo -e "${YELLOW}[WARNING] Services started but may not be fully ready${NC}"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${CYAN}Application is running at:${NC}"
echo -e "${BG_BLUE}${WHITE}  http://localhost:8501${NC}"
echo ""
echo -e "${CYAN}Services:${NC}"
echo -e "${GRAY}  - Streamlit App:  http://localhost:8501${NC}"
echo -e "${GRAY}  - PostgreSQL:     localhost:5432${NC}"
echo ""
echo -e "${CYAN}Useful commands:${NC}"
echo -e "${GRAY}  - View logs:      docker-compose logs -f${NC}"
echo -e "${GRAY}  - Stop services:  docker-compose down${NC}"
echo -e "${GRAY}  - Restart:        docker-compose restart${NC}"
echo ""
echo -e "${YELLOW}Opening browser...${NC}"
sleep 2

# Try to open browser
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8501
elif command -v open &> /dev/null; then
    open http://localhost:8501
else
    echo -e "${YELLOW}Could not open browser automatically.${NC}"
    echo -e "${YELLOW}Please open http://localhost:8501 manually.${NC}"
fi

echo ""
echo -e "${GREEN}Happy creating!${NC}"
echo ""
