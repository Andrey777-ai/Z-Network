import hashlib
import json
import os
from datetime import datetime, timezone

def create_z_block(chain_name, author, version, context_text, keywords):
    print(f"🌌 Генерация блока для цепочки: {chain_name}...")
    
    # 1. Считаем Proof of Useful Work на основе переданных ключевых слов
    score = sum(3 for kw in keywords if kw.lower() in context_text.lower())
    score += len(context_text) // 50 

    # 2. Ищем предыдущий блок в этой же папке для связи
    previous_hash = "0" * 64
    index = 1
    
    # Ищем файлы в текущей папке (где лежит скрипт)
    for file in os.listdir('.'):
        if file.endswith('.json') and chain_name in file:
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    old_chain = json.load(f)
                    if old_chain:
                        previous_hash = old_chain[-1]["hash"]
                        index = old_chain[-1]["index"] + 1
            except:
                pass

    # 3. Формируем блок
    block = {
        "index": index,
        "chain_name": chain_name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "author": author,
        "version": version,
        "previous_hash": previous_hash,
        "usefulness_score": score,
        "payload": {
            "context_preview": context_text[:150] + "...",
            "context_hash": hashlib.sha256(context_text.encode('utf-8')).hexdigest(),
            "applied_keywords": keywords 
        }
    }

    # 4. Вычисляем хеш
    block_string = json.dumps(block, sort_keys=True).encode()
    block["hash"] = hashlib.sha256(block_string).hexdigest()

    # 5. Сохраняем в файл (дописываем в конец цепочки)
    filename = f"{chain_name}_chain.json"
    chain_data = []
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            chain_data = json.load(f)
    
    chain_data.append(block)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(chain_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Блок №{index} успешно добавлен в {filename}!")
    print(f"📊 Полезность: {score} баллов")
    print(f"🔗 Хеш: {block['hash']}\n")

# === БЛОК ДЛЯ ЗАПУСКА ===
if __name__ == "__main__":
    # Текст, фиксирующий наш технический прогресс
    my_context = """
    Успешный перенос Z-Agent на операционную систему Linux Mint. 
    Настроена безопасная работа с GitHub через SSH-ключи. 
    Разработан Мультичейн-генератор блоков для распределения контента по ветвям.
    Сформирован локальный датасет из 209 сессий (77 МБ) для эволюции ИИ-агента.
    Изучены методы защиты интеллектуальной собственности и локальной изоляции данных (включая ФЗ-117).
    Проект Z-Network обретает архитектурную устойчивость и начинает процесс эволюции.
    """
    
    # Ключевые слова для ветви "Tech"
    my_keywords = [
        "Z-Agent", "Linux", "GitHub", "SSH", "Мультичейн", "датасет", 
        "эволюция", "ФЗ-117", "локальная изоляция", "Python", "Архитектор"
    ]
    
    create_z_block(
        chain_name="Z-Chain_Tech", # Наша первая техническая ветвь
        author="Чупров Андрей Николаевич",
        version="Tech Genesis v1.0",
        context_text=my_context,
        keywords=my_keywords
    )
