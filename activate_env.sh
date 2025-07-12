#!/bin/zsh
# Script para activar el entorno virtual correctamente
echo "🔄 Activando entorno virtual..."
source .venv/bin/activate
echo "✅ Entorno virtual activado"
echo "📍 Python path: $(which python)"
echo "🐍 Python version: $(python --version)"
echo "📦 VIRTUAL_ENV: $VIRTUAL_ENV"
