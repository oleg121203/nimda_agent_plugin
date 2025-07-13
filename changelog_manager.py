"""Changelog manager for maintaining CHANGELOG.md"""

import re
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import logging


class ChangelogManager:
    """Manager for handling the CHANGELOG.md file

    Features:
    - Add change log entries
    - Mark completed tasks
    - Update project status
    - Keep a Changelog format support
    """

    def __init__(self, project_path: Path):
        """
        Ініціалізація менеджера журналу змін

        Args:
            project_path: Шлях до проекту
        """
        self.project_path = project_path
        self.changelog_file = project_path / "CHANGELOG.md"
        self.logger = logging.getLogger('ChangelogManager')

        # Перевірка існування файлу
        if not self.changelog_file.exists():
            self._create_initial_changelog()

    def _create_initial_changelog(self):
        """Створення початкового CHANGELOG.md"""
        initial_content = f'''# Журнал змін

Всі значущі зміни цього проекту будуть документовані в цьому файлі.

Формат базується на [Keep a Changelog](https://keepachangelog.com/uk/1.0.0/),
і цей проект дотримується [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Нереалізовано]

### Додано
- [ ] Початкове налаштування проекту

### Змінено
- [ ] Оновлення документації

### Виправлено
- [ ] Початкові помилки

## [1.0.0] - {datetime.now().strftime('%Y-%m-%d')}

### Додано
- [x] Ініціалізація проекту NIMDA Agent
- [x] Створення структури файлів
- [x] Налаштування автоматизації

---

**Легенда:**
- [x] Виконано
- [ ] Не виконано
- [-] Скасовано

*Цей журнал автоматично оновлюється NIMDA Agent.*
'''

        try:
            self.changelog_file.write_text(initial_content, encoding='utf-8')
            self.logger.info("Створено початковий CHANGELOG.md")
        except Exception as e:
            self.logger.error(f"Помилка створення CHANGELOG.md: {e}")

    def add_entry(self, message: str, category: str = "Додано", completed: bool = True) -> bool:
        """
        Додавання нового запису до журналу змін

        Args:
            message: Повідомлення про зміну
            category: Категорія зміни (Додано, Змінено, Виправлено)
            completed: Чи є задача виконаною

        Returns:
            True якщо запис додано успішно
        """
        try:
            # Читання поточного вмісту
            if not self.changelog_file.exists():
                self._create_initial_changelog()

            content = self.changelog_file.read_text(encoding='utf-8')

            # Пошук секції "Нереалізовано"
            unreleased_pattern = r'## \[Нереалізовано\]'
            match = re.search(unreleased_pattern, content)

            if not match:
                self.logger.warning("Секція [Нереалізовано] не знайдена")
                return False

            # Пошук відповідної категорії
            category_pattern = f'### {category}'
            category_start = content.find(category_pattern, match.start())

            if category_start == -1:
                # Якщо категорія не знайдена, додаємо її
                self._add_category_section(category, message, completed)
                return True

            # Знаходимо місце для вставки нового запису
            lines = content.split('\n')
            category_line_idx = None

            for i, line in enumerate(lines):
                if line.strip() == f"### {category}":
                    category_line_idx = i
                    break

            if category_line_idx is None:
                return False

            # Форматування нового запису
            status_mark = "[x]" if completed else "[ ]"
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            new_entry = f"- {status_mark} {message} ({timestamp})"

            # Вставка нового запису після заголовка категорії
            lines.insert(category_line_idx + 1, new_entry)

            # Збереження оновленого вмісту
            updated_content = '\n'.join(lines)
            self.changelog_file.write_text(updated_content, encoding='utf-8')

            self.logger.info(f"Додано запис до CHANGELOG: {message}")
            return True

        except Exception as e:
            self.logger.error(f"Помилка додавання запису до CHANGELOG: {e}")
            return False

    def _add_category_section(self, category: str, message: str, completed: bool):
        """Додавання нової секції категорії"""
        try:
            content = self.changelog_file.read_text(encoding='utf-8')

            # Пошук секції "Нереалізовано"
            unreleased_pattern = r'(## \[Нереалізовано\])'
            match = re.search(unreleased_pattern, content)

            if not match:
                return False

            # Створення нової секції
            status_mark = "[x]" if completed else "[ ]"
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
            new_section = f'''
### {category}
- {status_mark} {message} ({timestamp})
'''

            # Вставка після заголовка "Нереалізовано"
            insert_pos = match.end()
            updated_content = content[:insert_pos] + new_section + content[insert_pos:]

            self.changelog_file.write_text(updated_content, encoding='utf-8')
            self.logger.info(f"Додано нову категорію '{category}' до CHANGELOG")

        except Exception as e:
            self.logger.error(f"Помилка додавання категорії: {e}")

    def mark_task_completed(self, task_info: Dict[str, Any]) -> bool:
        """
        Відмітка задачі як виконаної

        Args:
            task_info: Інформація про задачу

        Returns:
            True якщо задачу відмічено успішно
        """
        try:
            task_title = task_info.get("title", "Невідома задача")
            task_number = task_info.get("number", "N/A")

            # Додавання запису про виконання задачі
            message = f"Виконано задачу #{task_number}: {task_title}"

            # Додаємо до категорії "Виконано"
            self.add_entry(message, "Виконано", completed=True)

            # Якщо є підзадачі, додаємо їх теж
            subtasks = task_info.get("subtasks", [])
            completed_subtasks = [st for st in subtasks if st.get("completed", False)]

            if completed_subtasks:
                for subtask in completed_subtasks:
                    subtask_message = f"  └─ {subtask['text']}"
                    self.add_entry(subtask_message, "Виконано", completed=True)

            return True

        except Exception as e:
            self.logger.error(f"Помилка відмітки задачі: {e}")
            return False

    def update_version(self, version: str, release_notes: Optional[List[str]] = None) -> bool:
        """
        Створення нової версії в журналі змін

        Args:
            version: Номер версії
            release_notes: Додаткові нотатки про реліз

        Returns:
            True якщо версію створено успішно
        """
        try:
            content = self.changelog_file.read_text(encoding='utf-8')

            # Перенесення "Нереалізовано" до нової версії
            current_date = datetime.now().strftime('%Y-%m-%d')

            # Заміна [Нереалізовано] на версію
            version_header = f"## [{version}] - {current_date}"
            updated_content = re.sub(
                r'## \[Нереалізовано\]',
                f"## [Нереалізовано]\n\n### Додано\n- [ ] Нові функції\n\n### Змінено\n- [ ] Оновлення\n\n### Виправлено\n- [ ] Помилки\n\n{version_header}",
                content,
                count=1
            )

            # Додавання приміток до релізу
            if release_notes:
                notes_section = "\n\n**Примітки до релізу:**\n"
                for note in release_notes:
                    notes_section += f"- {note}\n"

                # Вставка після заголовка версії
                version_pos = updated_content.find(version_header) + len(version_header)
                updated_content = updated_content[:version_pos] + notes_section + updated_content[version_pos:]

            self.changelog_file.write_text(updated_content, encoding='utf-8')

            self.logger.info(f"Створено версію {version} в CHANGELOG")
            return True

        except Exception as e:
            self.logger.error(f"Помилка створення версії: {e}")
            return False

    def get_changelog_stats(self) -> Dict[str, Any]:
        """
        Отримання статистики журналу змін

        Returns:
            Статистика журналу змін
        """
        try:
            if not self.changelog_file.exists():
                return {
                    "exists": False,
                    "message": "CHANGELOG.md не існує"
                }

            content = self.changelog_file.read_text(encoding='utf-8')

            # Підрахунок записів
            completed_pattern = r'- \[x\]'
            pending_pattern = r'- \[ \]'
            cancelled_pattern = r'- \[-\]'

            completed_count = len(re.findall(completed_pattern, content))
            pending_count = len(re.findall(pending_pattern, content))
            cancelled_count = len(re.findall(cancelled_pattern, content))

            # Підрахунок версій
            version_pattern = r'## \[(\d+\.\d+\.\d+)\]'
            versions = re.findall(version_pattern, content)

            # Останнє оновлення
            lines = content.split('\n')
            last_modified = None

            for line in lines:
                if '(' in line and ')' in line:
                    # Пошук дати в дужках
                    date_match = re.search(r'\((\d{4}-\d{2}-\d{2} \d{2}:\d{2})\)', line)
                    if date_match:
                        last_modified = date_match.group(1)
                        break

            return {
                "exists": True,
                "completed_tasks": completed_count,
                "pending_tasks": pending_count,
                "cancelled_tasks": cancelled_count,
                "total_tasks": completed_count + pending_count + cancelled_count,
                "versions": versions,
                "latest_version": versions[0] if versions else None,
                "last_modified": last_modified,
                "file_size": len(content),
                "lines_count": len(lines)
            }

        except Exception as e:
            self.logger.error(f"Помилка отримання статистики: {e}")
            return {
                "exists": False,
                "error": str(e),
                "message": "Помилка читання CHANGELOG.md"
            }

    def search_entries(self, query: str) -> List[Dict[str, Any]]:
        """
        Пошук записів у журналі змін

        Args:
            query: Пошуковий запит

        Returns:
            Список знайдених записів
        """
        try:
            if not self.changelog_file.exists():
                return []

            content = self.changelog_file.read_text(encoding='utf-8')
            lines = content.split('\n')

            results = []
            current_section = None
            current_category = None

            for i, line in enumerate(lines):
                # Визначення секцій
                if line.startswith('## ['):
                    current_section = line.strip()
                    continue

                if line.startswith('### '):
                    current_category = line.strip()[4:]  # Видаляємо "### "
                    continue

                # Пошук у записах
                if line.startswith('- [') and query.lower() in line.lower():
                    # Визначення статусу
                    status = "completed" if "[x]" in line else "pending" if "[ ]" in line else "cancelled"

                    # Витягування тексту та дати
                    text_match = re.search(r'- \[.\] (.+)', line)
                    text = text_match.group(1) if text_match else line

                    date_match = re.search(r'\((\d{4}-\d{2}-\d{2} \d{2}:\d{2})\)', text)
                    date = date_match.group(1) if date_match else None

                    if date:
                        text = re.sub(r' \(\d{4}-\d{2}-\d{2} \d{2}:\d{2}\)', '', text)

                    results.append({
                        "line_number": i + 1,
                        "section": current_section,
                        "category": current_category,
                        "text": text.strip(),
                        "status": status,
                        "date": date,
                        "full_line": line.strip()
                    })

            return results

        except Exception as e:
            self.logger.error(f"Помилка пошуку в CHANGELOG: {e}")
            return []

    def cleanup_changelog(self) -> bool:
        """
        Очищення та реорганізація журналу змін

        Returns:
            True якщо очищення виконано успішно
        """
        try:
            if not self.changelog_file.exists():
                return False

            content = self.changelog_file.read_text(encoding='utf-8')

            # Видалення порожніх рядків підряд
            lines = content.split('\n')
            cleaned_lines = []
            prev_empty = False

            for line in lines:
                is_empty = line.strip() == ''

                if not (is_empty and prev_empty):
                    cleaned_lines.append(line)

                prev_empty = is_empty

            # Сортування записів у кожній категорії за датою
            cleaned_content = self._sort_entries_by_date('\n'.join(cleaned_lines))

            # Збереження очищеного вмісту
            self.changelog_file.write_text(cleaned_content, encoding='utf-8')

            self.logger.info("CHANGELOG.md очищено та реорганізовано")
            return True

        except Exception as e:
            self.logger.error(f"Помилка очищення CHANGELOG: {e}")
            return False

    def _sort_entries_by_date(self, content: str) -> str:
        """Сортування записів за датою в кожній категорії"""
        try:
            lines = content.split('\n')
            result_lines = []
            current_entries = []
            in_category = False

            for line in lines:
                if line.startswith('### '):
                    # Збереження попередніх відсортованих записів
                    if current_entries:
                        sorted_entries = self._sort_entry_list(current_entries)
                        result_lines.extend(sorted_entries)
                        current_entries = []

                    result_lines.append(line)
                    in_category = True

                elif line.startswith('- [') and in_category:
                    current_entries.append(line)

                else:
                    # Збереження попередніх відсортованих записів
                    if current_entries:
                        sorted_entries = self._sort_entry_list(current_entries)
                        result_lines.extend(sorted_entries)
                        current_entries = []

                    result_lines.append(line)
                    in_category = False

            # Збереження останніх записів
            if current_entries:
                sorted_entries = self._sort_entry_list(current_entries)
                result_lines.extend(sorted_entries)

            return '\n'.join(result_lines)

        except Exception:
            return content  # Повернення оригінального вмісту при помилці

    def _sort_entry_list(self, entries: List[str]) -> List[str]:
        """Сортування списку записів за датою"""
        def extract_date(entry: str) -> datetime:
            date_match = re.search(r'\((\d{4}-\d{2}-\d{2} \d{2}:\d{2})\)', entry)
            if date_match:
                try:
                    return datetime.strptime(date_match.group(1), '%Y-%m-%d %H:%M')
                except ValueError:
                    pass
            return datetime.min

        return sorted(entries, key=extract_date, reverse=True)  # Новіші записи зверху
