# Medical Chatbot - Deployment Guide

Complete guide for deploying the Medical Chatbot application to your production server.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Manual Deployment](#manual-deployment)
3. [Automated Deployment (GitHub Actions)](#automated-deployment)
4. [Post-Deployment](#post-deployment)
5. [Rollback](#rollback)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites

**On Your Local Machine:**
- Git
- SSH access to server
- Python 3.11+

**On Your Server:**
- Python 3.11+
- ChromaDB running on port 8000
- Ollama running on port 11434
- Sufficient permissions (sudo or proper user permissions)

**Server Details:**
- IP: `38.137.54.223`
- User: `krishan`
- Directory: `/home/krishan/projects/Medicalchatbot`

---

## 🔧 Manual Deployment

### Option 1: Using Deployment Script (Recommended)

**Step 1: Make script executable**
```bash
cd C:\AI_projects\Cosmos_project\Medical_chat_bots
chmod +x deploy.sh  # On Git Bash or WSL
```

**Step 2: Run deployment**
```bash
./deploy.sh krishan@38.137.54.223 main
```

The script will:
- ✅ Check Python syntax
- ✅ Create backup on server
- ✅ Upload all files
- ✅ Install dependencies
- ✅ Fix permissions
- ✅ Restart application
- ✅ Verify deployment

### Option 2: Manual Steps

**Step 1: Upload Files**
```bash
cd C:\AI_projects\Cosmos_project\Medical_chat_bots

# Upload Python files
scp main.py app.py config.py requirements.txt krishan@38.137.54.223:/home/krishan/projects/Medicalchatbot/

# Upload directories
scp -r chat_functions Embedding_fuctions database Excel_chat_bot krishan@38.137.54.223:/home/krishan/projects/Medicalchatbot/

# Upload utility scripts
scp fix_permissions.sh fix_dirs.py FIX_CHROMADB_PERMISSIONS.sh krishan@38.137.54.223:/home/krishan/projects/Medicalchatbot/
```

**Step 2: Setup on Server**
```bash
ssh krishan@38.137.54.223

cd /home/krishan/projects/Medicalchatbot

# Install dependencies
pip install -r requirements.txt

# Fix permissions
chmod +x *.sh
./fix_permissions.sh
python fix_dirs.py

# Restart application
pkill -f "python main.py"
nohup python main.py > app.log 2>&1 &

# Verify
ps aux | grep "python main.py"
tail -f app.log
```

**Step 3: Test**
```bash
curl http://localhost:5001/docs
```

---

## 🤖 Automated Deployment (GitHub Actions)

### Setup (One-Time)

**Step 1: Generate SSH Key Pair**

On your **local machine**:
```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f github_deploy_key
# This creates:
# - github_deploy_key (private key)
# - github_deploy_key.pub (public key)
```

**Step 2: Add Public Key to Server**

```bash
# Copy public key
cat github_deploy_key.pub

# SSH into server
ssh krishan@38.137.54.223

# Add to authorized_keys
mkdir -p ~/.ssh
echo "YOUR_PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

**Step 3: Add Secrets to GitHub**

Go to: `https://github.com/YOUR_USERNAME/Medical_chat_bots/settings/secrets/actions`

Add these secrets:

| Secret Name | Value | Example |
|------------|-------|---------|
| `SSH_PRIVATE_KEY` | Contents of `github_deploy_key` file | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `SERVER_IP` | Your server IP | `38.137.54.223` |
| `SERVER_USER` | SSH username | `krishan` |
| `REMOTE_DIR` | Application directory | `/home/krishan/projects/Medicalchatbot` |

**Step 4: Enable GitHub Actions**

The workflow file is already in `.github/workflows/deploy.yml`.

### Using Automated Deployment

**Option A: Auto-deploy on Push**
```bash
# Any push to main branch triggers deployment
git add .
git commit -m "Update application"
git push origin main

# GitHub Actions will automatically deploy
```

**Option B: Manual Trigger**
1. Go to GitHub → Actions tab
2. Select "Deploy Medical Chatbot" workflow
3. Click "Run workflow"
4. Select branch (usually `main`)
5. Click "Run workflow"

### Monitor Deployment

1. Go to GitHub → Actions tab
2. Click on the running workflow
3. Watch real-time logs
4. Wait for ✅ green checkmark

---

## ✅ Post-Deployment

### Verify Deployment

**1. Check Application Status**
```bash
ssh krishan@38.137.54.223 'ps aux | grep python'
```

**2. Check Logs**
```bash
ssh krishan@38.137.54.223 'tail -f /home/krishan/projects/Medicalchatbot/app.log'
```

**3. Test API Endpoints**

```bash
# Health check
curl http://38.137.54.223:5001/docs

# Upload test
curl -X POST "http://38.137.54.223:5001/upload_pdf/?collection_name=test" \
  -F "files=@test.pdf"

# Get collections
curl http://38.137.54.223:5001/get-collection

# Ask question
curl -X POST "http://38.137.54.223:5001/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this document about?",
    "collection_name": "test"
  }'
```

### Access Application

- **API Documentation**: http://38.137.54.223:5001/docs
- **Application**: http://38.137.54.223:5001

---

## 🔄 Rollback

If deployment fails or there's an issue:

### Automatic Rollback (Using Backup)

```bash
ssh krishan@38.137.54.223

cd /home/krishan/projects/Medicalchatbot

# List available backups
ls -lh backups/

# Extract backup (replace with your backup filename)
tar -xzf backups/backup_20250124_143000.tar.gz

# Restart application
pkill -f "python main.py"
python main.py
```

### Git Rollback

```bash
ssh krishan@38.137.54.223

cd /home/krishan/projects/Medicalchatbot

# View recent commits
git log --oneline -n 10

# Rollback to specific commit
git checkout <commit-hash>

# Restart application
pkill -f "python main.py"
python main.py
```

---

## 🔧 Troubleshooting

### Issue: "Permission denied"

```bash
ssh krishan@38.137.54.223

cd /home/krishan/projects/Medicalchatbot

# Fix permissions
chmod +x *.sh
./fix_permissions.sh
python fix_dirs.py
```

### Issue: "Module not found"

```bash
ssh krishan@38.137.54.223

cd /home/krishan/projects/Medicalchatbot

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: "Port already in use"

```bash
ssh krishan@38.137.54.223

# Find process using port 5001
lsof -i :5001

# Kill process
pkill -f "python main.py"

# Or kill by PID
kill -9 <PID>

# Restart
cd /home/krishan/projects/Medicalchatbot
python main.py
```

### Issue: "Cannot connect to ChromaDB"

```bash
ssh krishan@38.137.54.223

# Check if ChromaDB is running
ps aux | grep chroma

# Check port
netstat -tuln | grep 8000

# Start ChromaDB if needed
chroma run --path ./chroma_data --port 8000 &
```

### Issue: "Cannot connect to Ollama"

```bash
ssh krishan@38.137.54.223

# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
sudo systemctl start ollama

# Or run manually
nohup ollama serve > ~/ollama.log 2>&1 &

# Verify model
ollama list
ollama pull llama3.2:3b
```

### Issue: "Application not responding"

```bash
ssh krishan@38.137.54.223

cd /home/krishan/projects/Medicalchatbot

# Check logs
tail -100 app.log

# Check if process is running
ps aux | grep "python main.py"

# Restart with verbose logging
pkill -f "python main.py"
python main.py
```

---

## 📊 Monitoring

### View Real-time Logs

```bash
ssh krishan@38.137.54.223
tail -f /home/krishan/projects/Medicalchatbot/app.log
```

### Check Resource Usage

```bash
ssh krishan@38.137.54.223

# CPU and Memory
top
# Press 'q' to quit

# Disk usage
df -h

# Application specific
ps aux | grep python
```

### Application Status

```bash
ssh krishan@38.137.54.223

# Is it running?
systemctl status medical-chatbot  # If using systemd
# OR
ps aux | grep "python main.py"

# Check listening ports
netstat -tuln | grep 5001
```

---

## 🔐 Security Best Practices

### 1. Use SSH Keys (Not Passwords)

Already set up for GitHub Actions deployment.

### 2. Firewall Configuration

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 5001/tcp # Application
sudo ufw enable
sudo ufw status
```

### 3. Keep Dependencies Updated

```bash
pip list --outdated
pip install --upgrade package_name
```

### 4. Regular Backups

Backups are automatically created during deployment in:
`/home/krishan/projects/Medicalchatbot/backups/`

### 5. Secure Configuration

Never commit sensitive data to Git. Use environment variables:

```bash
# On server, create .env file
cat > .env << EOF
MONGO_USERNAME=your_username
MONGO_PASSWORD=your_password
OPENAI_API_KEY=your_key
EOF

chmod 600 .env
```

---

## 📅 Deployment Checklist

Before each deployment:

- [ ] Test locally
- [ ] Update requirements.txt if new dependencies added
- [ ] Update version/changelog
- [ ] Commit all changes to Git
- [ ] Tag release (optional): `git tag v1.0.0`
- [ ] Run deployment script or trigger GitHub Actions
- [ ] Verify application is running
- [ ] Test main endpoints
- [ ] Check logs for errors
- [ ] Notify team (if applicable)

---

## 🆘 Support

### Useful Commands Reference

```bash
# View logs
ssh krishan@38.137.54.223 'tail -f /home/krishan/projects/Medicalchatbot/app.log'

# Restart application
ssh krishan@38.137.54.223 'cd /home/krishan/projects/Medicalchatbot && pkill -f "python main.py" && python main.py'

# Check status
ssh krishan@38.137.54.223 'ps aux | grep python'

# Fix permissions
ssh krishan@38.137.54.223 'cd /home/krishan/projects/Medicalchatbot && ./fix_permissions.sh'

# View backups
ssh krishan@38.137.54.223 'ls -lh /home/krishan/projects/Medicalchatbot/backups/'
```

### Quick Deploy Command

```bash
cd C:\AI_projects\Cosmos_project\Medical_chat_bots && ./deploy.sh krishan@38.137.54.223 main
```

---

## 📝 Notes

- Deployment creates automatic backups before each deploy
- Backups are stored in `backups/` directory on server
- Old backups are NOT automatically deleted (manual cleanup needed)
- Application runs on port 5001
- Logs are in `app.log` in the application directory

**Your deployment system is ready! 🚀**

