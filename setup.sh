#!/bin/bash

# Inventory Management System - Setup Script

echo "🎯 Inventory Management System - Setup"
echo "======================================"

# Check Python
echo "✓ Checking Python..."
python3 --version

# Install backend dependencies
echo "✓ Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Create .env file
echo "✓ Creating .env file..."
if [ ! -f .env ]; then
    cp ../.env.example .env
    echo "⚠️  Please update .env with your MySQL credentials"
fi

echo ""
echo "✓ Setup completed!"
echo ""
echo "📝 Next steps:"
echo "1. Update backend/.env with your MySQL credentials"
echo "2. Run MySQL setup:"
echo "   mysql -u root -p < database/schema.sql"
echo "   mysql -u root -p inventory_system < database/seed_data.sql"
echo "3. Start Flask server:"
echo "   cd backend && python main.py"
echo "4. Open frontend/index.html in your browser"
echo ""
echo "🚀 Happy inventory management!"
