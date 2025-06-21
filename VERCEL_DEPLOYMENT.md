# 🚀 Vercel Deployment Guide

This guide will help you deploy the AI Agents Platform frontend to Vercel.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Backend API**: You'll need a deployed backend API (Railway, Render, or similar)

## 🎯 Deployment Options

### Option 1: Deploy Frontend Only (Recommended)

Since Vercel is optimized for frontend applications, we recommend deploying only the frontend to Vercel and hosting the backend separately.

#### Step 1: Deploy Backend First

Choose one of these platforms for your backend:

**Railway (Recommended)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Deploy backend
cd backend
railway init
railway up
```

**Render**
- Go to [render.com](https://render.com)
- Connect your GitHub repository
- Create a new Web Service
- Set build command: `pip install -r requirements.txt`
- Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Heroku**
```bash
# Install Heroku CLI
# Create Procfile in backend/
echo "web: uvicorn app.main:app --host 0.0.0.0 --port \$PORT" > backend/Procfile

# Deploy
heroku create your-app-name
heroku config:set CEREBRAS_API_KEY=your_key
git push heroku main
```

#### Step 2: Deploy Frontend to Vercel

1. **Connect Repository**
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository: `rajshah9305/crewaiagents`

2. **Configure Project**
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
   - **Install Command**: `npm install`

3. **Environment Variables**
   Add these environment variables in Vercel:
   ```
   REACT_APP_API_URL=https://your-backend-url.com
   REACT_APP_WS_URL=wss://your-backend-url.com
   ```

4. **Deploy**
   - Click "Deploy"
   - Wait for build to complete
   - Your app will be live at `https://your-app.vercel.app`

### Option 2: Full-Stack Deployment (Advanced)

For a full-stack deployment on Vercel, you can use Vercel Functions for the API:

1. **Create API Routes**
   ```bash
   # Create api directory in frontend
   mkdir -p frontend/api
   ```

2. **Move Backend Code**
   - Copy backend files to `frontend/api/`
   - Update imports and paths
   - Create serverless functions

3. **Update vercel.json**
   ```json
   {
     "functions": {
       "api/**/*.py": {
         "runtime": "python3.11"
       }
     }
   }
   ```

## 🔧 Configuration

### Environment Variables

Set these in your Vercel project settings:

```bash
# Required
CEREBRAS_API_KEY=your_cerebras_api_key
JWT_SECRET=your_jwt_secret

# Optional
OPENAI_API_KEY=your_openai_api_key
SERPER_API_KEY=your_serper_api_key
DATABASE_URL=your_database_url
REDIS_URL=your_redis_url
```

### Custom Domain (Optional)

1. Go to your Vercel project settings
2. Click "Domains"
3. Add your custom domain
4. Update DNS records as instructed

## 📱 Frontend Configuration

The frontend is configured to work with external APIs:

```typescript
// src/config/api.ts
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
export const WS_BASE_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';
```

## 🔄 Continuous Deployment

Vercel automatically deploys when you push to your main branch:

```bash
# Make changes
git add .
git commit -m "Update frontend"
git push origin main

# Vercel automatically deploys
```

## 📊 Monitoring

- **Vercel Analytics**: Built-in performance monitoring
- **Vercel Speed Insights**: Core Web Vitals tracking
- **Function Logs**: View API function logs in Vercel dashboard

## 🐛 Troubleshooting

### Build Failures

**Common Issues:**
```bash
# Node version mismatch
# Solution: Add .nvmrc file
echo "18" > frontend/.nvmrc

# Missing dependencies
# Solution: Check package.json and install missing packages

# TypeScript errors
# Solution: Fix type errors or add @ts-ignore comments
```

### API Connection Issues

**CORS Errors:**
- Ensure your backend allows requests from your Vercel domain
- Update CORS settings in backend

**Environment Variables:**
- Check that all required env vars are set in Vercel
- Verify API URLs are correct

### Performance Issues

**Optimizations:**
```bash
# Enable Vercel Edge Functions for better performance
# Add to vercel.json
{
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.11",
      "maxDuration": 30
    }
  }
}
```

## 🚀 Production Checklist

- [ ] Backend deployed and accessible
- [ ] Environment variables configured
- [ ] Custom domain set up (optional)
- [ ] SSL certificate active
- [ ] Performance monitoring enabled
- [ ] Error tracking configured
- [ ] Analytics set up

## 📞 Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Community**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Project Issues**: [github.com/rajshah9305/crewaiagents/issues](https://github.com/rajshah9305/crewaiagents/issues)

---

Your AI Agents Platform is now ready for production deployment on Vercel! 🎉 