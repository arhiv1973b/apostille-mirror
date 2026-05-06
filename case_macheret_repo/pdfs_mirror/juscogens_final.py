import os, fitz, re

def deep_audit(root_dir, targets):
    print("=== TI-ULA: ГЛОБАЛЬНЫЙ ФОРЕНЗИК-АУДИТ (IDNP + UN/UNIX) ===")
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('_fixed.pdf'):
                file_path = os.path.join(root, file)
                try:
                    doc = fitz.open(file_path)
                    for page_num, page in enumerate(doc, start=1):
                        text = page.get_text()
                        for target in targets:
                            if target in text:
                                pos = text.find(target)
                                start, end = max(0, pos-60), min(len(text), pos+60)
                                context = text[start:end].replace("\n", " ")
                                # Вывод в стандартный поток для перехвата PowerShell
                                print(f"✅ НАЙДЕНО: {target} | Стр. {page_num} | Файл: {file}")
                                print(f"   [Context]: ...{context}...")
                    doc.close()
                except: pass

if __name__ == '__main__':
    case_targets = ["2000001159455", "2000001159555", "2000001159655", "UNIX", "UN "]
    deep_audit("/app/repo/data", case_targets)