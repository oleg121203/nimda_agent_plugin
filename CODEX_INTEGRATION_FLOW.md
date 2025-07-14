# 🔗 Як працює інтеграція Codex сесії з локальним монітором

## 📋 **Схема роботи:**

### 1. **GPT Чат** → **command_processor.py**
```python
# При отриманні будь-якої команди в GPT чаті:
def process(self, command: str):
    # 🔥 АВТОМАТИЧНО створює файли сесії:
    self._mark_codex_session_active()
```

### 2. **Файли сесії** (створюються автоматично):
- `.codex_session_active` - час створення сесії
- `.last_codex_activity` - остання активність (timestamp)

### 3. **Локальний монітор** перевіряє кожні 30 сек:
```bash
# codex_monitor.sh
check_codex_session() {
    # Якщо файл існує і менше 60 сек → 🟢 активна
    # Якщо файл старше 60 сек → 🔴 таймаут
    # Якщо файл не існує → 🟡 немає сесії
}
```

## 🚀 **Послідовність дій:**

1. **У GPT чаті:** `run full dev`
2. **command_processor.py** створює файли сесії ✅
3. **Монітор детектує:** `🟢 Codex session is active`
4. **Якщо GPT сесія розривається:** файли стають старими
5. **Через 1 хвилину:** `🔴 Session timed out → local execution`
6. **Локальний запуск:** `python3 auto_dev_runner.py .`

## 📁 **Файли створюються:**

```bash
# Перевірити:
ls -la .codex_session* .last_codex_activity

# Якщо є файли → сесія була активна
# Якщо немає → ще не було команд з GPT
```

## ✅ **Тестування:**

```bash
# 1. Протестувати створення сесії:
python3 test_codex_session.py

# 2. Перевірити реакцію монітора:
./codex_monitor.sh status

# 3. Переглянути логи:
tail -f .codex_monitor.log
```

**Тепер система повністю інтегрована!** 🎉
