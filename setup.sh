#!/bin/bash

# Setup script for Sourcing Evaluator

echo "🚀 Sourcing Evaluator - Setup"
echo "==============================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no encontrado. Instálalo desde https://python.org"
    exit 1
fi

echo "✓ Python encontrado: $(python3 --version)"
echo ""

# Create venv
echo "📦 Creando virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✓ Virtual environment activado"
echo ""

# Install deps
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

echo "✓ Dependencias instaladas"
echo ""

# Create .env
if [ ! -f .env ]; then
    echo "⚙️  Creando archivo .env..."
    cp .env.example .env
    echo "✓ Archivo .env creado"
    echo ""
    echo "⚠️  IMPORTANTE: Edita .env y agrega tu GEMINI_API_KEY"
    echo "   1. Ve a https://ai.google.dev"
    echo "   2. Click 'Get API Key'"
    echo "   3. Copia tu API key en .env"
else
    echo "✓ .env ya existe"
fi

echo ""
echo "✅ Setup completado!"
echo ""
echo "Próximos pasos:"
echo "1. Edita .env con tu GEMINI_API_KEY"
echo "2. Ejecuta: source venv/bin/activate"
echo "3. Ejecuta: python app.py"
echo "4. Abre: http://localhost:8000"
echo ""
