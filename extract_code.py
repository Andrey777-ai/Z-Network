import os
import json
import re

# Пути к папкам
source_dir = os.path.expanduser("~/Рабочий стол/raw_sessions")
output_dir = os.path.expanduser("~/Рабочий стол/extracted_code")

os.makedirs(output_dir, exist_ok=True)

# Регулярка для поиска кода внутри текста
code_pattern = re.compile(r'```(?:python|py)?\s*(.*?)```', re.DOTALL | re.IGNORECASE)

print(f"🔍 Сканирую папку: {source_dir}")
print(f"📁 Сохраняю код в: {output_dir}\n")

total_extracted = 0

for filename in os.listdir(source_dir):
    if not filename.endswith(".json"):
        continue
        
    filepath = os.path.join(source_dir, filename)
    
    try:
        # Загружаем JSON
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
        
        session_name = filename.replace(".json", "")
        session_dir = os.path.join(output_dir, session_name)
        
        file_blocks_count = 0
        
        # Проходим по всем сообщениям (chat_messages)
        messages = data.get("chat_messages", [])
        for msg in messages:
            fragments = msg.get("fragments", [])
            for frag in fragments:
                content = frag.get("content")
                if not content or not isinstance(content, str):
                    continue
                
                # Превращаем экранированные \n в настоящие переносы строк
                # и убираем лишние слеши
                clean_text = content.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace('\\\\', '\\')
                
                # Ищем блоки кода
                matches = code_pattern.findall(clean_text)
                if matches:
                    os.makedirs(session_dir, exist_ok=True)
                    for i, code_block in enumerate(matches):
                        if len(code_block.strip()) < 20:
                            continue
                        
                        code_filename = os.path.join(session_dir, f"code_{file_blocks_count + i + 1}.py")
                        with open(code_filename, "w", encoding="utf-8") as code_f:
                            code_f.write(code_block.strip())
                        
                        total_extracted += 1
                        file_blocks_count += 1
                        
        if file_blocks_count > 0:
            print(f"✅ {filename}: найдено {file_blocks_count} блоков кода")

    except Exception as e:
        print(f"❌ Ошибка при чтении {filename}: {e}")

print(f"\n🎉 ГОТОВО! Всего извлечено блоков кода: {total_extracted}")
