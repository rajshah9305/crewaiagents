#!/bin/bash

# AI Agents Platform Deployment Script
# This script sets up and deploys the AI Agents Platform

set -e

echo "🚀 AI Agents Platform Deployment Script"
echo "========================================"

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    echo "❌ Unsupported operating system: $OSTYPE"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies based on OS
install_dependencies() {
    echo "📦 Installing system dependencies..."
    
    if [[ "$OS" == "linux" ]]; then
        if command_exists apt-get; then
            sudo apt-get update
            sudo apt-get install -y python3 python3-pip python3-venv nodejs npm postgresql postgresql-contrib redis-server curl
        elif command_exists yum; then
            sudo yum update -y
            sudo yum install -y python3 python3-pip nodejs npm postgresql postgresql-server redis curl
        else
            echo "❌ Unsupported package manager. Please install Python3, Node.js, PostgreSQL, and Redis manually."
            exit 1
        fi
    elif [[ "$OS" == "macos" ]]; then
        if ! command_exists brew; then
            echo "📦 Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python3 node postgresql redis
    fi
    
    echo "✅ System dependencies installed"
}

# Function to setup Python environment
setup_python() {
    echo "🐍 Setting up Python environment..."
    
    if [[ ! -d "venv" ]]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install --upgrade pip
    
    echo "✅ Python environment setup complete"
}

# Function to setup Node.js environment
setup_node() {
    echo "📦 Setting up Node.js environment..."
    
    npm install
    npm run setup:frontend
    
    echo "✅ Node.js environment setup complete"
}

# Function to setup database
setup_database() {
    echo "🗄️ Setting up database..."
    
    if [[ "$OS" == "linux" ]]; then
        sudo systemctl start postgresql
        sudo systemctl enable postgresql
    elif [[ "$OS" == "macos" ]]; then
        brew services start postgresql
    fi
    
    # Create database if it doesn't exist
    createdb ai_agents 2>/dev/null || echo "Database 'ai_agents' already exists"
    
    echo "✅ Database setup complete"
}

# Function to setup Redis
setup_redis() {
    echo "🔴 Setting up Redis..."
    
    if [[ "$OS" == "linux" ]]; then
        sudo systemctl start redis-server
        sudo systemctl enable redis-server
    elif [[ "$OS" == "macos" ]]; then
        brew services start redis
    fi
    
    echo "✅ Redis setup complete"
}

# Function to setup environment file
setup_env() {
    echo "⚙️ Setting up environment configuration..."
    
    if [[ ! -f ".env" ]]; then
        cp .env.example .env
        echo "📝 Please edit .env file with your API keys:"
        echo "   - CEREBRAS_API_KEY (get from https://cloud.cerebras.ai)"
        echo "   - OPENAI_API_KEY (optional, for additional tools)"
        echo "   - SERPER_API_KEY (optional, for web search)"
        echo "   - JWT_SECRET (change this in production)"
    else
        echo "✅ Environment file already exists"
    fi
}

# Function to install PM2
install_pm2() {
    echo "📦 Installing PM2..."
    
    if ! command_exists pm2; then
        npm install -g pm2
    fi
    
    echo "✅ PM2 installed"
}

# Function to build and deploy
deploy() {
    echo "🚀 Deploying application..."
    
    # Build frontend
    echo "🏗️ Building frontend..."
    npm run build
    
    # Start backend with PM2
    echo "🔄 Starting backend with PM2..."
    pm2 start ecosystem.config.js --env production
    
    echo "✅ Deployment complete!"
    echo ""
    echo "🎉 AI Agents Platform is now running!"
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 API Docs: http://localhost:8000/docs"
    echo ""
    echo "📋 Useful commands:"
    echo "   pm2 logs ai-agents-backend    # View backend logs"
    echo "   pm2 restart ai-agents-backend # Restart backend"
    echo "   pm2 stop ai-agents-backend    # Stop backend"
    echo "   make dev                      # Start development mode"
}

# Function to show help
show_help() {
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  setup     - Complete setup (dependencies, environment, database)"
    echo "  deploy    - Deploy the application"
    echo "  dev       - Start development mode"
    echo "  help      - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 setup   # First time setup"
    echo "  $0 deploy  # Deploy to production"
    echo "  $0 dev     # Start development servers"
}

# Main script logic
case "${1:-}" in
    "setup")
        install_dependencies
        setup_python
        setup_node
        setup_database
        setup_redis
        setup_env
        install_pm2
        echo ""
        echo "✅ Setup complete! Run '$0 deploy' to deploy the application"
        ;;
    "deploy")
        setup_env
        deploy
        ;;
    "dev")
        setup_env
        echo "🚀 Starting development servers..."
        npm run dev
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    "")
        echo "❌ No option specified"
        show_help
        exit 1
        ;;
    *)
        echo "❌ Unknown option: $1"
        show_help
        exit 1
        ;;
esac 