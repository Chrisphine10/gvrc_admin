#!/usr/bin/env python3
"""
Script to create chat media directories
"""

import os

def create_chat_directories():
    """Create chat media directories"""
    base_dir = "media"
    chat_dir = os.path.join(base_dir, "chat_files")
    
    # Create main chat directory
    os.makedirs(chat_dir, exist_ok=True)
    print(f"Created directory: {chat_dir}")
    
    # Create subdirectories for different file types
    subdirs = [
        "images",
        "videos", 
        "documents",
        "audio"
    ]
    
    for subdir in subdirs:
        subdir_path = os.path.join(chat_dir, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        print(f"Created directory: {subdir_path}")
    
    # Create year/month/day structure
    import datetime
    now = datetime.datetime.now()
    date_dir = os.path.join(chat_dir, str(now.year), f"{now.month:02d}", f"{now.day:02d}")
    os.makedirs(date_dir, exist_ok=True)
    print(f"Created date directory: {date_dir}")
    
    print("\nChat media directories created successfully!")
    print(f"Base chat directory: {chat_dir}")

if __name__ == "__main__":
    create_chat_directories()
