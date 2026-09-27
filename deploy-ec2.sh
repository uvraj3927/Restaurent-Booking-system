#!/bin/bash

##############################################################################
# PYRITES GRILL - AWS DEPLOYMENT SCRIPT
# Complete setup for EC2 + RDS + S3 deployment
# Run this script on your EC2 instance (Ubuntu 24.04 LTS)
##############################################################################

set -e  # Exit on any error

echo "========================================================================"
echo "PYRITES GRILL - AWS DEPLOYMENT INITIALIZATION"
echo "========================================================================"
echo ""

# ==============================================================================
# PHASE 1: SYSTEM SETUP & DEPENDENCIES
# ==============================================================================
echo "[PHASE 1] Installing system dependencies..."
echo ""

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    mysql-client \
    curl \
    wget

echo "✅ System dependencies installed"
echo ""

# ==============================================================================
# PHASE 2: CLONE REPOSITORY
# ==============================================================================
echo "[PHASE 2] Cloning repository..."
echo ""

cd /home/ubuntu
git clone https://github.com/uvraj3927/Restaurent-Booking-system.git
cd Restaurent-Booking-system

echo "✅ Repository cloned to /home/ubuntu/Restaurent-Booking-system"
echo ""

# ==============================================================================
# PHASE 3: BACKEND SETUP
# ==============================================================================
echo "[PHASE 3] Setting up Flask backend..."
echo ""

cd backend

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

echo "✅ Virtual environment created and activated"
echo ""

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "✅ Python dependencies installed"
echo ""

# ==============================================================================
# PHASE 4: ENVIRONMENT CONFIGURATION
# ==============================================================================
echo "[PHASE 4] Configuring environment variables..."
echo ""

# Copy example to actual .env file
cp .env.example .env

echo "⚠️  IMPORTANT: Edit .env with your actual database credentials:"
echo ""
echo "   nano /home/ubuntu/Restaurent-Booking-system/backend/.env"
echo ""
echo "   Required fields to update:"
echo "   - DATABASE_URL (RDS endpoint, username, password)"
echo "   - FLASK_ENV (set to: production)"
echo "   - SECRET_KEY (generate secure key)"
echo "   - ADMIN_API_KEY (generate secure key)"
echo ""
echo "   Example DATABASE_URL:"
echo "   mysql+pymysql://admin:YOUR_PASSWORD@terraform-XXXXX.cahuiyuc6om9.us-east-1.rds.amazonaws.com:3306/myappdb"
echo ""

read -p "Press ENTER after editing .env file..."

echo ""

# ==============================================================================
# PHASE 5: DATABASE CONNECTION TEST
# ==============================================================================
echo "[PHASE 5] Testing database connection..."
echo ""

# Read DATABASE_URL from .env
DB_URL=$(grep "^DATABASE_URL=" .env | cut -d'=' -f2)

if [[ "$DB_URL" == *"mysql"* ]]; then
    echo "Testing connection to RDS database..."
    # Extract host from DATABASE_URL
    DB_HOST=$(echo "$DB_URL" | sed -n 's/.*@\([^:]*\).*/\1/p')
    echo "   Database Host: $DB_HOST"
    
    if mysql -h "$DB_HOST" -u admin -p -e "SELECT 1;" 2>/dev/null; then
        echo "✅ Database connection successful"
    else
        echo "❌ Database connection failed - check credentials in .env"
        exit 1
    fi
else
    echo "⚠️  Using SQLite (development only)"
fi

echo ""

# ==============================================================================
# PHASE 6: DATABASE SEEDING
# ==============================================================================
echo "[PHASE 6] Seeding database with initial data..."
echo ""

python seeds.py

echo "✅ Database seeded successfully"
echo ""

# ==============================================================================
# PHASE 7: BACKEND VERIFICATION
# ==============================================================================
echo "[PHASE 7] Verifying backend setup..."
echo ""

echo "Backend directory: /home/ubuntu/Restaurent-Booking-system/backend"
echo "Virtual environment: /home/ubuntu/Restaurent-Booking-system/backend/venv"
echo "Configuration file: /home/ubuntu/Restaurent-Booking-system/backend/.env"
echo "Main app: /home/ubuntu/Restaurent-Booking-system/backend/app.py"
echo ""

# ==============================================================================
# PHASE 8: FRONTEND S3 PREPARATION INFO
# ==============================================================================
echo "[PHASE 8] Frontend deployment information..."
echo ""

echo "Frontend location: /home/ubuntu/Restaurent-Booking-system/frontend"
echo "S3 Bucket: restaurant-booking-frontend-868ca2b4"
echo ""

# ==============================================================================
# PHASE 9: STARTUP INSTRUCTIONS
# ==============================================================================
echo ""
echo "========================================================================"
echo "✅ SETUP COMPLETE - READY FOR DEPLOYMENT"
echo "========================================================================"
echo ""

echo "TO START THE FLASK BACKEND:"
echo ""
echo "  1. Activate virtual environment:"
echo "     source /home/ubuntu/Restaurent-Booking-system/backend/venv/bin/activate"
echo ""
echo "  2. Start Flask development server:"
echo "     cd /home/ubuntu/Restaurent-Booking-system/backend"
echo "     python app.py"
echo ""
echo "  3. For production (with Gunicorn):"
echo "     pip install gunicorn"
echo "     gunicorn --bind 0.0.0.0:5000 --workers 4 app:app"
echo ""
echo "  4. Verify backend is running:"
echo "     curl http://localhost:5000/api/health"
echo ""

echo "TO DEPLOY FRONTEND TO S3 (from local machine):"
echo ""
echo "  1. Install AWS CLI (if not already installed):"
echo "     pip install awscli"
echo ""
echo "  2. Configure AWS credentials:"
echo "     aws configure"
echo ""
echo "  3. Sync frontend files to S3:"
echo "     aws s3 sync ./frontend/ s3://restaurant-booking-frontend-868ca2b4/ --delete"
echo ""
echo "  4. Access frontend:"
echo "     http://restaurant-booking-frontend-868ca2b4.s3-website-us-east-1.amazonaws.com"
echo ""

echo "TROUBLESHOOTING:"
echo ""
echo "  • Check backend logs:"
echo "    tail -f /var/log/flask-app.log"
echo ""
echo "  • Test RDS connection:"
echo "    mysql -h <RDS_ENDPOINT> -u admin -p myappdb -e 'SELECT 1;'"
echo ""
echo "  • Test CORS:"
echo "    curl -H 'Origin: http://restaurant-booking-frontend-868ca2b4.s3-website-us-east-1.amazonaws.com' http://44.200.253.83:5000/api/restaurants"
echo ""
echo "========================================================================"
echo ""
