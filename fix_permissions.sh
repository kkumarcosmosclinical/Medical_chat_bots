#!/bin/bash

# Script to fix directory permissions for Medical Chatbot application

echo "Fixing directory permissions..."

# Create directories if they don't exist
mkdir -p uploaded_pdfs
mkdir -p Excel_files
mkdir -p chroma
mkdir -p chroma_data
mkdir -p .chroma
mkdir -p __pycache__
mkdir -p Embedding_fuctions/__pycache__
mkdir -p chat_functions/__pycache__
mkdir -p database/__pycache__
mkdir -p Excel_chat_bot/__pycache__

# Set proper permissions for directories (rwxrwxrwx)
chmod 777 uploaded_pdfs
chmod 777 Excel_files
chmod 777 chroma 2>/dev/null || true
chmod 777 chroma_data 2>/dev/null || true
chmod 777 .chroma 2>/dev/null || true
chmod 755 __pycache__ 2>/dev/null || true
chmod 755 Embedding_fuctions/__pycache__ 2>/dev/null || true
chmod 755 chat_functions/__pycache__ 2>/dev/null || true
chmod 755 database/__pycache__ 2>/dev/null || true
chmod 755 Excel_chat_bot/__pycache__ 2>/dev/null || true

# Set proper permissions for uploaded files if they exist
find uploaded_pdfs -type f -exec chmod 666 {} \; 2>/dev/null || true
find Excel_files -type f -exec chmod 666 {} \; 2>/dev/null || true

# Fix ChromaDB database files if they exist
find . -name "*.sqlite*" -type f -exec chmod 666 {} \; 2>/dev/null || true
find chroma -type f -exec chmod 666 {} \; 2>/dev/null || true
find chroma_data -type f -exec chmod 666 {} \; 2>/dev/null || true
find .chroma -type f -exec chmod 666 {} \; 2>/dev/null || true

# Create combined.pdf with proper permissions if it doesn't exist
touch combined.pdf 2>/dev/null || true
chmod 666 combined.pdf 2>/dev/null || true

echo "✅ Permissions fixed successfully!"
echo ""
echo "Directory permissions:"
ls -ld uploaded_pdfs Excel_files combined.pdf 2>/dev/null || true

echo ""
echo "You can now run the application with: python main.py"

