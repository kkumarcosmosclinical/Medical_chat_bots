#!/bin/bash

# Quick fix for ChromaDB readonly database error

echo "=================================================="
echo "Fixing ChromaDB Permissions"
echo "=================================================="

# Get the current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Working directory: $SCRIPT_DIR"
echo ""

# Create ChromaDB directories
echo "Creating ChromaDB directories..."
mkdir -p chroma chroma_data .chroma
chmod 777 chroma chroma_data .chroma 2>/dev/null

# Fix ownership
echo "Fixing ownership..."
sudo chown -R $USER:$USER . 2>/dev/null || chown -R $USER:$USER .

# Fix ChromaDB SQLite database files
echo "Fixing ChromaDB database files..."
find . -name "*.sqlite*" -type f -exec chmod 666 {} \; 2>/dev/null
find chroma -type f -exec chmod 666 {} \; 2>/dev/null
find chroma_data -type f -exec chmod 666 {} \; 2>/dev/null
find .chroma -type f -exec chmod 666 {} \; 2>/dev/null

# Fix all directories recursively
echo "Fixing directory permissions..."
find chroma -type d -exec chmod 777 {} \; 2>/dev/null
find chroma_data -type d -exec chmod 777 {} \; 2>/dev/null
find .chroma -type d -exec chmod 777 {} \; 2>/dev/null

# Also fix uploaded_pdfs and Excel_files while we're at it
chmod 777 uploaded_pdfs Excel_files 2>/dev/null
chmod 666 combined.pdf 2>/dev/null

echo ""
echo "✅ ChromaDB permissions fixed!"
echo ""
echo "Directory permissions:"
ls -ld chroma* .chroma 2>/dev/null || echo "ChromaDB directories not found yet (will be created on first use)"
echo ""
echo "Database files:"
find . -name "*.sqlite*" -type f -ls 2>/dev/null | head -5 || echo "No database files found yet"
echo ""
echo "=================================================="
echo "Now restart your application:"
echo "  pkill -f 'python main.py'"
echo "  python main.py"
echo "=================================================="

