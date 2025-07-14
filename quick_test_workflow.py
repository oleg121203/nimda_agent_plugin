#!/usr/bin/env python3
"""
Швидкий тест інтерактивного воркфлоу без пауз
"""

import sys

sys.path.append("/Users/dev/Documents/nimda_agent_plugin")

from interactive_dev_workflow import InteractiveDevWorkflow


class QuickTestWorkflow(InteractiveDevWorkflow):
    """Швидкий тест без пауз"""

    def wait_for_user(self, message: str = ""):
        """Пропускаємо паузи"""
        pass

    def interactive_error_fixing_loop(self, max_iterations: int = 2):
        """Скорочений цикл виправлення помилок"""
        return super().interactive_error_fixing_loop(max_iterations)


def main():
    """Головна функція швидкого тесту"""
    print("🚀 Швидкий тест NIMDA воркфлоу (без пауз)")
    print("=" * 50)

    workflow = QuickTestWorkflow()
    success = workflow.run_full_workflow()

    if success:
        print("\n🎉 Швидкий тест завершено успішно!")
    else:
        print("\n❌ Швидкий тест завершено з помилками.")

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
