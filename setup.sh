#!/bin/bash

# Setup script para entorno local
# Este script configura el entorno antes de ejecutar la aplicación

echo "🚀 Configurando entorno para Dashboard GitHub Copilot..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instala Python 3.8 o superior."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip &> /dev/null; then
    echo "❌ pip no está instalado. Por favor instala pip."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️ Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📋 Instalando dependencias..."
pip install -r requirements.txt

# Verificar que el archivo de datos existe
DATA_FILE="Encuesta de adopción de GitHub Copilot tabla.xlsx"
if [ ! -f "$DATA_FILE" ]; then
    echo "⚠️ ADVERTENCIA: No se encontró el archivo '$DATA_FILE'"
    echo "   Por favor, coloca el archivo en la raíz del proyecto antes de ejecutar la app."
    echo ""
fi

# Configurar locales para soporte de caracteres especiales
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

echo "✅ Setup completado!"
echo ""
echo "Para ejecutar la aplicación:"
echo "  1. Asegúrate de que el archivo '$DATA_FILE' esté en la raíz"
echo "  2. Ejecuta: streamlit run dashboard.py"
echo ""
echo "Para activar el entorno virtual manualmente:"
echo "  source venv/bin/activate"
