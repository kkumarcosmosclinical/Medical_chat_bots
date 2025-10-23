# Deployment Quick Reference

## 🚀 Deploy Now

```bash
cd C:\AI_projects\Cosmos_project\Medical_chat_bots
./deploy.sh krishan@38.137.54.223 main
```

---

## 📋 Common Commands

### Deploy
```bash
./deploy.sh krishan@38.137.54.223
```

### Check Status
```bash
ssh krishan@38.137.54.223 'ps aux | grep python'
```

### View Logs
```bash
ssh krishan@38.137.54.223 'tail -f /home/krishan/projects/Medicalchatbot/app.log'
```

### Restart App
```bash
ssh krishan@38.137.54.223 'cd /home/krishan/projects/Medicalchatbot && pkill -f "python main.py" && python main.py'
```

### Fix Permissions
```bash
ssh krishan@38.137.54.223 'cd /home/krishan/projects/Medicalchatbot && ./fix_permissions.sh'
```

---

## 🔧 Troubleshooting

### App Not Responding
```bash
ssh krishan@38.137.54.223
cd /home/krishan/projects/Medicalchatbot
tail -100 app.log
pkill -f "python main.py"
python main.py
```

### Permission Errors
```bash
ssh krishan@38.137.54.223
cd /home/krishan/projects/Medicalchatbot
./FIX_CHROMADB_PERMISSIONS.sh
./fix_permissions.sh
```

### ChromaDB Issues
```bash
ssh krishan@38.137.54.223
chmod 777 chroma chroma_data .chroma
find . -name "*.sqlite*" -exec chmod 666 {} \;
```

---

## 📊 URLs

- **App**: http://38.137.54.223:5001
- **Docs**: http://38.137.54.223:5001/docs

---

## 🔄 Rollback

```bash
ssh krishan@38.137.54.223
cd /home/krishan/projects/Medicalchatbot
ls backups/
tar -xzf backups/backup_YYYYMMDD_HHMMSS.tar.gz
pkill -f "python main.py"
python main.py
```

---

## 📦 GitHub Actions

**Manual Deploy:**
1. Go to GitHub → Actions
2. Select "Deploy Medical Chatbot"
3. Click "Run workflow"

**Auto Deploy:**
```bash
git add .
git commit -m "Update"
git push origin main
```

---

## ✅ Post-Deploy Check

```bash
# 1. Check process
ssh krishan@38.137.54.223 'ps aux | grep python'

# 2. Test API
curl http://38.137.54.223:5001/docs

# 3. Check logs
ssh krishan@38.137.54.223 'tail -20 /home/krishan/projects/Medicalchatbot/app.log'
```

