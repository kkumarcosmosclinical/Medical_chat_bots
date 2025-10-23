#!/usr/bin/env python3
"""
Quick script to fix directory permissions for Medical Chatbot
Run this on your server before starting the application
"""
import os
import sys

def fix_permissions():
    """Fix permissions for all necessary directories and files"""
    print("=" * 60)
    print("Fixing Directory Permissions")
    print("=" * 60)
    
    # Get current directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Working directory: {base_dir}\n")
    
    # Directories to create/fix
    directories = [
        'uploaded_pdfs',
        'Excel_files',
        'chroma',
        'chroma_data',
        '.chroma',
    ]
    
    # Create directories with full permissions
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        try:
            # Create if doesn't exist
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, mode=0o777)
                print(f"✓ Created: {directory}")
            else:
                # Fix permissions if exists
                os.chmod(dir_path, 0o777)
                print(f"✓ Fixed permissions: {directory}")
            
            # Verify permissions
            stat_info = os.stat(dir_path)
            perms = oct(stat_info.st_mode)[-3:]
            print(f"  Permissions: {perms}")
            
        except Exception as e:
            print(f"✗ Error with {directory}: {e}")
    
    # Fix combined.pdf if it exists
    combined_pdf = os.path.join(base_dir, 'combined.pdf')
    try:
        if os.path.exists(combined_pdf):
            os.chmod(combined_pdf, 0o666)
            print(f"\n✓ Fixed permissions: combined.pdf")
        else:
            # Create empty file
            with open(combined_pdf, 'w') as f:
                pass
            os.chmod(combined_pdf, 0o666)
            print(f"\n✓ Created: combined.pdf")
    except Exception as e:
        print(f"\n⚠ Warning with combined.pdf: {e}")
    
    # Fix existing files in directories
    print("\nFixing existing files...")
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        if os.path.exists(dir_path):
            for filename in os.listdir(dir_path):
                file_path = os.path.join(dir_path, filename)
                if os.path.isfile(file_path):
                    try:
                        os.chmod(file_path, 0o666)
                        print(f"  ✓ Fixed: {directory}/{filename}")
                    except Exception as e:
                        print(f"  ✗ Error: {directory}/{filename}: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Permission fix complete!")
    print("=" * 60)
    print("\nNow you can run: python main.py")
    print()

if __name__ == "__main__":
    try:
        fix_permissions()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

