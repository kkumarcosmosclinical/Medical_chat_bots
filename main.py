import uvicorn
from config import settings
import os
import sys

def setup_directories():
    """Create necessary directories with proper permissions"""
    directories = [
        settings.UPLOAD_DIR,
        settings.EXCEL_DIR,
        '__pycache__',
        'chroma',
        'chroma_data',
        '.chroma',
    ]
    
    for directory in directories:
        try:
            os.makedirs(directory, mode=0o777, exist_ok=True)
            print(f"✓ Directory ready: {directory}")
        except Exception as e:
            print(f"⚠ Warning: Could not create/set permissions for {directory}: {e}")
    
    # Create combined.pdf if it doesn't exist
    try:
        if not os.path.exists(settings.COMBINED_PDF):
            with open(settings.COMBINED_PDF, 'w') as f:
                pass
            os.chmod(settings.COMBINED_PDF, 0o666)
    except Exception as e:
        print(f"⚠ Warning: Could not create combined.pdf: {e}")
    
    # Fix ChromaDB database files if they exist
    try:
        import glob
        for db_file in glob.glob('**/*.sqlite*', recursive=True):
            try:
                os.chmod(db_file, 0o666)
                print(f"✓ Fixed ChromaDB file: {db_file}")
            except:
                pass
    except:
        pass

if __name__ == "__main__":
    print("=" * 50)
    print("Medical Chatbot Application")
    print("=" * 50)
    
    # Setup directories
    setup_directories()
    
    print(f"\n🚀 Starting server on {settings.APP_HOST}:{settings.APP_PORT}")
    print(f"📚 API Documentation: http://localhost:{settings.APP_PORT}/docs")
    print("=" * 50 + "\n")
    
    try:
        uvicorn.run(
            "app:app", 
            host=settings.APP_HOST, 
            port=settings.APP_PORT,
            reload=False
        )
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)
