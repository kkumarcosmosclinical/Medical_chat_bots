# Fix Permission Errors - Quick Guide

## The Problem
You're getting: `PermissionError: [Errno 13] Permission denied: 'uploaded_pdfs/file-sample_150kB.pdf'`

## Quick Fix (On Your Linux Server)

### Option 1: Run the Fix Script (Easiest)

```bash
# Navigate to your project directory
cd /home/krishan/projects/Medicalchatbot

# Make the script executable
chmod +x fix_permissions.sh

# Run it
./fix_permissions.sh
```

### Option 2: Manual Commands

```bash
# Navigate to your project directory
cd /home/krishan/projects/Medicalchatbot

# Create directories with proper permissions
mkdir -p uploaded_pdfs Excel_files
chmod 777 uploaded_pdfs
chmod 777 Excel_files

# If combined.pdf exists, fix its permissions
chmod 666 combined.pdf 2>/dev/null || true

# Fix any existing files
find uploaded_pdfs -type f -exec chmod 666 {} \;
find Excel_files -type f -exec chmod 666 {} \;

# Restart your application
python main.py
```

### Option 3: Run with Proper User (Recommended for Production)

```bash
# Change ownership to your user
sudo chown -R $USER:$USER /home/krishan/projects/Medicalchatbot

# Set proper permissions
chmod 755 /home/krishan/projects/Medicalchatbot
chmod 777 uploaded_pdfs Excel_files
```

## Verify Permissions

```bash
# Check directory permissions
ls -la uploaded_pdfs Excel_files

# Should show something like:
# drwxrwxrwx 2 krishan krishan 4096 Oct 24 02:30 uploaded_pdfs
# drwxrwxrwx 2 krishan krishan 4096 Oct 24 02:30 Excel_files
```

## Restart the Application

```bash
# Stop the current running process (Ctrl+C if running in terminal)
# Or if running as a service:
# sudo systemctl restart medical-chatbot

# Start again
python main.py
```

## Permanent Fix (Optional)

If you're running this as a systemd service, add this to your service file:

```ini
[Service]
User=krishan
Group=krishan
WorkingDirectory=/home/krishan/projects/Medicalchatbot
UMask=0002
```

## Code Changes Already Made

✅ Updated `app.py` to:
- Create directories with `mode=0o777`
- Set file permissions after writing
- Better error handling

✅ Updated `main.py` to:
- Automatically create directories on startup
- Set proper permissions
- Show helpful status messages

## Still Having Issues?

1. **Check if directory exists:**
   ```bash
   ls -la /home/krishan/projects/Medicalchatbot/uploaded_pdfs
   ```

2. **Check disk space:**
   ```bash
   df -h
   ```

3. **Check SELinux (if enabled):**
   ```bash
   getenforce
   # If it says "Enforcing", you might need to adjust SELinux policies
   ```

4. **Run as different user (temporary test):**
   ```bash
   sudo python main.py  # Not recommended for production!
   ```

## Test the Fix

After fixing permissions, test with:

```bash
curl -X POST "http://localhost:5001/upload_pdf/?collection_name=test" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@your_test_file.pdf"
```

If you still get errors, check the application logs for more details.

