#!/bin/bash
set -e

# Цветовая схема
RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 1. Список 13 критических файлов «VOID» (Evidence Integrity List)
CRITICAL_FILES=(
    "APOSTILLE_FRAUD_REPORT.md"
    "ECHR_SUBMISSION.md"
    "NOTICE_OF_INTEGRITY.md"
    "docs/muruyan_node/final_offset_notification.md"
    "docs/damages/final_registry_2026.md"
    "docs/claim/ru.md"
    "docs/claim/identity_warfare.md"
    "docs/claim/ukraine_migrant_fraud.md"
    "docs/claim/cc_sabotage.md"
    "docs/property_theft/eviction_blockade_2003_2021.md"
    "bot_audit/evidence_of_service/jcc_final_dispatch_log.md"
    "docs/legal_foundation/echr_ratification_1997.md"
    "docs/denunciation/morozan_void_act.md"
)

echo -e "${CYAN}[→] ЗАПУСК АВТОМАТИЧЕСКОГО АУДИТА ЦЕЛОСТНОСТИ...${NC}"

# 2. Проверка наличия файлов
MISSING_FILES=0
for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}[ERR] КРИТИЧЕСКИЙ ФАЙЛ ОТСУТСТВУЕТ: $file${NC}"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    echo -e "${RED}------------------------------------------------------------${NC}"
    echo -e "${RED}ДЕПЛОЙ ЗАБЛОКИРОВАН: Обнаружено отсутствие $MISSING_FILES улик!${NC}"
    echo -e "${RED}Восстановите файлы перед попыткой пуша.${NC}"
    exit 1
fi

# 3. Генерация отчета о целостности (Integrity Report)
REPORT_FILE="bot_audit/integrity_report_$(date '+%Y%m%d').md"
echo "# 🛡️ ОТЧЕТ О ЦЕЛОСТНОСТИ ДОКАЗАТЕЛЬСТВ (JUS COGENS)" > $REPORT_FILE
echo "Дата аудита: $(date '+%Y-%m-%d %H:%M:%S')" >> $REPORT_FILE
echo "Статус: ВЕРИФИЦИРОВАНО" >> $REPORT_FILE
echo -e "\n## ХЕШ-СУММЫ SHA-256" >> $REPORT_FILE
for file in "${CRITICAL_FILES[@]}"; do
    sha256sum "$file" >> $REPORT_FILE
done

echo -e "${GREEN}[✓] Аудит пройден. 13/13 файлов на месте. Отчет создан: $REPORT_FILE${NC}"

# 4. Процедура Git
git add .
git commit -m "legal(integrity): automated audit success - evidence vault locked [$(date '+%Y-%m-%d')]" || echo "Нет изменений для коммита"
git push origin master

echo -e "${YELLOW}------------------------------------------------------------${NC}"
echo -e "${GREEN}[✓] СТРАТЕГИЯ 9 АПРЕЛЯ ЗАЩИЩЕНА. ДЕПЛОЙ ЗАВЕРШЕН.${NC}"
