#!/bin/bash
# Автор: A©tor | STAGED_ASSEMBLY v2.0 | Обход readdirent через find
DESTINATION="gdrive:CASE-MACHERET-EVIDENCE-FINAL"
SOURCE="/mnt/h/WSL_PDFs"
LOG_FILE="migration_$(date +%Y%m%d_%H%M%S).log"
INDEX_FILE="./mirrors/evidence_index.json"
ERRORS=0
SUCCESS=0

mkdir -p ./mirrors/
echo -e "\e[36m--- TI-ULA MIGRATE v4 · find-mode ---\e[0m"
echo "Лог: $LOG_FILE"

# Считаем файлы через find (обходит readdirent)
TOTAL=$(find "$SOURCE" -maxdepth 1 -type f 2>/dev/null | wc -l)
echo "[ SCAN ] Файлов найдено: $TOTAL"

echo -e "\e[33m[ COPY ] Загрузка файлов по одному через find...\e[0m"

# find обходит проблему readdirent — передаём каждый файл отдельно
find "$SOURCE" -maxdepth 1 -type f 2>/dev/null | while IFS= read -r filepath; do
    filename=$(basename "$filepath")
    rclone copyto "$filepath" "$DESTINATION/$filename" \
        --ignore-existing \
        --drive-chunk-size 64M \
        --retries 2 \
        >> "$LOG_FILE" 2>&1

    if [ $? -eq 0 ]; then
        echo "[ OK ] $filename" | tee -a "$LOG_FILE"
        SUCCESS=$((SUCCESS + 1))
    else
        echo "[ ERR ] $filename" | tee -a "$LOG_FILE"
        ERRORS=$((ERRORS + 1))
    fi
done

echo -e "\e[32m[ DONE ] Успешно: $SUCCESS | Ошибок: $ERRORS\e[0m"

echo -e "\e[33m[ INDEX ] Построение реестра из облака...\e[0m"

rclone lsjson "$DESTINATION" -R --no-modtime > /tmp/raw_index.json 2>&1

# Проверяем что JSON валидный
if jq empty /tmp/raw_index.json 2>/dev/null; then
    jq '[.[] | {name: .Name, size: .Size, id: .ID, mime: .MimeType}]' \
        /tmp/raw_index.json > "$INDEX_FILE"
    COUNT=$(jq '. | length' "$INDEX_FILE")
    echo -e "\e[32m[ DONE ] Реестр: $COUNT объектов → $INDEX_FILE\e[0m"
else
    echo -e "\e[31m[ FAIL ] Невалидный JSON от lsjson:\e[0m"
    head -5 /tmp/raw_index.json
fi

echo -e "\e[36m--- TI-ULA ЗАВЕРШЕНО · IDNP 655 ---\e[0m"
