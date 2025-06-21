module.exports = {
  apps: [
    {
      name: 'ai-agents-backend',
      script: 'backend/app/main.py',
      interpreter: 'python3',
      cwd: './backend',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '1G',
      env: {
        NODE_ENV: 'development',
        DATABASE_URL: 'postgresql://postgres:password@localhost:5432/ai_agents',
        CEREBRAS_API_KEY: process.env.CEREBRAS_API_KEY,
        OPENAI_API_KEY: process.env.OPENAI_API_KEY,
        SERPER_API_KEY: process.env.SERPER_API_KEY,
        JWT_SECRET: process.env.JWT_SECRET || 'your-super-secret-jwt-key-change-this-in-production',
        REDIS_URL: 'redis://localhost:6379',
        BACKEND_CORS_ORIGINS: '["http://localhost:3000", "https://yourdomain.com"]'
      },
      env_production: {
        NODE_ENV: 'production',
        DATABASE_URL: process.env.DATABASE_URL,
        CEREBRAS_API_KEY: process.env.CEREBRAS_API_KEY,
        OPENAI_API_KEY: process.env.OPENAI_API_KEY,
        SERPER_API_KEY: process.env.SERPER_API_KEY,
        JWT_SECRET: process.env.JWT_SECRET,
        REDIS_URL: process.env.REDIS_URL,
        BACKEND_CORS_ORIGINS: process.env.BACKEND_CORS_ORIGINS
      }
    }
  ]
}; 