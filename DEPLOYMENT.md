# Deployment Guide - BENYAMIN BATAU JOURNAL APP

Panduan lengkap untuk deploy aplikasi ke berbagai platform.

## 📋 Pre-requisites

- Python 3.8+
- Git
- Account di platform hosting (Heroku, Railway, atau DigitalOcean)
- API Keys (Anthropic dan/atau OpenAI) - opsional

## 🚀 Deployment Options

### Option 1: Heroku

#### 1. Install Heroku CLI
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download dari: https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Login ke Heroku
```bash
heroku login
```

#### 3. Create Heroku App
```bash
cd benyamin_journal_app
heroku create benyamin-journal-app

# Atau gunakan nama custom
heroku create your-app-name
```

#### 4. Set Environment Variables
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set ANTHROPIC_API_KEY="your-anthropic-key"
heroku config:set OPENAI_API_KEY="your-openai-key"
heroku config:set FLASK_ENV="production"
```

#### 5. Deploy
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

#### 6. Open App
```bash
heroku open
```

#### 7. View Logs
```bash
heroku logs --tail
```

---

### Option 2: Railway.app

#### 1. Install Railway CLI
```bash
npm install -g @railway/cli

# Atau gunakan web interface: https://railway.app
```

#### 2. Login
```bash
railway login
```

#### 3. Initialize Project
```bash
cd benyamin_journal_app
railway init
```

#### 4. Deploy
```bash
railway up
```

#### 5. Set Environment Variables
Go to Railway dashboard → Your project → Variables → Add:
- `SECRET_KEY`
- `ANTHROPIC_API_KEY`
- `OPENAI_API_KEY`
- `FLASK_ENV=production`

#### 6. Generate Domain
```bash
railway domain
```

---

### Option 3: DigitalOcean App Platform

#### 1. Connect Repository
- Login ke DigitalOcean
- Go to Apps → Create App
- Connect GitHub repository

#### 2. Configure App
```yaml
name: benyamin-journal-app
services:
- name: web
  github:
    repo: your-username/benyamin-journal-app
    branch: main
  run_command: gunicorn app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: SECRET_KEY
    value: your-secret-key
  - key: ANTHROPIC_API_KEY
    value: your-anthropic-key
  - key: OPENAI_API_KEY
    value: your-openai-key
  - key: FLASK_ENV
    value: production
```

#### 3. Deploy
- Click "Create Resources"
- Wait for build to complete
- Access your app URL

---

### Option 4: VPS (Ubuntu Server)

#### 1. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Install Dependencies
```bash
# Python
sudo apt install python3 python3-pip python3-venv -y

# Nginx
sudo apt install nginx -y

# Supervisor (untuk process management)
sudo apt install supervisor -y
```

#### 3. Clone Repository
```bash
cd /var/www
sudo git clone https://github.com/your-username/benyamin-journal-app.git
cd benyamin-journal-app
```

#### 4. Setup Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 5. Create .env File
```bash
sudo nano .env
```

Add environment variables:
```env
SECRET_KEY=your-secret-key
ANTHROPIC_API_KEY=your-key
OPENAI_API_KEY=your-key
FLASK_ENV=production
```

#### 6. Configure Gunicorn
Create `/etc/supervisor/conf.d/journal-app.conf`:
```ini
[program:journal-app]
directory=/var/www/benyamin-journal-app
command=/var/www/benyamin-journal-app/venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
user=www-data
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/journal-app/err.log
stdout_logfile=/var/log/journal-app/out.log
```

#### 7. Configure Nginx
Create `/etc/nginx/sites-available/journal-app`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        client_max_body_size 50M;
    }

    location /static {
        alias /var/www/benyamin-journal-app/static;
    }
}
```

#### 8. Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/journal-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 9. Start Application
```bash
sudo mkdir -p /var/log/journal-app
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start journal-app
```

#### 10. Setup SSL (Optional but Recommended)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## 🔐 Security Best Practices

### 1. Environment Variables
❌ Never commit .env file to Git
✅ Use platform-specific secrets management
✅ Rotate API keys regularly

### 2. File Upload
✅ Validate file types
✅ Limit file sizes
✅ Scan for malware (if possible)
✅ Use temporary storage

### 3. HTTPS
✅ Always use SSL/TLS in production
✅ Redirect HTTP to HTTPS
✅ Use secure cookies

### 4. Rate Limiting
```python
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

### 5. CORS
```python
CORS(app, resources={
    r"/*": {
        "origins": ["https://your-domain.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

---

## 📊 Monitoring

### Heroku
```bash
heroku logs --tail
heroku ps
heroku addons:create papertrail
```

### Railway
- View logs in Railway dashboard
- Enable Datadog integration

### VPS
```bash
# Check application status
sudo supervisorctl status journal-app

# View logs
tail -f /var/log/journal-app/out.log
tail -f /var/log/journal-app/err.log

# Nginx logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 🔄 Updates & Maintenance

### Heroku
```bash
git pull origin main
git push heroku main
```

### Railway
```bash
railway up
```

### VPS
```bash
cd /var/www/benyamin-journal-app
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl restart journal-app
```

---

## 🆘 Troubleshooting

### Application won't start
1. Check logs
2. Verify environment variables
3. Ensure all dependencies installed
4. Check Python version

### File upload fails
1. Check MAX_FILE_SIZE setting
2. Verify disk space
3. Check folder permissions

### AI features not working
1. Verify API keys are set
2. Check API quota/limits
3. Test with AI disabled

### Slow performance
1. Increase gunicorn workers
2. Upgrade server resources
3. Implement caching
4. Optimize file processing

---

## 📞 Support

If you encounter issues:
- 📧 Email: benyamin.batau@example.com
- 🐛 GitHub Issues: https://github.com/benyaminbatau/journal-app/issues

---

**Made with ❤️ by Benyamin Batau**
