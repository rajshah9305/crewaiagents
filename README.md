# 🤖 AI Agents Platform

A production-ready full-stack platform for managing teams of AI agents powered by Cerebras ultra-fast inference and CrewAI framework.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
# 1. Clone the repository
git clone https://github.com/rajshah9305/crewaiagents.git
cd crewaiagents

# 2. Run automated setup
./deploy.sh setup

# 3. Edit environment variables
nano .env

# 4. Deploy to production
./deploy.sh deploy

# ✅ Access at http://localhost:3000
```

### Option 2: Manual Setup
```bash
# 1. Clone the repository
git clone https://github.com/rajshah9305/crewaiagents.git
cd crewaiagents

# 2. Setup environment
cp .env.example .env
# Edit .env with your API keys

# 3. Install dependencies
npm install
npm run setup:backend
npm run setup:frontend

# 4. Setup database
createdb ai_agents
npm run db:migrate

# 5. Start development servers
npm run dev

# ✅ Access at http://localhost:3000
```

## 🎯 Features

- ⚡ **Ultra-fast AI**: Cerebras integration (1000+ tokens/second)
- 🤖 **Agent Management**: Create, configure, and manage AI agents
- 👥 **Team Collaboration**: Build teams of agents for complex workflows
- 💬 **Real-time Chat**: WebSocket-powered chat interface
- 📊 **Analytics Dashboard**: Performance monitoring and insights
- 🔒 **Enterprise Security**: JWT auth, rate limiting, audit logs
- 🎨 **Modern UI**: React + TypeScript + Tailwind CSS
- 🚀 **Production Ready**: PM2 process management, nginx proxy

## 📁 Project Structure

```
ai-agents-platform/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration & database
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── requirements.txt    # Python dependencies
│   └── main.py            # FastAPI application
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API services
│   │   └── types/         # TypeScript types
│   ├── package.json       # Node.js dependencies
│   └── vite.config.ts     # Vite configuration
├── nginx/                  # Production proxy configuration
├── ecosystem.config.js     # PM2 configuration
├── deploy.sh              # Deployment script
├── package.json           # Root package.json
└── .env.example           # Environment template
```

## 🔑 Required API Keys

- **Cerebras API Key**: Get from [cloud.cerebras.ai](https://cloud.cerebras.ai)
- **OpenAI API Key**: For additional tools (optional)
- **Serper API Key**: For web search capabilities

## 🛠️ Development Commands

```bash
# Development
npm run dev              # Start both frontend and backend
npm run dev:backend      # Start backend only
npm run dev:frontend     # Start frontend only

# Production
npm run build            # Build frontend
npm run start            # Start with PM2
npm run stop             # Stop PM2 processes
npm run restart          # Restart PM2 processes
npm run logs             # View PM2 logs

# Database
npm run db:setup         # Setup database
npm run db:migrate       # Run migrations

# Testing
npm run test             # Run all tests
npm run test:backend     # Run backend tests
npm run test:frontend    # Run frontend tests

# Linting
npm run lint             # Run all linters
npm run lint:backend     # Run backend linters
npm run lint:frontend    # Run frontend linters
```

## 🚀 Production Deployment

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL
- Redis
- nginx (optional, for production)

### Deployment Steps
```bash
# 1. Setup production environment
./deploy.sh setup

# 2. Configure environment variables
nano .env

# 3. Deploy application
./deploy.sh deploy

# 4. Setup nginx (optional)
sudo cp nginx/nginx.conf /etc/nginx/nginx.conf
sudo systemctl restart nginx
```

### PM2 Management
```bash
# View running processes
pm2 list

# View logs
pm2 logs ai-agents-backend

# Restart application
pm2 restart ai-agents-backend

# Stop application
pm2 stop ai-agents-backend

# Monitor resources
pm2 monit
```

## 📖 Documentation

- [API Documentation](http://localhost:8000/docs)
- [Development Guide](docs/development.md)
- [Deployment Guide](docs/deployment.md)

## 🔧 System Requirements

### Development
- **OS**: macOS, Linux, Windows (WSL)
- **Python**: 3.11+
- **Node.js**: 18+
- **Memory**: 4GB RAM
- **Storage**: 2GB free space

### Production
- **OS**: Ubuntu 20.04+, CentOS 8+, macOS
- **Python**: 3.11+
- **Node.js**: 18+
- **PostgreSQL**: 13+
- **Redis**: 6+
- **Memory**: 8GB RAM (recommended)
- **Storage**: 10GB free space

## 🐛 Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check if dependencies are installed
cd backend && pip install -r requirements.txt

# Check if database is running
sudo systemctl status postgresql

# Check logs
pm2 logs ai-agents-backend
```

**Frontend build fails:**
```bash
# Clear node_modules and reinstall
cd frontend && rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18+
```

**Database connection issues:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Create database if it doesn't exist
createdb ai_agents

# Run migrations
npm run db:migrate
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/rajshah9305/crewaiagents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rajshah9305/crewaiagents/discussions)
- **Email**: support@yourdomain.com

---

Built with ❤️ combining FastAPI, React, CrewAI, and Cerebras technologies. 