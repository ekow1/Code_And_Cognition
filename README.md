# FastAPI MongoDB Application - EC2 Deployment

A modern FastAPI application with MongoDB integration, optimized for deployment on EC2 Ubuntu instances.

## 🚀 Features

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database with Motor async driver
- **JWT Authentication** - Secure token-based authentication
- **Docker** - Containerized deployment
- **Nginx** - Reverse proxy with SSL termination
- **GitHub Actions** - Automated CI/CD pipeline
- **Health Monitoring** - Built-in health checks

## 📋 Prerequisites

- EC2 Ubuntu instance
- Docker & Docker Compose installed on EC2
- GitHub repository with secrets configured
- MongoDB (local or Atlas)
- Domain name (optional, for SSL)

## 🛠️ EC2 Setup

### 1. Install Docker on EC2 Ubuntu

```bash
# Update system
sudo apt update

# Install required packages
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
```

### 2. Clone Repository

```bash
# Create application directory
sudo mkdir -p /opt/fastapi-app
sudo chown $USER:$USER /opt/fastapi-app
cd /opt/fastapi-app

# Clone your repository
git clone https://github.com/yourusername/your-repo.git .
```

### 3. Configure Environment

```bash
# Copy environment template
cp env.example .env

# Edit environment variables
nano .env
```

### 4. Setup SSL (Optional)

```bash
# Create SSL directory
mkdir -p nginx/ssl

# Generate self-signed certificate (for testing)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=your-domain.com"

# For production, use Let's Encrypt or your SSL provider
```

## 🔧 GitHub Secrets Configuration

Add these secrets to your GitHub repository:

- `EC2_HOST` - Your EC2 public IP or domain
- `EC2_USERNAME` - Ubuntu username (usually `ubuntu`)
- `EC2_SSH_KEY` - Your private SSH key for EC2 access

## 🚀 Deployment

### Automatic Deployment (GitHub Actions)

1. Push to `main` or `master` branch
2. GitHub Actions will automatically:
   - Run tests
   - Build Docker image
   - Push to GitHub Container Registry
   - Deploy to EC2

### Manual Deployment

```bash
# On EC2 instance
cd /opt/fastapi-app

# Pull latest changes
git pull origin main

# Build and start containers
docker-compose up -d --build

# Check status
docker-compose ps
docker-compose logs -f
```

## 📊 Monitoring

### Health Checks

- **Health**: `GET /health` - Overall application health
- **Readiness**: `GET /ready` - Deployment verification

### Logs

```bash
# Application logs
docker-compose logs -f app

# Nginx logs
docker-compose logs -f nginx

# All logs
docker-compose logs -f
```

### Status Commands

```bash
# Check container status
docker-compose ps

# Check resource usage
docker stats

# Check disk space
df -h

# Check memory usage
free -h
```

## 🔒 Security

### Firewall Configuration

```bash
# Allow SSH
sudo ufw allow ssh

# Allow HTTP and HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Enable firewall
sudo ufw enable
```

### SSL Configuration

For production SSL certificates:

1. **Let's Encrypt** (recommended):
   ```bash
   sudo apt install certbot
   sudo certbot certonly --standalone -d your-domain.com
   ```

2. **Update Nginx configuration** to use Let's Encrypt certificates:
   ```nginx
   ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
   ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
   ```

## 🛠️ Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check logs
docker-compose logs app

# Check environment variables
docker-compose config

# Verify Dockerfile
docker build --no-cache .
```

#### Database Connection Issues
```bash
# Test MongoDB connection
docker exec -it fastapi-app python -c "from app.db.mongo_db import client; print(client)"

# Check network connectivity
docker network ls
docker network inspect mongdb_app-network
```

#### SSL Issues
```bash
# Check SSL certificate
openssl x509 -in nginx/ssl/cert.pem -text -noout

# Test SSL connection
curl -k https://your-domain.com/health
```

### Debug Commands

```bash
# Enter container
docker exec -it fastapi-app bash

# Check processes
docker exec fastapi-app ps aux

# View environment variables
docker exec fastapi-app env

# Test API endpoints
curl http://localhost:8000/health
curl https://your-domain.com/health
```

## 📈 Scaling

### Horizontal Scaling

```bash
# Scale application containers
docker-compose up -d --scale app=3

# Use load balancer for multiple instances
```

### Vertical Scaling

```bash
# Update resource limits in docker-compose.yml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
```

## 🔄 Updates

### Application Updates

1. **Automatic**: Push to main branch (GitHub Actions)
2. **Manual**: 
   ```bash
   cd /opt/fastapi-app
   git pull origin main
   docker-compose up -d --build
   ```

### System Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io
```

## 📚 API Documentation

- **Swagger UI**: `https://your-domain.com/docs`
- **ReDoc**: `https://your-domain.com/redoc`
- **Health Check**: `https://your-domain.com/health`

## 🤝 Support

For issues and questions:

1. Check the troubleshooting section
2. Review application logs
3. Verify configuration
4. Create an issue in the repository

## 📄 License

This project is licensed under the MIT License.
