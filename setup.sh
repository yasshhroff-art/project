#!/usr/bin/env bash
set -e

echo "=========================================="
echo "Google Ads Campaign Manager - Quick Setup"
echo "=========================================="
echo ""

# Ensure we're in project root
if [ ! -f "README.md" ]; then
  echo "❌ Please run this script from the project root directory"
  exit 1
fi

echo "📦 Checking system dependencies..."
echo ""

# --- Python 3.11 check (Windows-safe) ---
if ! py -3.11 --version >/dev/null 2>&1; then
  echo "❌ Python 3.11 not found"
  echo "👉 Install Python 3.11 (64-bit) from python.org"
  exit 1
fi
echo "✅ Python found: $(py -3.11 --version)"

# --- Node ---
if ! command -v node >/dev/null; then
  echo "❌ Node.js not found (need Node 16+)"
  exit 1
fi
echo "✅ Node found: $(node --version)"

# --- npm ---
if ! command -v npm >/dev/null; then
  echo "❌ npm not found"
  exit 1
fi
echo "✅ npm found: $(npm --version)"

echo ""
echo "🔧 Backend setup..."
echo ""

cd backend

# --- Create venv only if missing ---
if [ ! -d "venv" ]; then
  echo "Creating Python 3.11 virtual environment..."
  py -3.11 -m venv venv --without-pip
fi

# --- Activate venv (Windows Git Bash) ---
source venv/Scripts/activate

# --- Install pip if missing ---
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# --- Install backend deps ---
echo "Installing Python dependencies..."
pip install -r requirements.txt

# --- Env file ---
if [ ! -f ".env" ]; then
  echo "Creating backend .env file..."
  cp .env.example .env
fi

# --- DB init ---
echo "Initializing database..."
python init_db.py

echo "✅ Backend ready"
cd ..

echo ""
echo "⚛️ Frontend setup..."
echo ""

cd frontend

if [ ! -d "node_modules" ]; then
  echo "Installing frontend dependencies..."
  npm install
fi

if [ ! -f ".env" ]; then
  echo "Creating frontend .env file..."
  cp .env.example .env
fi

echo "✅ Frontend ready"
cd ..

echo ""
echo "=========================================="
echo "✅ SETUP COMPLETE"
echo "=========================================="
echo ""
echo "🚀 To start the app:"
echo ""
echo "Backend:"
echo "  cd backend"
echo "  source venv/Scripts/activate"
echo "  python app.py"
echo ""
echo "Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Open 👉 http://localhost:5173"
echo ""
