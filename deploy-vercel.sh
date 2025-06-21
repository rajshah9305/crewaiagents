#!/bin/bash

# Vercel Deployment Helper Script
# This script helps you deploy the AI Agents Platform to Vercel

set -e

echo "🚀 Vercel Deployment Helper"
echo "============================"

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "🔧 Preparing for Vercel deployment..."

# Check if backend URL is provided
if [ -z "$1" ]; then
    echo "⚠️  No backend URL provided"
    echo "Usage: $0 <backend-url>"
    echo "Example: $0 https://your-backend.railway.app"
    echo ""
    echo "Please provide your backend URL (Railway, Render, Heroku, etc.)"
    read -p "Backend URL: " BACKEND_URL
else
    BACKEND_URL=$1
fi

# Convert HTTP to WSS for WebSocket
WS_URL=$(echo $BACKEND_URL | sed 's/http:/ws:/' | sed 's/https:/wss:/')

echo "📝 Setting up environment variables..."
echo "Backend URL: $BACKEND_URL"
echo "WebSocket URL: $WS_URL"

# Create .env.local for Vercel
cat > frontend/.env.local << EOF
REACT_APP_API_URL=$BACKEND_URL
REACT_APP_WS_URL=$WS_URL
EOF

echo "✅ Environment variables created in frontend/.env.local"

# Navigate to frontend directory
cd frontend

echo "🔍 Checking frontend setup..."
if [ ! -f "package.json" ]; then
    echo "❌ Error: package.json not found in frontend directory"
    exit 1
fi

echo "📦 Installing dependencies..."
npm install

echo "🏗️ Building frontend..."
npm run build

echo "🚀 Deploying to Vercel..."
echo ""
echo "📋 Deployment Steps:"
echo "1. Vercel will open in your browser"
echo "2. Sign in with your GitHub account"
echo "3. Import the repository: rajshah9305/crewaiagents"
echo "4. Configure the project:"
echo "   - Framework: Vite"
echo "   - Root Directory: frontend"
echo "   - Build Command: npm run build"
echo "   - Output Directory: build"
echo "5. Add environment variables:"
echo "   - REACT_APP_API_URL: $BACKEND_URL"
echo "   - REACT_APP_WS_URL: $WS_URL"
echo "6. Click Deploy"
echo ""

# Start Vercel deployment
vercel --prod

echo ""
echo "🎉 Deployment complete!"
echo "📱 Your app should be live at the URL provided by Vercel"
echo ""
echo "📋 Next steps:"
echo "1. Test your application"
echo "2. Set up a custom domain (optional)"
echo "3. Configure analytics and monitoring"
echo ""
echo "📚 For more information, see VERCEL_DEPLOYMENT.md" 