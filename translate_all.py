#!/usr/bin/env python3
"""
Automatic Translation Script for NIMDA Agent
Translates all Ukrainian text to English for professional codebase
"""

import logging
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class NIMDATranslator:
    """Comprehensive translator for NIMDA codebase"""

    def __init__(self, root_path: Path):
        self.root_path = Path(root_path)
        self.translations = self._load_translations()
        self.backup_dir = self.root_path / ".translation_backups"
        self.backup_dir.mkdir(exist_ok=True)

        # Files to process
        self.target_files = [
            "git_manager.py",
            "dev_plan_manager.py",
            "changelog_manager.py",
            "agent.py",
            "command_processor.py",
            "project_initializer.py",
            "run_nimda_agent.py",
            "setup_env.py",
            "main.py",
        ]

        # Pattern for Ukrainian text detection
        self.ukrainian_pattern = re.compile(r"[а-щьюяіїєґА-ЩЬЮЯІЇЄҐ]")

    def _load_translations(self) -> Dict[str, str]:
        """Load comprehensive Ukrainian to English translations"""
        return {
            # Common error messages
            "Помилка": "Error",
            "помилка": "error",
            "Помилки": "Errors",
            "помилки": "errors",
            "Увага": "Warning",
            "увага": "warning",
            "Успішно": "Successfully",
            "успішно": "successfully",
            "Завантаження": "Loading",
            "завантаження": "loading",
            "Збереження": "Saving",
            "збереження": "saving",
            "Створення": "Creating",
            "створення": "creating",
            "Оновлення": "Updating",
            "оновлення": "updating",
            "Видалення": "Deleting",
            "видалення": "deleting",
            "Відправка": "Sending",
            "відправка": "sending",
            "Отримання": "Receiving",
            "отримання": "receiving",
            # Git operations
            "репозиторій": "repository",
            "репозиторію": "repository",
            "Репозиторій": "Repository",
            "гілка": "branch",
            "гілки": "branch",
            "Гілка": "Branch",
            "коміт": "commit",
            "коміту": "commit",
            "Коміт": "Commit",
            "зміни": "changes",
            "змін": "changes",
            "Зміни": "Changes",
            "віддалений": "remote",
            "віддаленого": "remote",
            "Віддалений": "Remote",
            "локальні": "local",
            "локальних": "local",
            "Локальні": "Local",
            "синхронізація": "synchronization",
            "синхронізації": "synchronization",
            "Синхронізація": "Synchronization",
            "резервна": "backup",
            "резервний": "backup",
            "резервну": "backup",
            "Резервна": "Backup",
            "Резервний": "Backup",
            # File operations
            "файл": "file",
            "файлу": "file",
            "файли": "files",
            "файлів": "files",
            "Файл": "File",
            "Файли": "Files",
            "директорія": "directory",
            "директорії": "directory",
            "Директорія": "Directory",
            "шлях": "path",
            "Шлях": "Path",
            # Status and states
            "статус": "status",
            "Статус": "Status",
            "стан": "state",
            "Стан": "State",
            "готово": "ready",
            "Готово": "Ready",
            "завершено": "completed",
            "Завершено": "Completed",
            "виконано": "executed",
            "Виконано": "Executed",
            "активний": "active",
            "Активний": "Active",
            # Development terms
            "задача": "task",
            "задачі": "task",
            "Задача": "Task",
            "Задачі": "Tasks",
            "план": "plan",
            "плану": "plan",
            "План": "Plan",
            "проект": "project",
            "проекту": "project",
            "Проект": "Project",
            "розробка": "development",
            "розробки": "development",
            "Розробка": "Development",
            "тестування": "testing",
            "Тестування": "Testing",
            "документація": "documentation",
            "Документація": "Documentation",
            "налаштування": "configuration",
            "Налаштування": "Configuration",
            "ініціалізація": "initialization",
            "Ініціалізація": "Initialization",
            # Time and dates
            "година": "hour",
            "години": "hours",
            "хвилина": "minute",
            "хвилини": "minutes",
            "секунда": "second",
            "секунди": "seconds",
            "день": "day",
            "дні": "days",
            "тиждень": "week",
            "тижні": "weeks",
            "місяць": "month",
            "місяці": "months",
            # Actions
            "виконати": "execute",
            "запустити": "start",
            "зупинити": "stop",
            "перезапустити": "restart",
            "підключити": "connect",
            "відключити": "disconnect",
            "налаштувати": "configure",
            "встановити": "install",
            "видалити": "delete",
            "оновити": "update",
            "перевірити": "check",
            "знайти": "find",
            "створити": "create",
            "зберегти": "save",
            "завантажити": "load",
            # System terms
            "система": "system",
            "системи": "system",
            "Система": "System",
            "сервіс": "service",
            "Сервіс": "Service",
            "агент": "agent",
            "Агент": "Agent",
            "клієнт": "client",
            "Клієнт": "Client",
            "сервер": "server",
            "Сервер": "Server",
            "мережа": "network",
            "Мережа": "Network",
            "підключення": "connection",
            "Підключення": "Connection",
            # Specific translations for this codebase
            "не існує": "does not exist",
            "не знайдено": "not found",
            "не вдалося": "failed to",
            "Не вдалося": "Failed to",
            "не ініціалізовано": "not initialized",
            "не налаштовано": "not configured",
            "завершена": "completed",
            "з помилками": "with errors",
            "успішне": "successful",
            "невдале": "failed",
            "критична": "critical",
            "Критична": "Critical",
            # Dev plan specific
            "Додано": "Added",
            "Змінено": "Changed",
            "Виправлено": "Fixed",
            "Видалено": "Removed",
            "Нереалізовано": "Unreleased",
            "виконання": "execution",
            "Виконання": "Execution",
            "обробка": "processing",
            "Обробка": "Processing",
            # Changelog specific
            "журнал змін": "changelog",
            "Журнал змін": "Changelog",
            "запис": "entry",
            "записи": "entries",
            "Запис": "Entry",
            "категорія": "category",
            "Категорія": "Category",
            "версія": "version",
            "Версія": "Version",
            "очищення": "cleanup",
            "Очищення": "Cleanup",
            "пошук": "search",
            "Пошук": "Search",
            "статистика": "statistics",
            "Статистика": "Statistics",
            # Specific error patterns
            "Помилка створення репозиторію": "Error creating repository",
            "Помилка Git": "Git error",
            "Помилка отримання статусу": "Error getting status",
            "Помилка виконання команди": "Error executing command",
            "Помилка створення коміту": "Error creating commit",
            "Помилка відправки змін": "Error pushing changes",
            "Помилка отримання змін": "Error pulling changes",
            "Помилка синхронізації": "Synchronization error",
            "Помилка створення резервної гілки": "Error creating backup branch",
            "Помилка налаштування віддаленого репозиторію": "Error setting up remote repository",
            "Помилка виконання задачі": "Error executing task",
            "Помилка оновлення плану": "Error updating plan",
            "Помилка додавання запису до CHANGELOG": "Error adding entry to CHANGELOG",
            "Помилка створення версії": "Error creating version",
            "Помилка очищення CHANGELOG": "Error cleaning CHANGELOG",
            "Помилка пошуку в CHANGELOG": "Error searching in CHANGELOG",
            "Помилка отримання статистики": "Error getting statistics",
            "Помилка відмітки задачі": "Error marking task",
            "Помилка додавання категорії": "Error adding category",
            # Success messages
            "Зміни отримано з віддаленого репозиторію": "Changes pulled from remote repository",
            "Зміни успішно отримано": "Changes successfully received",
            "Зміни відправлено до віддаленого репозиторію": "Changes pushed to remote repository",
            "Коміт створено": "Commit created",
            "Резервну гілку створено": "Backup branch created",
            "GitHub репозиторій налаштовано": "GitHub repository configured",
            "Віддалений репозиторій налаштовано": "Remote repository configured",
            "План розширено на": "Plan expanded by",
            "CHANGELOG.md очищено та реорганізовано": "CHANGELOG.md cleaned and reorganized",
            "Додано запис до CHANGELOG": "Added entry to CHANGELOG",
            "Створено версію": "Created version",
            "Додано нову категорію": "Added new category",
            # Common phrases
            "немає змін": "no changes",
            "Немає змін для коміту": "No changes to commit",
            "всі файли": "all files",
            "поточна гілка": "current branch",
            "останній коміт": "last commit",
            "кількість комітів": "commit count",
            "попереду": "ahead",
            "позаду": "behind",
            "загальна кількість": "total count",
            "успішна операція": "successful operation",
            "невдала операція": "failed operation",
        }

    def detect_ukrainian_text(self, text: str) -> List[Tuple[int, str]]:
        """Detect Ukrainian text in a string"""
        ukrainian_matches = []
        lines = text.split("\n")

        for line_num, line in enumerate(lines, 1):
            if self.ukrainian_pattern.search(line):
                ukrainian_matches.append((line_num, line.strip()))

        return ukrainian_matches

    def translate_text(self, text: str) -> str:
        """Translate Ukrainian text to English"""
        translated = text

        # Sort by length (longest first) to avoid partial replacements
        for ukrainian, english in sorted(
            self.translations.items(), key=lambda x: len(x[0]), reverse=True
        ):
            # Word boundary replacements for exact matches
            pattern = r"\b" + re.escape(ukrainian) + r"\b"
            translated = re.sub(pattern, english, translated, flags=re.IGNORECASE)

        return translated

    def backup_file(self, file_path: Path) -> Path:
        """Create backup of file before translation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}_{timestamp}.bak"
        backup_path = self.backup_dir / backup_name

        with open(file_path, "r", encoding="utf-8") as src:
            with open(backup_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())

        logger.info(f"Backup created: {backup_path}")
        return backup_path

    def translate_file(self, file_path: Path) -> dict:
        """Translate Ukrainian text in a single file"""
        if not file_path.exists():
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            # Read original content
            with open(file_path, "r", encoding="utf-8") as f:
                original_content = f.read()

            # Detect Ukrainian text
            ukrainian_matches = self.detect_ukrainian_text(original_content)

            if not ukrainian_matches:
                return {
                    "success": True,
                    "changes": 0,
                    "message": "No Ukrainian text found",
                }

            # Create backup
            backup_path = self.backup_file(file_path)

            # Translate content
            translated_content = self.translate_text(original_content)

            # Write translated content
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(translated_content)

            # Verify changes
            changes_made = len(ukrainian_matches)

            logger.info(
                f"Translated {file_path}: {changes_made} Ukrainian text instances"
            )

            return {
                "success": True,
                "changes": changes_made,
                "backup_path": str(backup_path),
                "ukrainian_matches": ukrainian_matches[:5],  # First 5 for preview
                "message": f"Successfully translated {changes_made} Ukrainian text instances",
            }

        except Exception as e:
            logger.error(f"Error translating {file_path}: {e}")
            return {"success": False, "error": str(e)}

    def translate_all_files(self) -> dict:
        """Translate all target files"""
        results = {
            "success": True,
            "total_files": 0,
            "translated_files": 0,
            "total_changes": 0,
            "files": {},
            "errors": [],
        }

        for filename in self.target_files:
            file_path = self.root_path / filename
            results["total_files"] += 1

            logger.info(f"Processing {filename}...")

            file_result = self.translate_file(file_path)
            results["files"][filename] = file_result

            if file_result["success"]:
                if file_result["changes"] > 0:
                    results["translated_files"] += 1
                    results["total_changes"] += file_result["changes"]
            else:
                results["success"] = False
                results["errors"].append(
                    f"{filename}: {file_result.get('error', 'Unknown error')}"
                )

        return results

    def generate_translation_report(self, results: dict) -> str:
        """Generate detailed translation report"""
        report = []
        report.append("=" * 60)
        report.append("🌐 NIMDA TRANSLATION REPORT")
        report.append("=" * 60)
        report.append("📊 Summary:")
        report.append(f"  • Total files processed: {results['total_files']}")
        report.append(f"  • Files with translations: {results['translated_files']}")
        report.append(f"  • Total changes made: {results['total_changes']}")
        report.append(
            f"  • Overall success: {'✅ YES' if results['success'] else '❌ NO'}"
        )
        report.append("")

        if results["errors"]:
            report.append("❌ Errors:")
            for error in results["errors"]:
                report.append(f"  • {error}")
            report.append("")

        report.append("📁 File Details:")
        for filename, file_result in results["files"].items():
            if file_result["success"]:
                status = "✅" if file_result["changes"] > 0 else "➖"
                report.append(
                    f"  {status} {filename}: {file_result['changes']} changes"
                )

                # Show sample Ukrainian matches
                if file_result.get("ukrainian_matches"):
                    report.append("      Sample Ukrainian text found:")
                    for line_num, line in file_result["ukrainian_matches"]:
                        preview = line[:60] + "..." if len(line) > 60 else line
                        report.append(f"        Line {line_num}: {preview}")
            else:
                report.append(f"  ❌ {filename}: {file_result.get('error', 'Failed')}")

        report.append("")
        report.append(f"🔄 Backup files saved in: {self.backup_dir}")
        report.append("=" * 60)

        return "\n".join(report)

    def restore_from_backup(self, filename: str, backup_timestamp: str = None) -> bool:
        """Restore file from backup"""
        try:
            if backup_timestamp:
                backup_name = f"{filename}_{backup_timestamp}.bak"
            else:
                # Find latest backup
                backups = list(self.backup_dir.glob(f"{filename}_*.bak"))
                if not backups:
                    logger.error(f"No backups found for {filename}")
                    return False
                backup_name = sorted(backups)[-1].name

            backup_path = self.backup_dir / backup_name
            target_path = self.root_path / filename

            if not backup_path.exists():
                logger.error(f"Backup not found: {backup_path}")
                return False

            with open(backup_path, "r", encoding="utf-8") as src:
                with open(target_path, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

            logger.info(f"Restored {filename} from {backup_name}")
            return True

        except Exception as e:
            logger.error(f"Error restoring {filename}: {e}")
            return False


def main():
    """Main execution function"""
    print("🌐 NIMDA Automatic Translation Tool")
    print("=" * 50)

    # Get root path
    if len(sys.argv) > 1:
        root_path = Path(sys.argv[1])
    else:
        root_path = Path.cwd()

    if not root_path.exists():
        print(f"❌ Path does not exist: {root_path}")
        sys.exit(1)

    # Initialize translator
    translator = NIMDATranslator(root_path)

    # Handle command line arguments
    if len(sys.argv) > 2:
        command = sys.argv[2]

        if command == "--scan":
            # Scan for Ukrainian text only
            print("🔍 Scanning for Ukrainian text...")
            for filename in translator.target_files:
                file_path = root_path / filename
                if file_path.exists():
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    matches = translator.detect_ukrainian_text(content)
                    if matches:
                        print(
                            f"\n📄 {filename}: {len(matches)} Ukrainian text instances"
                        )
                        for line_num, line in matches[:3]:  # Show first 3
                            preview = line[:60] + "..." if len(line) > 60 else line
                            print(f"   Line {line_num}: {preview}")
            return

        elif command == "--restore":
            # Restore from backup
            if len(sys.argv) > 3:
                filename = sys.argv[3]
                success = translator.restore_from_backup(filename)
                print(
                    f"{'✅' if success else '❌'} Restore {'successful' if success else 'failed'}"
                )
            else:
                print("❌ Please specify filename to restore")
            return

    # Confirm translation
    print(f"📁 Working directory: {root_path}")
    print(f"🎯 Target files: {len(translator.target_files)}")
    print("\nFiles to translate:")
    for filename in translator.target_files:
        file_path = root_path / filename
        exists = "✅" if file_path.exists() else "❌"
        print(f"  {exists} {filename}")

    print("\n⚠️  This will modify source files (backups will be created)")
    confirm = input("Continue with translation? (y/N): ").strip().lower()

    if confirm != "y":
        print("👋 Translation cancelled")
        return

    # Perform translation
    print("\n🚀 Starting translation...")
    results = translator.translate_all_files()

    # Generate and display report
    report = translator.generate_translation_report(results)
    print("\n" + report)

    # Save report to file
    report_path = (
        root_path / f"translation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    )
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 Report saved: {report_path}")

    if results["success"]:
        print("\n🎉 Translation completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Test the translated code")
        print("   2. Run tests to ensure functionality")
        print("   3. Commit changes if everything works")
        print("   4. Use --restore filename to revert if needed")
    else:
        print("\n⚠️  Translation completed with errors. Check the report above.")


if __name__ == "__main__":
    main()
