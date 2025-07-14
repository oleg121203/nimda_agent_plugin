"""
Changelog manager - maintaining CHANGELOG.md
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class ChangelogManager:
    """
    Manager for maintaining changelog in CHANGELOG.md file

    Functions:
    - Adding change records
    - Marking completed tasks
    - Updating project status
    - Supporting Keep a Changelog formatting
    """

    def __init__(self, project_path: Path):
        """
        Initialize changelog manager

        Args:
            project_path: Path to project
        """
        self.project_path = project_path
        self.changelog_file = project_path / "CHANGELOG.md"
        self.logger = logging.getLogger("ChangelogManager")

        # Check file existence
        if not self.changelog_file.exists():
            self._create_initial_changelog()

    def _create_initial_changelog(self):
        """Create initial CHANGELOG.md"""
        initial_content = f"""# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- [ ] Initial project setup

### Changed
- [ ] Documentation updates

### Fixed
- [ ] Initial errors

## [1.0.0] - {datetime.now().strftime("%Y-%m-%d")}

### Added
- [x] NIMDA Agent project initialization
- [x] File structure creation
- [x] Automation setup

---

**Legend:**
- [x] Completed
- [ ] Not completed
- [-] Cancelled

*This changelog is automatically updated by NIMDA Agent.*
"""

        try:
            self.changelog_file.write_text(initial_content, encoding="utf-8")
            self.logger.info("Created initial CHANGELOG.md")
        except Exception as e:
            self.logger.error(f"Error creating CHANGELOG.md: {e}")

    def add_entry(
        self, message: str, category: str = "Added", completed: bool = True
    ) -> bool:
        """
        Add new entry to changelog

        Args:
            message: Change message
            category: Change category (Added, Changed, Fixed)
            completed: Whether task is completed

        Returns:
            True if entry added successfully
        """
        try:
            # Read current content
            if not self.changelog_file.exists():
                self._create_initial_changelog()

            content = self.changelog_file.read_text(encoding="utf-8")

            # search секції "Unreleased"
            unreleased_pattern = r"## \[Unreleased\]"
            match = re.search(unreleased_pattern, content)

            if not match:
                self.logger.warning("Секція [Unreleased] не знайдена")
                return False

            # search відповідної категорії
            category_pattern = f"### {category}"
            category_start = content.find(category_pattern, match.start())

            if category_start == -1:
                # Якщо category не знайдена, додаємо її
                self._add_category_section(category, message, completed)
                return True

            # Знаходимо місце для вставки нового запису
            lines = content.split("\n")
            category_line_idx = None

            for i, line in enumerate(lines):
                if line.strip() == f"### {category}":
                    category_line_idx = i
                    break

            if category_line_idx is None:
                return False

            # Форматування нового запису
            status_mark = "[x]" if completed else "[ ]"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_entry = f"- {status_mark} {message} ({timestamp})"

            # Вставка нового запису після заголовка категорії
            lines.insert(category_line_idx + 1, new_entry)

            # Saving оновленого вмісту
            updated_content = "\n".join(lines)
            self.changelog_file.write_text(updated_content, encoding="utf-8")

            self.logger.info(f"Added entry to CHANGELOG: {message}")
            return True

        except Exception as e:
            self.logger.error(f"Error adding entry to CHANGELOG: {e}")
            return False

    def _add_category_section(self, category: str, message: str, completed: bool):
        """Додавання нової секції категорії"""
        try:
            content = self.changelog_file.read_text(encoding="utf-8")

            # search секції "Unreleased"
            unreleased_pattern = r"(## \[Unreleased\])"
            match = re.search(unreleased_pattern, content)

            if not match:
                return False

            # Creating нової секції
            status_mark = "[x]" if completed else "[ ]"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            new_section = f"""
### {category}
- {status_mark} {message} ({timestamp})
"""

            # Вставка після заголовка "Unreleased"
            insert_pos = match.end()
            updated_content = content[:insert_pos] + new_section + content[insert_pos:]

            self.changelog_file.write_text(updated_content, encoding="utf-8")
            self.logger.info(f"Added new category '{category}' до CHANGELOG")

        except Exception as e:
            self.logger.error(f"Error adding category: {e}")

    def mark_task_completed(self, task_info: Dict[str, Any]) -> bool:
        """
        Відмітка task як виконаної

        Args:
            task_info: Інформація про задачу

        Returns:
            True якщо задачу відмічено Successfully
        """
        try:
            task_title = task_info.get("title", "Невідома task")
            task_number = task_info.get("number", "N/A")

            # Додавання запису про execution task
            message = f"executed задачу #{task_number}: {task_title}"

            # Додаємо до категорії "executed"
            self.add_entry(message, "executed", completed=True)

            # Якщо є підзадачі, додаємо їх теж
            subtasks = task_info.get("subtasks", [])
            completed_subtasks = [st for st in subtasks if st.get("completed", False)]

            if completed_subtasks:
                for subtask in completed_subtasks:
                    subtask_message = f"  └─ {subtask['text']}"
                    self.add_entry(subtask_message, "executed", completed=True)

            return True

        except Exception as e:
            self.logger.error(f"Error marking task: {e}")
            return False

    def update_version(
        self, version: str, release_notes: Optional[List[str]] = None
    ) -> bool:
        """
        Creating нової версії в журналі changes

        Args:
            version: Номер версії
            release_notes: Додаткові нотатки про реліз

        Returns:
            True якщо версію створено Successfully
        """
        try:
            content = self.changelog_file.read_text(encoding="utf-8")

            # Перенесення "Unreleased" до нової версії
            current_date = datetime.now().strftime("%Y-%m-%d")

            # Заміна [Unreleased] на версію
            version_header = f"## [{version}] - {current_date}"
            updated_content = re.sub(
                r"## \[Unreleased\]",
                f"## [Unreleased]\n\n### Added\n- [ ] Нові функції\n\n### Changed\n- [ ] Updating\n\n### Fixed\n- [ ] Errors\n\n{version_header}",
                content,
                count=1,
            )

            # Додавання приміток до релізу
            if release_notes:
                notes_section = "\n\n**Примітки до релізу:**\n"
                for note in release_notes:
                    notes_section += f"- {note}\n"

                # Вставка після заголовка версії
                version_pos = updated_content.find(version_header) + len(version_header)
                updated_content = (
                    updated_content[:version_pos]
                    + notes_section
                    + updated_content[version_pos:]
                )

            self.changelog_file.write_text(updated_content, encoding="utf-8")

            self.logger.info(f"Created version {version} в CHANGELOG")
            return True

        except Exception as e:
            self.logger.error(f"Error creating version: {e}")
            return False

    def get_changelog_stats(self) -> Dict[str, Any]:
        """
        Receiving статистики журналу changes

        Returns:
            statistics журналу changes
        """
        try:
            if not self.changelog_file.exists():
                return {"exists": False, "message": "CHANGELOG.md does not exist"}

            content = self.changelog_file.read_text(encoding="utf-8")

            # Підрахунок записів
            completed_pattern = r"- \[x\]"
            pending_pattern = r"- \[ \]"
            cancelled_pattern = r"- \[-\]"

            completed_count = len(re.findall(completed_pattern, content))
            pending_count = len(re.findall(pending_pattern, content))
            cancelled_count = len(re.findall(cancelled_pattern, content))

            # Підрахунок версій
            version_pattern = r"## \[(\d+\.\d+\.\d+)\]"
            versions = re.findall(version_pattern, content)

            # Останнє Updating
            lines = content.split("\n")
            last_modified = None

            for line in lines:
                if "(" in line and ")" in line:
                    # search дати в дужках
                    date_match = re.search(r"\((\d{4}-\d{2}-\d{2} \d{2}:\d{2})\)", line)
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
                "lines_count": len(lines),
            }

        except Exception as e:
            self.logger.error(f"Error getting statistics: {e}")
            return {
                "exists": False,
                "error": str(e),
                "message": "Error читання CHANGELOG.md",
            }

    def search_entries(self, query: str) -> List[Dict[str, Any]]:
        """
        search записів у журналі changes

        Args:
            query: Пошуковий запит

        Returns:
            Список знайдених записів
        """
        try:
            if not self.changelog_file.exists():
                return []

            content = self.changelog_file.read_text(encoding="utf-8")
            lines = content.split("\n")

            results = []
            current_section = None
            current_category = None

            for i, line in enumerate(lines):
                # Визначення секцій
                if line.startswith("## ["):
                    current_section = line.strip()
                    continue

                if line.startswith("### "):
                    current_category = line.strip()[4:]  # Видаляємо "### "
                    continue

                # search у записах
                if line.startswith("- [") and query.lower() in line.lower():
                    # Визначення статусу
                    status = (
                        "completed"
                        if "[x]" in line
                        else "pending"
                        if "[ ]" in line
                        else "cancelled"
                    )

                    # Витягування тексту та дати
                    text_match = re.search(r"- \[.\] (.+)", line)
                    text = text_match.group(1) if text_match else line

                    date_match = re.search(r"\((\d{4}-\d{2}-\d{2} \d{2}:\d{2})\)", text)
                    date = date_match.group(1) if date_match else None

                    if date:
                        text = re.sub(r" \(\d{4}-\d{2}-\d{2} \d{2}:\d{2}\)", "", text)

                    results.append(
                        {
                            "line_number": i + 1,
                            "section": current_section,
                            "category": current_category,
                            "text": text.strip(),
                            "status": status,
                            "date": date,
                            "full_line": line.strip(),
                        }
                    )

            return results

        except Exception as e:
            self.logger.error(f"Error searching in CHANGELOG: {e}")
            return []

    def cleanup_changelog(self) -> bool:
        """
        cleanup та реорганізація журналу changes

        Returns:
            True якщо cleanup executed Successfully
        """
        try:
            if not self.changelog_file.exists():
                return False

            content = self.changelog_file.read_text(encoding="utf-8")

            # Deleting порожніх рядків підряд
            lines = content.split("\n")
            cleaned_lines = []
            prev_empty = False

            for line in lines:
                is_empty = line.strip() == ""

                if not (is_empty and prev_empty):
                    cleaned_lines.append(line)

                prev_empty = is_empty

            # Сортування записів у кожній категорії за датою
            cleaned_content = self._sort_entries_by_date("\n".join(cleaned_lines))

            # Saving очищеного вмісту
            self.changelog_file.write_text(cleaned_content, encoding="utf-8")

            self.logger.info("CHANGELOG.md cleaned and reorganized")
            return True

        except Exception as e:
            self.logger.error(f"Error cleaning CHANGELOG: {e}")
            return False

    def _sort_entries_by_date(self, content: str) -> str:
        """Сортування записів за датою в кожній категорії"""
        try:
            lines = content.split("\n")
            result_lines = []
            current_entries = []
            in_category = False

            for line in lines:
                if line.startswith("### "):
                    # Saving попередніх відсортованих записів
                    if current_entries:
                        sorted_entries = self._sort_entry_list(current_entries)
                        result_lines.extend(sorted_entries)
                        current_entries = []

                    result_lines.append(line)
                    in_category = True

                elif line.startswith("- [") and in_category:
                    current_entries.append(line)

                else:
                    # Saving попередніх відсортованих записів
                    if current_entries:
                        sorted_entries = self._sort_entry_list(current_entries)
                        result_lines.extend(sorted_entries)
                        current_entries = []

                    result_lines.append(line)
                    in_category = False

            # Saving останніх записів
            if current_entries:
                sorted_entries = self._sort_entry_list(current_entries)
                result_lines.extend(sorted_entries)

            return "\n".join(result_lines)

        except Exception:
            return content  # Повернення оригінального вмісту при помилці

    def _sort_entry_list(self, entries: List[str]) -> List[str]:
        """Сортування списку записів за датою"""

        def extract_date(entry: str) -> datetime:
            date_match = re.search(r"\((\d{4}-\d{2}-\d{2} \d{2}:\d{2})\)", entry)
            if date_match:
                try:
                    return datetime.strptime(date_match.group(1), "%Y-%m-%d %H:%M")
                except ValueError:
                    pass
            return datetime.min

        return sorted(entries, key=extract_date, reverse=True)  # Новіші entries зверху
