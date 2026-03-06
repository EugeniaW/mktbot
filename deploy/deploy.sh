#!/bin/bash
# Deploy script for DigitalOcean Droplet
set -e

echo "🚀 Deploying Deep Research Bot to DigitalOcean..."

# Update system
echo "📦 Updating system..."
apt-get update && apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    usermod -aG docker $USER || true
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Create app directory
mkdir -p /opt/deep-research-bot
cd /opt/deep-research-bot

# Note: User needs to upload files or clone from git
echo "📁 Please ensure the following files are in /opt/deep-research-bot/:"
echo "  - src/bot.py"
echo "  - requirements.txt"
echo "  - Dockerfile"
echo "  - docker-compose.yml"
echo "  - .env (with API keys!)"
echo ""
echo "Then run: docker-compose up -d --build"
