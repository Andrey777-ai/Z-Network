import os
import re

# Пути
source_dir = os.path.expanduser("~/Рабочий стол/raw_perplexity")
output_dir = os.path.expanduser("~/Рабочий стол/extracted_code_perplexity")

os.makedirs(output_dir, exist_ok=True)

print(f"🔍 Запуск тотального сканирования: {source_dir}\n")
total_extracted = 0

for root, dirs, files in os.walk(source_dir):
    for filename in files:
        filepath = os.path.join(root, filename)
        
        # Читаем абсолютно все файлы как текст
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            # Если файл пустой, пропускаем
            if len(content.strip()) < 50:
                continue
                
            # Ищем блоки ```python ... ``` (если они есть)
            matches = re.findall(r'```(?:python|py)?\s*(.*?)```', content, re.DOTALL | re.IGNORECASE)
            
            # Если блоков с кавычками нет, но есть слово python или import, берем весь текст
            if not matches and ("python" in content.lower() or "import " in content):
                matches = [content] # Берем весь файл целиком
                
            if matches:
                session_name = os.path.basename(root) + "_" + filename
                session_name = session_name.replace(".", "_").replace(" ", "_")
                session_dir = os.path.join(output_dir, session_name)
                os.makedirs(session_dir, exist_ok=True)
                
                for i, code_block in enumerate(matches):
                    # Очищаем от мусора
                    clean_code = code_block.strip()
                    if len(clean_code) < 20:
                        continue
                        
                    code_filename = os.path.join(session_dir, f"code_{i+1}.py")
                    with open(code_filename, "w", encoding="utf-8") as code_f:
                        code_f.write(clean_code)
                    total_extracted += 1
                    
                print(f"✅ {filename}: найдено {len(matches)} блоков")

        except Exception as e:
            print(f"❌ Ошибка при чтении {filename}: {e}")

print(f"\n🎉 ГОТОВО! Всего извлечено блоков кода и текста: {total_extracted}")
