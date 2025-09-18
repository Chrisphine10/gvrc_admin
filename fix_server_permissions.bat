@echo off
REM Script to fix admin permissions on the server (Windows)
REM Run this script on your server to fix the admin user permissions

echo 🔧 Fixing admin user permissions on server...

REM Activate virtual environment (adjust path as needed)
if exist "env\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call env\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    echo 📦 Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found, using system Python
)

REM Run the management command
echo 🚀 Running fix_admin_permissions command...
python manage.py fix_admin_permissions

echo ✅ Done! Try logging in again with your admin account.
pause
