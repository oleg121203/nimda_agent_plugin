# NIMDA Agent Plugin

🤖 **Універсальний автономний агент розробки**

NIMDA Agent Plugin - це потужний інструмент для автоматизації розробки програмного забезпечення. Він може бути доданий до будь-якого проекту як окремий плагін і забезпечує повний цикл автономної розробки.

## 🎯 Основні можливості

- **📋 Управління планом розробки** - читання та виконання DEV_PLAN.md
- **🔧 Git інтеграція** - повне управління локальним та віддаленим репозиторієм
- **🤖 Автономність** - самостійне виконання задач без втручання
- **🔄 Автоматичне виправлення** - виявлення та усунення помилок
- **♻️ Повторне виконання завдань** - підзадачі DEV плану виконуються кілька разів
  до успіху (кількість спроб налаштовується через `MAX_RETRIES`)
- **📝 Ведення журналу** - автоматичне оновлення CHANGELOG.md
- **🌐 Codex інтеграція** - управління через віддалені команди
- **🚀 Універсальність** - підтримка Python, JavaScript, Web та інших проектів

## 📁 Структура плагіна

```
nimda_agent_plugin/
├── __init__.py              # Ініціалізація плагіна
├── agent.py                 # Основний клас агента
├── dev_plan_manager.py      # Менеджер DEV_PLAN.md
├── git_manager.py           # Менеджер Git репозиторію
├── command_processor.py     # Обробник команд
├── project_initializer.py   # Ініціалізатор проекту
├── changelog_manager.py     # Менеджер CHANGELOG.md
├── run_nimda_agent.py       # Скрипт запуску
└── README.md               # Ця документація
```

## 🚀 Швидкий старт

### 1. Додавання до проекту

Скопіюйте папку `nimda_agent_plugin` до кореня вашого проекту:

```bash
# Клонування або завантаження плагіна
cp -r nimda_agent_plugin /path/to/your/project/

# Перехід до проекту
cd /path/to/your/project/
```

### 2. Ініціалізація

```bash
# Ініціалізація нового проекту
python nimda_agent_plugin/run_nimda_agent.py --init

# Або якщо проект вже існує
python nimda_agent_plugin/run_nimda_agent.py --command "ініціалізація"
```

### 3. Створення DEV_PLAN.md

Агент автоматично створить шаблон DEV_PLAN.md, але ви можете створити свій:

```markdown
# План розробки мого проекту

## Опис проекту
Опишіть ваш проект тут.

## Головні задачі

### 1. Базова функціональність
- [ ] Створити основні класи
- [ ] Реалізувати API
- [ ] Написати тести

### 2. Оптимізація
- [ ] Покращити продуктивність
- [ ] Додати кешування
- [ ] Оптимізувати базу даних

### 3. Документація
- [ ] Написати README
- [ ] Створити API документацію
- [ ] Додати приклади використання
```

## 🎮 Використання

### Інтерактивний режим

```bash
python nimda_agent_plugin/run_nimda_agent.py
```

### Виконання команд

```bash
# Показати статус
python nimda_agent_plugin/run_nimda_agent.py --command "статус"

# Оновити план розробки
python nimda_agent_plugin/run_nimda_agent.py --command "допрацюй девплан"

# Виконати конкретну задачу
python nimda_agent_plugin/run_nimda_agent.py --command "виконай задачу номер 1"

# Виконати весь план
python nimda_agent_plugin/run_nimda_agent.py --command "виконай весь ДЕВ"
# Команда автоматично синхронізує зміни з GitHub

# Синхронізація з Git
python nimda_agent_plugin/run_nimda_agent.py --command "синхронізація"
```

### Режим демона

```bash
# Запуск у режимі очікування команд
python nimda_agent_plugin/run_nimda_agent.py --daemon
```

## 📋 Підтримувані команди

| Команда | Опис |
|---------|------|
| `статус` | Поточний статус агента та прогрес |
| `допрацюй девплан` | Оновлення та розширення DEV_PLAN.md |
| `виконай задачу номер X` | Виконання конкретної задачі з плану |
| `виконай весь ДЕВ` | Виконання всього плану з автосинхронізацією GitHub |
| `синхронізація` | Синхронізація з віддаленим Git репозиторієм |
| `виправити помилки` | Автоматичне виявлення та виправлення помилок |
| `ініціалізація` | Створення базової структури проекту |
| `допомога` | Показ списку доступних команд |

## 🔧 Налаштування GitHub

```bash
# Підключення GitHub репозиторію
python nimda_agent_plugin/run_nimda_agent.py --setup-github https://github.com/username/repository.git

# Або через команду
python nimda_agent_plugin/run_nimda_agent.py --command "налаштувати github https://github.com/username/repository.git"
```

## 🌐 Інтеграція з Codex

Агент автоматично створює файли для інтеграції з Codex:

### `codex.yaml`
```yaml
language: python
entrypoint: main.py
run: |
  pip install -r requirements.txt
  python -m pytest --tb=short
  python main.py
```

### `.codex/config.json`
```json
{
  "nimda_agent": {
    "enabled": true,
    "auto_execute": false,
    "commands": [
      "статус",
      "допрацюй девплан",
      "виконай весь ДЕВ",
      "синхронізація"
    ]
  }
}
```

## 📊 Моніторинг та логування

### Логи
Агент створює детальні логи у папці `nimda_logs/`:

```
nimda_logs/
├── nimda_agent_20241211.log
└── error_details.log
```

### CHANGELOG.md
Автоматично ведеться журнал усіх змін:

```markdown
# Журнал змін

## [Нереалізовано]

### Додано
- [x] Реалізовано базову функціональність (2024-12-11 14:30)
- [ ] Додати нові функції

### Виправлено
- [x] Виправлено помилку у парсингі (2024-12-11 15:15)
```

## 🔄 GitHub Actions інтеграція

Агент автоматично створює GitHub workflows:

### `.github/workflows/nimda-agent.yml`
```yaml
name: NIMDA Agent Auto-Development

on:
  schedule:
    - cron: '0 */6 * * *'  # Кожні 6 годин
  workflow_dispatch:
    inputs:
      command:
        description: 'NIMDA Agent Command'
        required: true
        default: 'статус'

jobs:
  nimda-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run NIMDA Agent
        run: python nimda_agent_plugin/run_nimda_agent.py --command "${{ github.event.inputs.command }}"
```

## 🧩 Розширення функціональності

### Додавання нових типів проектів

Редагуйте `project_initializer.py`:

```python
self.project_templates["my_framework"] = {
    "extensions": [".myext"],
    "files": ["config.my", "main.my"],
    "directories": ["src", "lib"],
    "workflows": ["my-ci.yml"]
}
```

### Додавання нових команд

Редагуйте `command_processor.py`:

```python
self.command_patterns["my_command"] = [
    r"моя команда",
    r"my command"
]
```

## 🔍 Приклади використання

### Автоматична розробка веб-додатку

```bash
# 1. Ініціалізація
mkdir my-web-app && cd my-web-app
python ../nimda_agent_plugin/run_nimda_agent.py --init

# 2. Налаштування GitHub
python nimda_agent_plugin/run_nimda_agent.py --setup-github https://github.com/user/my-web-app.git

# 3. Запуск автоматичної розробки
python nimda_agent_plugin/run_nimda_agent.py --command "виконай весь ДЕВ"
```

### Підтримка існуючого проекту

```bash
# 1. Додання агента до існуючого проекту
cp -r /path/to/nimda_agent_plugin .

# 2. Створення плану розробки
cat > DEV_PLAN.md << EOF
# План розвитку проекту

### 1. Рефакторинг
- [ ] Покращити архітектуру
- [ ] Оптимізувати код
- [ ] Додати тести

### 2. Нові функції
- [ ] Реалізувати API v2
- [ ] Додати аутентифікацію
- [ ] Створити admin панель
EOF

# 3. Запуск агента
python nimda_agent_plugin/run_nimda_agent.py --daemon
```

## 🐛 Усунення проблем

### Агент не запускається
```bash
# Перевірка Python версії (потрібен 3.8+)
python --version

# Встановлення залежностей
pip install requests pyyaml pathlib

# Запуск з детальним виводом
python nimda_agent_plugin/run_nimda_agent.py --verbose
```

### Git помилки
```bash
# Ініціалізація Git репозиторію
git init
git config user.name "NIMDA Agent"
git config user.email "nimda@example.com"

# Запуск агента
python nimda_agent_plugin/run_nimda_agent.py --command "синхронізація"
```

### DEV_PLAN.md не обробляється
```bash
# Перевірка формату файлу
python nimda_agent_plugin/run_nimda_agent.py --command "допрацюй девплан"

# Ручна перевірка парсингу
python -c "
from nimda_agent_plugin.dev_plan_manager import DevPlanManager
from pathlib import Path
manager = DevPlanManager(Path('.'))
print(manager.get_plan_status())
"
```

## 📞 Підтримка

- **Issues**: Створюйте issue у GitHub репозиторії
- **Документація**: Дивіться файли в папці плагіна
- **Приклади**: Дивіться папку `examples/` (якщо доступна)

## 📄 Ліцензія

MIT License - дивіться файл LICENSE для деталей.

## 🤝 Внесок у розробку

1. Fork репозиторій
2. Створіть feature branch (`git checkout -b feature/amazing-feature`)
3. Зробіть commit змін (`git commit -m 'Add amazing feature'`)
4. Push до branch (`git push origin feature/amazing-feature`)
5. Відкрийте Pull Request

---

🤖 **NIMDA Agent Plugin** - Ваш персональний помічник у розробці ПЗ!
