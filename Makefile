.PHONY: help setup dev build start stop restart logs test clean deploy db-setup migrate

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Setup development environment
	@echo "🔧 Setting up development environment..."
	cp .env.example .env
	@echo "📝 Please edit .env file with your API keys"
	@echo "🔑 Get Cerebras API key from: https://cloud.cerebras.ai"
	npm install
	npm run setup:backend
	npm run setup:frontend
	@echo "✅ Setup complete! Run 'make dev' to start development servers"

dev: ## Start development servers
	@echo "🚀 Starting development servers..."
	npm run dev

build: ## Build frontend for production
	@echo "🏗️ Building frontend..."
	npm run build

start: ## Start production servers with PM2
	@echo "🚀 Starting production servers..."
	npm run start

stop: ## Stop production servers
	@echo "🛑 Stopping production servers..."
	npm run stop

restart: ## Restart production servers
	@echo "🔄 Restarting production servers..."
	npm run restart

logs: ## Show PM2 logs
	npm run logs

test: ## Run all tests
	@echo "🧪 Running tests..."
	npm run test

clean: ## Clean up node_modules and build artifacts
	@echo "🧹 Cleaning up..."
	rm -rf frontend/node_modules
	rm -rf frontend/build
	rm -rf node_modules
	@echo "✅ Cleanup complete"

deploy: ## Deploy to production
	@echo "🚀 Deploying to production..."
	@echo "1. Building frontend..."
	npm run build
	@echo "2. Starting backend with PM2..."
	npm run start
	@echo "✅ Deployment complete!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

db-setup: ## Setup database
	@echo "🗄️ Setting up database..."
	npm run db:setup

migrate: ## Run database migrations
	@echo "🔄 Running database migrations..."
	npm run db:migrate

install-deps: ## Install system dependencies (Ubuntu/Debian)
	@echo "📦 Installing system dependencies..."
	sudo apt-get update
	sudo apt-get install -y python3 python3-pip python3-venv nodejs npm postgresql postgresql-contrib redis-server
	@echo "✅ System dependencies installed"

install-deps-mac: ## Install system dependencies (macOS)
	@echo "📦 Installing system dependencies..."
	brew install python3 node postgresql redis
	@echo "✅ System dependencies installed"

create-env: ## Create Python virtual environment
	@echo "🐍 Creating Python virtual environment..."
	python3 -m venv venv
	@echo "✅ Virtual environment created"
	@echo "💡 Activate with: source venv/bin/activate"

install-pm2: ## Install PM2 globally
	@echo "📦 Installing PM2..."
	npm install -g pm2
	@echo "✅ PM2 installed"

production-setup: ## Complete production setup
	@echo "🚀 Setting up production environment..."
	make install-deps
	make create-env
	make install-pm2
	make setup
	make db-setup
	make migrate
	@echo "✅ Production setup complete!"
	@echo "🎯 Run 'make deploy' to start the application" 