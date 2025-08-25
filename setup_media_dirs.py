#!/usr/bin/env python3
"""
Script to set up media directories for chat files
"""

import os

def create_media_directories():
    """Create media directories for chat files"""
    base_dir = "media"
    chat_dir = os.path.join(base_dir, "chat_files")
    
    # Create main chat directory
    os.makedirs(chat_dir, exist_ok=True)
    
    # Create subdirectories for different file types
    subdirs = [
        "images",
        "videos", 
        "documents",
        "audio"
    ]
    
    for subdir in subdirs:
        os.makedirs(os.path.join(chat_dir, subdir), exist_ok=True)
        print(f"Created directory: {os.path.join(chat_dir, subdir)}")
    
    # Create year/month/day structure
    import datetime
    now = datetime.datetime.now()
    date_dir = os.path.join(chat_dir, str(now.year), f"{now.month:02d}", f"{now.day:02d}")
    os.makedirs(date_dir, exist_ok=True)
    print(f"Created date directory: {date_dir}")
    
    print("\nMedia directories created successfully!")
    print(f"Base chat directory: {chat_dir}")

if __name__ == "__main__":
    create_media_directories()
