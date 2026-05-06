import sys
import hashlib
import os
import pdfplumber

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def extract_and_deduplicate(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Ошибка: Файл '{pdf_path}' не найден.")
        return

    print(f"\n--- АУДИТ ФАЙЛА: {pdf_path} ---")
    
    file_hash = calculate_sha256(pdf_path)
    print(f"SHA-256 VERIFIER: {file_hash}")
    
    seen_lines = set()
    clean_text = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    for line in text.split('\n'):
                        line = line.strip()
                        if line and line not in seen_lines:
                            clean_text.append(line)
                            seen_lines.add(line)
        
        report_name = pdf_path.replace(".pdf", "_forensic_report.txt")
        with open(report_name, "w", encoding="utf-8") as report:
            report.write(f"FILE: {pdf_path}\n")
            report.write(f"HASH: {file_hash}\n")
            report.write("-" * 30 + "\n\n")
            report.write("\n".join(clean_text))
        
        print(f"✅ Успешно: извлечено {len(clean_text)} уникальных строк.")
        print(f"📄 Forensic-отчет сформирован: {report_name}")
    except Exception as e:
        print(f"❌ Ошибка при обработке: {e}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Использование: python extract_pdf_with_deduplication_fixed.py \"имя_файла.pdf\"")
    else:
        extract_and_deduplicate(sys.argv[1])
