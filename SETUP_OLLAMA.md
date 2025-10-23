# Setup Ollama on Your Server

## Quick Summary

Your Medical Chatbot needs **Ollama** running to answer questions. Follow these steps to install and configure it on your Linux server.

---

## 📋 Step-by-Step Installation

### 1. SSH into Your Server

```bash
ssh krishan@38.137.54.223
```

### 2. Install Ollama

```bash
# Download and install Ollama
curl -fsSL https://ollama.com/install.sh | sh
```

### 3. Start Ollama Service

**Option A: Run in Background**
```bash
# Start Ollama in background
nohup ollama serve > ~/ollama.log 2>&1 &

# Check if it's running
ps aux | grep ollama
```

**Option B: Run as Systemd Service (Recommended for Production)**
```bash
# Ollama should auto-create a systemd service during installation
# Enable and start it
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama

# Check logs if needed
sudo journalctl -u ollama -f
```

### 4. Pull the Required Model

```bash
# This will download the llama3.2:3b model (~2GB)
ollama pull llama3.2:3b

# Verify the model is installed
ollama list
```

### 5. Test Ollama is Working

```bash
# Test the API endpoint
curl http://127.0.0.1:11434/api/tags

# Should return JSON with available models
# Example output:
# {"models":[{"name":"llama3.2:3b","modified_at":"2025-10-24T...",...}]}

# Test chat completion
curl http://127.0.0.1:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.2:3b",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### 6. Deploy Updated Config Files

**Copy the updated files to your server:**

```bash
# From your Windows machine
cd C:\AI_projects\Cosmos_project\Medical_chat_bots

# Copy updated files
scp config.py app.py krishan@38.137.54.223:/home/krishan/projects/Medicalchatbot/
```

### 7. Restart Your Application

```bash
# On the server
cd /home/krishan/projects/Medicalchatbot

# Stop the old process
pkill -f "python main.py"

# Start with new config
python main.py
```

---

## 🔍 Verify Everything Works

### Test the Complete Flow:

1. **Upload a PDF:**
```bash
curl -X POST "http://38.137.54.223:5001/upload_pdf/?collection_name=test123" \
  -F "files=@test.pdf"
```

2. **Ask a Question:**
```bash
curl -X POST "http://38.137.54.223:5001/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this document about?",
    "collection_name": "test123"
  }'
```

You should get a proper answer! ✅

---

## 🔧 Troubleshooting

### Issue: "Cannot connect to Ollama"

**Check if Ollama is running:**
```bash
ps aux | grep ollama
# OR
sudo systemctl status ollama
```

**Check if port is listening:**
```bash
netstat -tuln | grep 11434
# OR
ss -tuln | grep 11434
```

**Restart Ollama:**
```bash
sudo systemctl restart ollama
# OR
pkill ollama && nohup ollama serve > ~/ollama.log 2>&1 &
```

### Issue: Model not found

```bash
# List installed models
ollama list

# Pull the model again if missing
ollama pull llama3.2:3b
```

### Issue: Port 11434 already in use

```bash
# Find what's using the port
sudo lsof -i :11434

# Kill the process
sudo kill -9 <PID>

# Restart Ollama
sudo systemctl restart ollama
```

### Issue: Out of memory

Ollama needs at least **4GB RAM** to run `llama3.2:3b`. Check available memory:

```bash
free -h

# If low on RAM, use a smaller model
ollama pull llama3.2:1b  # Smaller, needs less RAM
```

Then update `chat_functions/chats.py` to use the smaller model:
```python
def rag(query, retrieved_documents, model="llama3.2:1b"):
```

---

## 📊 Resource Requirements

- **Disk Space**: ~2GB for llama3.2:3b model
- **RAM**: Minimum 4GB, Recommended 8GB+
- **CPU**: Any modern CPU (GPU not required but helps)

---

## 🚀 Performance Tips

### Use GPU Acceleration (If Available)

Ollama automatically uses GPU if NVIDIA GPU is available:

```bash
# Check for GPU
nvidia-smi

# Ollama will automatically use it
```

### Adjust Model Size Based on Hardware

| Model | Size | RAM Needed | Speed |
|-------|------|------------|-------|
| llama3.2:1b | 1.3GB | 2-4GB | Fast |
| llama3.2:3b | 2.0GB | 4-8GB | Medium |
| llama3.2:7b | 4.7GB | 8-16GB | Slower, Better Quality |

---

## ⚙️ Advanced Configuration

### Run Ollama on Different Port

```bash
# Set environment variable
export OLLAMA_HOST=0.0.0.0:8080

# Start Ollama
ollama serve
```

Then update your `config.py`:
```python
OLLAMA_PORT: int = int(os.getenv('OLLAMA_PORT', '8080'))
```

### Limit Ollama Memory Usage

```bash
# Set max memory (e.g., 4GB)
export OLLAMA_MAX_LOADED_MODELS=1
export OLLAMA_NUM_PARALLEL=1

ollama serve
```

---

## ✅ Quick Checklist

Before using the chatbot, verify:

- [ ] Ollama is installed: `which ollama`
- [ ] Ollama is running: `ps aux | grep ollama`
- [ ] Port 11434 is listening: `ss -tuln | grep 11434`
- [ ] Model is downloaded: `ollama list`
- [ ] API is responding: `curl http://127.0.0.1:11434/api/tags`
- [ ] Updated config files are deployed
- [ ] Application is restarted

---

## 🆘 Still Having Issues?

Check the logs:

```bash
# Application logs
tail -f ~/medical_chatbot.log

# Ollama logs (if running as service)
sudo journalctl -u ollama -f

# Ollama logs (if running in background)
tail -f ~/ollama.log
```

Contact support with these log outputs if issues persist.

