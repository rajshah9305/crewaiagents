# 🚀 Complete Deployment Steps

This guide provides step-by-step instructions to deploy the AI Agents Platform to production.

## 📋 Prerequisites

### Required Accounts
- [ ] GitHub account (for repository access)
- [ ] Cerebras API key from [cloud.cerebras.ai](https://cloud.cerebras.ai)
- [ ] Vercel account for frontend deployment
- [ ] Railway/Render/Heroku account for backend deployment

### Required Knowledge
- Basic command line usage
- Understanding of environment variables
- Basic Git operations

## 🎯 Deployment Strategy

We'll deploy using a **hybrid approach**:
- **Frontend**: Vercel (optimized for React apps)
- **Backend**: Railway/Render/Heroku (for Python APIs)
- **Database**: PostgreSQL (auto-provisioned by platform)
- **Caching**: Redis (optional, auto-provisioned)

## 📝 Step-by-Step Deployment

### Step 1: Prepare Your Environment

```bash
# 1. Clone the repository
git clone https://github.com/rajshah9305/crewaiagents.git
cd crewaiagents

# 2. Verify the structure
ls -la
# Should show: backend/, frontend/, deploy.sh, etc.

# 3. Check if you have the required tools
node --version  # Should be 18+
npm --version   # Should be 8+
python3 --version  # Should be 3.11+
```

### Step 2: Deploy Backend (Choose One Option)

#### Option A: Railway (Recommended - Easiest)

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login to Railway
railway login

# 3. Navigate to backend directory
cd backend

# 4. Initialize Railway project
railway init

# 5. Deploy to Railway
railway up

# 6. Get your deployment URL
railway status
# Note down the URL: https://your-app.railway.app
```

**Configure Environment Variables in Railway Dashboard:**
1. Go to [railway.app](https://railway.app)
2. Select your project
3. Go to "Variables" tab
4. Add these variables:
   ```
   CEREBRAS_API_KEY=your_cerebras_api_key_here
   JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
   OPENAI_API_KEY=your_openai_api_key_here (optional)
   SERPER_API_KEY=your_serper_api_key_here (optional)
   BACKEND_CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
   ```

#### Option B: Render (Free Tier)

1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New Web Service"
4. Connect repository: `rajshah9305/crewaiagents`
5. Configure:
   - **Name**: `ai-agents-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: `backend`
6. Add environment variables (same as Railway)
7. Click "Create Web Service"

#### Option C: Heroku (Paid)

```bash
# 1. Install Heroku CLI
brew install heroku/brew/heroku  # macOS
# or download from https://devcenter.heroku.com/articles/heroku-cli

# 2. Login to Heroku
heroku login

# 3. Create Heroku app
heroku create your-ai-agents-backend

# 4. Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# 5. Set environment variables
heroku config:set CEREBRAS_API_KEY=your_cerebras_api_key_here
heroku config:set JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
heroku config:set OPENAI_API_KEY=your_openai_api_key_here
heroku config:set SERPER_API_KEY=your_serper_api_key_here
heroku config:set BACKEND_CORS_ORIGINS='["https://your-frontend-domain.vercel.app"]'

# 6. Deploy
git push heroku main
```

### Step 3: Test Your Backend

```bash
# Test health endpoint
curl https://your-backend-url.com/health
# Should return: {"status": "healthy", "service": "ai-agents-platform"}

# Test API documentation
# Visit: https://your-backend-url.com/docs
# Should show FastAPI documentation

# Test root endpoint
curl https://your-backend-url.com/
# Should return API information
```

### Step 4: Deploy Frontend to Vercel

#### Option A: Using the Helper Script (Recommended)

```bash
# 1. Go back to project root
cd ..

# 2. Run the deployment script with your backend URL
./deploy-vercel.sh https://your-backend-url.com

# 3. Follow the prompts in your browser
# - Sign in to Vercel with GitHub
# - Import repository: rajshah9305/crewaiagents
# - Configure project settings
# - Add environment variables
# - Deploy
```

#### Option B: Manual Vercel Deployment

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Import GitHub repository: `rajshah9305/crewaiagents`
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`
5. Add environment variables:
   ```
   REACT_APP_API_URL=https://your-backend-url.com
   REACT_APP_WS_URL=wss://your-backend-url.com
   ```
6. Click "Deploy"

### Step 5: Configure CORS (Important!)

After deploying frontend, update your backend CORS settings:

1. Go to your backend platform dashboard
2. Update `BACKEND_CORS_ORIGINS` environment variable:
   ```
   BACKEND_CORS_ORIGINS=["https://your-frontend.vercel.app"]
   ```
3. Redeploy backend if necessary

### Step 6: Test Complete Application

```bash
# 1. Test frontend
# Visit: https://your-frontend.vercel.app
# Should show the AI Agents Platform landing page

# 2. Test API connection
# Open browser dev tools
# Check for any CORS errors in console

# 3. Test backend endpoints
curl https://your-backend-url.com/health
curl https://your-backend-url.com/docs
```

## 🔧 Environment Variables Reference

### Backend Variables (Required)
```bash
CEREBRAS_API_KEY=your_cerebras_api_key_here
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
```

### Backend Variables (Optional)
```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
DATABASE_URL=postgresql://... (auto-provided)
REDIS_URL=redis://... (auto-provided)
BACKEND_CORS_ORIGINS=["https://your-frontend-domain.vercel.app"]
```

### Frontend Variables (Required)
```bash
REACT_APP_API_URL=https://your-backend-url.com
REACT_APP_WS_URL=wss://your-backend-url.com
```

## 🐛 Troubleshooting Common Issues

### Backend Issues

**Build Failures:**
```bash
# Check Python version compatibility
python3 --version  # Should be 3.11+

# Check requirements.txt
cat backend/requirements.txt

# Check platform logs
# Railway: railway logs
# Render: View logs in dashboard
# Heroku: heroku logs --tail
```

**Database Connection:**
```bash
# Check if DATABASE_URL is set
# Most platforms auto-provide this

# Test database connection
# Check platform dashboard for database status
```

**CORS Errors:**
```bash
# Update BACKEND_CORS_ORIGINS with exact frontend domain
# Include protocol: https://your-domain.vercel.app
# Not just: your-domain.vercel.app
```

### Frontend Issues

**Build Failures:**
```bash
# Check Node.js version
node --version  # Should be 18+

# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**API Connection:**
```bash
# Verify environment variables in Vercel
# Check REACT_APP_API_URL is correct
# Check REACT_APP_WS_URL is correct

# Test API endpoint directly
curl https://your-backend-url.com/health
```

**Environment Variables Not Loading:**
```bash
# Vercel requires REACT_APP_ prefix
# Variables must be set in Vercel dashboard
# Not in .env files (for production)
```

## 📊 Post-Deployment Checklist

- [ ] Backend health check passes
- [ ] Frontend loads without errors
- [ ] API documentation accessible
- [ ] CORS errors resolved
- [ ] Environment variables configured
- [ ] SSL certificates active
- [ ] Custom domain configured (optional)
- [ ] Monitoring set up
- [ ] Error tracking configured

## 🔄 Continuous Deployment

### Automatic Deployments
- **Vercel**: Automatically deploys on git push to main branch
- **Railway**: Automatically deploys on git push to main branch
- **Render**: Automatically deploys on git push to main branch
- **Heroku**: Deploys on git push to heroku remote

### Manual Deployments
```bash
# Update code
git add .
git commit -m "Update application"
git push origin main

# Frontend automatically deploys to Vercel
# Backend automatically deploys to chosen platform
```

## 📈 Monitoring and Maintenance

### Health Checks
```bash
# Backend health
curl https://your-backend-url.com/health

# Frontend status
# Check Vercel dashboard for build status
```

### Logs
```bash
# Railway logs
railway logs

# Render logs
# View in dashboard

# Heroku logs
heroku logs --tail

# Vercel logs
# View in Vercel dashboard
```

### Performance Monitoring
- **Vercel Analytics**: Built-in performance monitoring
- **Platform Metrics**: Check your backend platform dashboard
- **Error Tracking**: Set up Sentry or similar service

## 🎉 Success!

Your AI Agents Platform is now deployed and ready for production use!

### Your URLs
- **Frontend**: https://your-app.vercel.app
- **Backend API**: https://your-backend-url.com
- **API Docs**: https://your-backend-url.com/docs

### Next Steps
1. Set up custom domain (optional)
2. Configure monitoring and alerts
3. Set up backup strategies
4. Plan for scaling
5. Document your deployment for team members

## 📞 Support

- **Project Issues**: [GitHub Issues](https://github.com/rajshah9305/crewaiagents/issues)
- **Railway**: [railway.app/docs](https://railway.app/docs)
- **Render**: [render.com/docs](https://render.com/docs)
- **Heroku**: [devcenter.heroku.com](https://devcenter.heroku.com)
- **Vercel**: [vercel.com/docs](https://vercel.com/docs)

---

**Happy Deploying! 🚀** 