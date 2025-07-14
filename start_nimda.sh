#!/bin/bash

# NIMDA Agent Quick Start Script
# Швидкий запуск NIMDA Agent з різними режимами

set -e

# Colors для виводу
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Функція для виводу заголовка
print_header() {
    echo -e "${CYAN}"
    echo "🤖 NIMDA Agent - Quick Start"
    echo "============================"
    echo -e "${NC}"
}

# Функція для виводу допомоги
show_help() {
    echo -e "${BLUE}Доступні режими:${NC}"
    echo -e "  ${GREEN}gui${NC}        - Запустити GUI інтерфейс"
    echo -e "  ${GREEN}status${NC}     - Перевірка статусу системи"
    echo -e "  ${GREEN}health${NC}     - Запустити health dashboard"
    echo -e "  ${GREEN}interactive${NC} - Інтерактивний режим"
    echo -e "  ${GREEN}dev${NC}        - Автоматична розробка"
    echo -e "  ${GREEN}analyze${NC}    - Глибокий аналіз системи"
    echo ""
    echo -e "${YELLOW}Приклади:${NC}"
    echo -e "  ${CYAN}./start_nimda.sh gui${NC}                    # GUI режим"
    echo -e "  ${CYAN}./start_nimda.sh status${NC}                 # Статус системи"
    echo -e "  ${CYAN}./start_nimda.sh health 8080${NC}            # Health dashboard на порті 8080"
    echo -e "  ${CYAN}./start_nimda.sh dev 3${NC}                  # 3 цикли розробки"
    echo ""
}

# Перевірка Python 3.11
check_python() {
    if ! command -v python3.11 &> /dev/null; then
        echo -e "${RED}❌ Python 3.11 не знайдено${NC}"
        echo -e "${YELLOW}💡 Встановіть Python 3.11 або використовуйте python3${NC}"
        exit 1
    fi
}

# Основна логіка
main() {
    print_header
    check_python
    
    # Перейти в директорію NIMDA
    cd "$(dirname "$0")"
    
    MODE="${1:-interactive}"
    
    case $MODE in
        gui)
            echo -e "${GREEN}🚀 Запуск GUI інтерфейсу...${NC}"
            python3.11 GUI/nimda_gui.py
            ;;
        status)
            echo -e "${GREEN}🔍 Перевірка статусу системи...${NC}"
            python3.11 nimda_app.py --status
            ;;
        health)
            PORT="${2:-8080}"
            echo -e "${GREEN}🌐 Запуск health dashboard на порті $PORT...${NC}"
            python3.11 nimda_app.py --health --port $PORT
            ;;
        interactive)
            echo -e "${GREEN}🎯 Інтерактивний режим...${NC}"
            python3.11 nimda_app.py --interactive
            ;;
        dev)
            CYCLES="${2:-1}"
            echo -e "${GREEN}🤖 Автоматична розробка ($CYCLES циклів)...${NC}"
            python3.11 nimda_app.py --auto-dev --cycles $CYCLES
            ;;
        analyze)
            echo -e "${GREEN}🧠 Глибокий аналіз системи...${NC}"
            python3.11 nimda_app.py --analyze
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            echo -e "${RED}❌ Невідомий режим: $MODE${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Обробка сигналу переривання
trap 'echo -e "\n${YELLOW}👋 NIMDA Agent зупинено${NC}"; exit 0' INT

# Запуск основної функції
main "$@"
