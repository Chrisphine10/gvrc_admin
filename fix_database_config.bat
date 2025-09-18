@echo off
REM Script to fix database configuration on Windows

echo 🔧 Fixing database configuration...

REM Check current environment variables
echo 📋 Current environment variables:
echo DB_ENGINE: %DB_ENGINE%
echo DB_NAME: %DB_NAME%
echo DB_USERNAME: %DB_USERNAME%
echo DB_HOST: %DB_HOST%
echo DB_PORT: %DB_PORT%

REM Fix the DB_ENGINE variable
echo 🔧 Setting correct DB_ENGINE...
set DB_ENGINE=postgresql

REM Set other database variables if not set
if "%DB_NAME%"=="" set DB_NAME=gvrc_db
if "%DB_USERNAME%"=="" set DB_USERNAME=postgres
if "%DB_PASS%"=="" set DB_PASS=postgres123#
if "%DB_HOST%"=="" set DB_HOST=database-postgres.cn2uqm2iclii.eu-north-1.rds.amazonaws.com
if "%DB_PORT%"=="" set DB_PORT=5432

echo ✅ Updated environment variables:
echo DB_ENGINE: %DB_ENGINE%
echo DB_NAME: %DB_NAME%
echo DB_USERNAME: %DB_USERNAME%
echo DB_HOST: %DB_HOST%
echo DB_PORT: %DB_PORT%

REM Test database connection
echo 🔍 Testing database connection...
python manage.py check --database default

echo ✅ Database configuration fixed!
echo 🚀 You can now run your Django commands normally.
pause
