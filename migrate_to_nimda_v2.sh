#!/bin/bash
"""
🔄 NIMDA Migration Script
Скрипт для міграції до nimda_src_v2 workflow системи

Виконує:
1. Backup старих файлів
2. Переміщення до nimda_src_v2
3. Очищення дублікатів
4. Тестування нової системи
"""

echo "🚀 NIMDA Migration to v2.0 Workflow"
echo "═══════════════════════════════════════"

# Перевірка наявності nimda_src_v2
if [ ! -d "nimda_src_v2" ]; then
    echo "❌ Директорія nimda_src_v2 не знайдена!"
    exit 1
fi

echo "📦 Створення backup старих файлів..."
mkdir -p backup_before_migration
cp -r plugins/ backup_before_migration/ 2>/dev/null || true
cp -r Core/ backup_before_migration/ 2>/dev/null || true
cp run_plugin_system.py backup_before_migration/ 2>/dev/null || true
cp migrate_to_core.py backup_before_migration/ 2>/dev/null || true

echo "✅ Backup створено в backup_before_migration/"

echo "🧹 Очищення старих файлів..."
rm -rf plugins/
rm -rf Core/
rm -f run_plugin_system.py
rm -f migrate_to_core.py

echo "✅ Старі файли видалено"

echo "🔗 Створення symlink для зворотної сумісності..."
ln -sf nimda_src_v2/nimda_workflow_launcher.py run_nimda_workflow.py

echo "🧪 Тестування нової системи..."
cd nimda_src_v2

echo "📋 Перевірка структури..."
if [ -f "nimda_workflow_launcher.py" ] && [ -d "Core" ] && [ -d "plugins" ]; then
    echo "✅ Структура nimda_src_v2 правильна"
else
    echo "❌ Помилка структури nimda_src_v2"
    exit 1
fi

echo "🐍 Перевірка Python синтаксису..."
python3 -m py_compile nimda_workflow_launcher.py
python3 -m py_compile Core/plugin_system_runner.py
python3 -m py_compile plugins/plugin_manager.py

if [ $? -eq 0 ]; then
    echo "✅ Синтаксис Python правильний"
else
    echo "❌ Помилки синтаксису Python"
    exit 1
fi

cd ..

echo ""
echo "🎉 Міграція до NIMDA v2.0 завершена успішно!"
echo "═══════════════════════════════════════════════"
echo "📁 Нова система: nimda_src_v2/"
echo "🚀 Запуск: python3 nimda_src_v2/nimda_workflow_launcher.py"
echo "🔗 Швидкий запуск: python3 run_nimda_workflow.py"
echo "📦 Backup: backup_before_migration/"
echo ""
echo "🌟 NIMDA Agent Workflow System v2.0 готова до роботи!"
