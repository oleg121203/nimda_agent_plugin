#!/bin/bash

# NIMDA Agent GUI Launcher
# Автоматичний запуск з перевіркою залежностей

echo "🤖 NIMDA Agent - GUI Launcher"
echo "==============================="

# Перевіряємо наявність Python 3.11
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    echo "❌ Python не знайдено!"
    exit 1
fi

echo "🐍 Using: $PYTHON_CMD"

# Перевіряємо чи встановлені GUI залежності
if ! $PYTHON_CMD -c "import PySide6" &> /dev/null; then
    echo "📦 GUI залежності не встановлені. Встановлюємо..."
    $PYTHON_CMD nimda_app.py --install-gui-deps
    
    if [ $? -ne 0 ]; then
        echo "❌ Помилка встановлення залежностей"
        exit 1
    fi
fi

# Запускаємо NIMDA GUI
echo "🚀 Starting NIMDA GUI..."
$PYTHON_CMD nimda_app.py --mode gui

echo "👋 NIMDA GUI завершено"
