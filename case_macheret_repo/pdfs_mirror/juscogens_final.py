import os, fitz

def deep_audit(root_dir, targets):
    print(f"--- СТАРТ СКАНЕРА: Директория {root_dir} ---")
    
    files_found = 0
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                files_found += 1
                # Выводим каждый файл, чтобы ты видел работу в реальном времени
                print(f"🔍 Анализ: {file}")
                
                file_path = os.path.join(root, file)
                try:
                    doc = fitz.open(file_path)
                    for page_num, page in enumerate(doc, start=1):
                        text = page.get_text()
                        for target in targets:
                            if target in text:
                                print(f"    🔥 НАЙДЕН УЗЕЛ [{target}] | Стр. {page_num}")
                    doc.close()
                except Exception as e:
                    print(f"    ❌ Ошибка доступа: {file} ({e})")
    
    print(f"--- ИТОГ: Обработано файлов: {files_found} ---")

if __name__ == '__main__':
    # Оставляем самые "грязные" маркеры для быстрой проверки
    case_targets = ["2000001159555", "UNIX", "12000", "16000", "25.210.250", "40", "80"]
    deep_audit("/app/repo/data", case_targets)