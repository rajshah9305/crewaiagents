# 🚀 Backend Deployment Guide

This guide will help you deploy the AI Agents Platform backend to various cloud platforms.

## 📋 Prerequisites

1. **API Keys**: Get your Cerebras API key from [cloud.cerebras.ai](https://cloud.cerebras.ai)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Database**: You'll need a PostgreSQL database (provided by most platforms)

## 🎯 Deployment Options

### Option 1: Railway (Recommended - Easiest)

**Railway** is the easiest option with automatic database provisioning.

#### Step 1: Sign Up
1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account
3. Create a new project

#### Step 2: Deploy Backend
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Navigate to backend directory
cd backend

# Initialize Railway project
railway init

# Deploy to Railway
railway up
```

#### Step 3: Configure Environment Variables
In Railway dashboard, add these environment variables:
```bash
CEREBRAS_API_KEY=your_cerebras_api_key_here
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
DATABASE_URL=postgresql://... (auto-provided by Railway)
REDIS_URL=redis://... (optional, Railway provides Redis)
BACKEND_CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
```

#### Step 4: Get Your Backend URL
Railway will provide you with a URL like: `https://your-app.railway.app`

### Option 2: Render (Free Tier Available)

**Render** offers a generous free tier for web services.

#### Step 1: Sign Up
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Create a new Web Service

#### Step 2: Connect Repository
1. Connect your GitHub repository: `rajshah9305/crewaiagents`
2. Configure the service:
   - **Name**: `ai-agents-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`

#### Step 3: Configure Environment Variables
Add these environment variables in Render:
```bash
CEREBRAS_API_KEY=your_cerebras_api_key_here
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
DATABASE_URL=postgresql://... (create PostgreSQL service in Render)
REDIS_URL=redis://... (optional)
BACKEND_CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
```

#### Step 4: Deploy
Click "Create Web Service" and wait for deployment.

### Option 3: Heroku (Paid)

**Heroku** is a reliable platform with good performance.

#### Step 1: Install Heroku CLI
```bash
# macOS
brew install heroku/brew/heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Deploy
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-ai-agents-backend

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Add Redis addon (optional)
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set CEREBRAS_API_KEY=your_cerebras_api_key_here
heroku config:set JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
heroku config:set OPENAI_API_KEY=your_openai_api_key_here
heroku config:set SERPER_API_KEY=your_serper_api_key_here
heroku config:set BACKEND_CORS_ORIGINS='["https://your-frontend-domain.vercel.app"]'

# Deploy
git push heroku main
```

### Option 4: DigitalOcean App Platform

**DigitalOcean** offers good performance and reasonable pricing.

#### Step 1: Create App
1. Go to [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Navigate to App Platform
3. Create a new app from GitHub repository

#### Step 2: Configure
- **Source**: GitHub repository
- **Branch**: `main`
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Run Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Step 3: Add Database
1. Add a PostgreSQL database component
2. Link it to your app
3. Set environment variables

## 🔧 Environment Variables

All platforms require these environment variables:

### Required
```bash
CEREBRAS_API_KEY=your_cerebras_api_key_here
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
```

### Optional
```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
DATABASE_URL=postgresql://... (auto-provided by most platforms)
REDIS_URL=redis://... (optional)
BACKEND_CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
```

## 🗄️ Database Setup

### Railway (Automatic)
Railway automatically provisions PostgreSQL and provides the `DATABASE_URL`.

### Render (Manual)
1. Create a PostgreSQL service in Render
2. Copy the connection string to your web service environment variables

### Heroku (Automatic)
Heroku automatically provisions PostgreSQL when you add the addon.

### Manual Database Setup
If you need to set up your own database:

```sql
-- Connect to your PostgreSQL database
\c your_database_name;

-- Run the initialization script
\i backend/init.sql;
```

## 🔍 Testing Your Deployment

Once deployed, test your backend:

```bash
# Health check
curl https://your-backend-url.com/health

# API documentation
# Visit: https://your-backend-url.com/docs

# Test an endpoint
curl https://your-backend-url.com/
```

## 🐛 Troubleshooting

### Common Issues

**Build Failures:**
```bash
# Check if all dependencies are in requirements.txt
# Ensure Python version is compatible (3.11+)
# Check for missing system dependencies
```

**Database Connection Issues:**
```bash
# Verify DATABASE_URL is correct
# Check if database is accessible
# Ensure database schema is created
```

**Environment Variables:**
```bash
# Verify all required env vars are set
# Check for typos in variable names
# Ensure values are properly quoted
```

**CORS Issues:**
```bash
# Update BACKEND_CORS_ORIGINS with your frontend domain
# Ensure the domain is properly formatted
```

## 📊 Monitoring

### Railway
- Built-in logs and metrics
- Automatic health checks
- Performance monitoring

### Render
- Request logs
- Build logs
- Performance metrics

### Heroku
- Application logs: `heroku logs --tail`
- Performance monitoring
- Addon monitoring

## 🔄 Continuous Deployment

All platforms support automatic deployments:

1. **Railway**: Automatically deploys on git push
2. **Render**: Automatically deploys on git push
3. **Heroku**: Automatically deploys on git push to heroku remote

## 💰 Cost Comparison

| Platform | Free Tier | Paid Plans | Database |
|----------|-----------|------------|----------|
| Railway | ❌ | $5/month | ✅ Included |
| Render | ✅ | $7/month | ✅ Included |
| Heroku | ❌ | $7/month | ✅ Addon |
| DigitalOcean | ❌ | $5/month | ✅ Addon |

## 🎯 Recommendation

**For beginners**: Use **Railway** - easiest setup, includes database
**For free tier**: Use **Render** - generous free tier
**For production**: Use **Railway** or **DigitalOcean** - good performance

## 📞 Support

- **Railway**: [railway.app/docs](https://railway.app/docs)
- **Render**: [render.com/docs](https://render.com/docs)
- **Heroku**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **DigitalOcean**: [docs.digitalocean.com](https://docs.digitalocean.com)

---

Once your backend is deployed, you can proceed with frontend deployment to Vercel! 🎉 