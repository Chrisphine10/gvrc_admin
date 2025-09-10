#!/bin/bash

# GVRC Admin - Gunicorn + Nginx Deployment Script
# This script sets up a production environment with Gunicorn and Nginx

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="gvrc_admin"
PROJECT_DIR="/var/www/$PROJECT_NAME"
SERVICE_USER="www-data"
NGINX_SITES_AVAILABLE="/etc/nginx/sites-available"
NGINX_SITES_ENABLED="/etc/nginx/sites-enabled"
SYSTEMD_DIR="/etc/systemd/system"

echo -e "${GREEN}Starting GVRC Admin deployment...${NC}"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}Please run as root (use sudo)${NC}"
    exit 1
fi

# Update system packages
echo -e "${YELLOW}Updating system packages...${NC}"
apt update && apt upgrade -y

# Install required packages
echo -e "${YELLOW}Installing required packages...${NC}"
apt install -y python3 python3-pip python3-venv nginx postgresql-client redis-server git

# Create project directory
echo -e "${YELLOW}Setting up project directory...${NC}"
mkdir -p $PROJECT_DIR
mkdir -p /var/log/gunicorn
mkdir -p /var/log/gvrc_admin
mkdir -p /var/run/gunicorn
mkdir -p /var/www/gvrc_admin/staticfiles
mkdir -p /var/www/gvrc_admin/media

# Set permissions
chown -R $SERVICE_USER:$SERVICE_USER $PROJECT_DIR
chown -R $SERVICE_USER:$SERVICE_USER /var/log/gunicorn
chown -R $SERVICE_USER:$SERVICE_USER /var/log/gvrc_admin
chown -R $SERVICE_USER:$SERVICE_USER /var/run/gunicorn

# Copy project files (assuming current directory is the project)
echo -e "${YELLOW}Copying project files...${NC}"
cp -r . $PROJECT_DIR/
cd $PROJECT_DIR

# Create virtual environment
echo -e "${YELLOW}Creating virtual environment...${NC}"
python3 -m venv env
source env/bin/activate

# Install Python dependencies
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Set up environment variables
echo -e "${YELLOW}Setting up environment variables...${NC}"
if [ ! -f .env ]; then
    cp env.example .env
    echo -e "${YELLOW}Please edit .env file with your production settings${NC}"
fi

# Collect static files
echo -e "${YELLOW}Collecting static files...${NC}"
python manage.py collectstatic --noinput --settings=core.settings.prod

# Run database migrations
echo -e "${YELLOW}Running database migrations...${NC}"
python manage.py migrate --settings=core.settings.prod

# Create superuser (optional)
echo -e "${YELLOW}Do you want to create a superuser? (y/n)${NC}"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser --settings=core.settings.prod
fi

# Configure Nginx
echo -e "${YELLOW}Configuring Nginx...${NC}"
cp nginx/appseed-app.conf $NGINX_SITES_AVAILABLE/$PROJECT_NAME
ln -sf $NGINX_SITES_AVAILABLE/$PROJECT_NAME $NGINX_SITES_ENABLED/

# Remove default Nginx site if it exists
if [ -f $NGINX_SITES_ENABLED/default ]; then
    rm $NGINX_SITES_ENABLED/default
fi

# Test Nginx configuration
nginx -t

# Configure systemd services
echo -e "${YELLOW}Configuring systemd services...${NC}"
cp systemd/gvrc-admin-gunicorn.service $SYSTEMD_DIR/
cp systemd/gvrc-admin-gunicorn.socket $SYSTEMD_DIR/
cp systemd/gvrc-admin-nginx.service $SYSTEMD_DIR/

# Reload systemd and enable services
systemctl daemon-reload
systemctl enable gvrc-admin-gunicorn.socket
systemctl enable gvrc-admin-nginx.service

# Start services
echo -e "${YELLOW}Starting services...${NC}"
systemctl start gvrc-admin-gunicorn.socket
systemctl start gvrc-admin-nginx.service

# Enable firewall (if ufw is available)
if command -v ufw &> /dev/null; then
    echo -e "${YELLOW}Configuring firewall...${NC}"
    ufw allow 'Nginx Full'
    ufw allow ssh
    ufw --force enable
fi

# Set up log rotation
echo -e "${YELLOW}Setting up log rotation...${NC}"
cat > /etc/logrotate.d/gvrc-admin << EOF
/var/log/gunicorn/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
    postrotate
        systemctl reload gvrc-admin-gunicorn
    endscript
}

/var/log/gvrc_admin/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
}
EOF

# Create management scripts
echo -e "${YELLOW}Creating management scripts...${NC}"
cat > /usr/local/bin/gvrc-admin-manage << 'EOF'
#!/bin/bash
cd /var/www/gvrc_admin
source env/bin/activate
python manage.py "$@" --settings=core.settings.prod
EOF

chmod +x /usr/local/bin/gvrc-admin-manage

# Create service management script
cat > /usr/local/bin/gvrc-admin-service << 'EOF'
#!/bin/bash
case "$1" in
    start)
        systemctl start gvrc-admin-gunicorn.socket
        systemctl start gvrc-admin-nginx.service
        echo "Services started"
        ;;
    stop)
        systemctl stop gvrc-admin-gunicorn.socket
        systemctl stop gvrc-admin-nginx.service
        echo "Services stopped"
        ;;
    restart)
        systemctl restart gvrc-admin-gunicorn.socket
        systemctl restart gvrc-admin-nginx.service
        echo "Services restarted"
        ;;
    status)
        systemctl status gvrc-admin-gunicorn.socket
        systemctl status gvrc-admin-nginx.service
        ;;
    reload)
        systemctl reload gvrc-admin-gunicorn
        systemctl reload gvrc-admin-nginx.service
        echo "Services reloaded"
        ;;
    logs)
        journalctl -u gvrc-admin-gunicorn -f
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|reload|logs}"
        exit 1
        ;;
esac
EOF

chmod +x /usr/local/bin/gvrc-admin-service

# Final status check
echo -e "${YELLOW}Checking service status...${NC}"
systemctl status gvrc-admin-gunicorn.socket --no-pager
systemctl status gvrc-admin-nginx.service --no-pager

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}Your application should be available at: http://$(hostname -I | awk '{print $1}')${NC}"
echo -e "${GREEN}Use 'gvrc-admin-service' command to manage services${NC}"
echo -e "${GREEN}Use 'gvrc-admin-manage' command to run Django management commands${NC}"

# Display useful information
echo -e "${YELLOW}Useful commands:${NC}"
echo "  Service management: gvrc-admin-service {start|stop|restart|status|reload|logs}"
echo "  Django management: gvrc-admin-manage {command}"
echo "  View logs: journalctl -u gvrc-admin-gunicorn -f"
echo "  Nginx logs: tail -f /var/log/nginx/access.log"
echo "  Nginx error logs: tail -f /var/log/nginx/error.log"
