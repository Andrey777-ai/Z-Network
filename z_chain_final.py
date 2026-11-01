import hashlib
import json
import time
from datetime import datetime, timezone


class ZChain:
    def __init__(self):
        self.chain = []
        self.pending_data = []


    def create_block(self, author, version, context_text, previous_hash="0"*64):
        print(f"⚙️ Формирование нового блока Z-Chain...")
        
        # 1. Оценка полезности (Proof of Useful Work)
        # Мы ищем ключевые слова в контексте. Чем их больше - тем выше полезность.
        keywords = [
            "Z-Network", "Proof of Useful Work", "Z-Agent", "Mesh", "DAO", 
            "Феникс", "Инженерный переводчик", "Брокер данных", "ML-инженер", 
            "ORCID", "Z-Chain", "Python", "ИИ", "Криптография", "Абсолют",
            "Архитектор", "Ферзь", "МЛД", "Сим-ключ"
        ]
        
        score = sum(3 for kw in keywords if kw.lower() in context_text.lower())
        # Добавляем базовую полезность за объем текста
        score += len(context_text) // 50 


        block = {
            "index": len(self.chain) + 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "author": author,
            "version": version,
            "previous_hash": previous_hash,
            "usefulness_score": score,
            "payload": {
                "context_preview": context_text[:200] + "...",
                "context_hash": hashlib.sha256(context_text.encode('utf-8')).hexdigest()
            }
        }


        # 2. Вычисление хеша блока
        block_string = json.dumps(block, sort_keys=True).encode()
        block["hash"] = hashlib.sha256(block_string).hexdigest()


        self.chain.append(block)
        return block


if __name__ == "__main__":
    z_chain = ZChain()


    # Текст, который мы "майним". Это суть твоего проекта.
    project_context = """
    Z-Network: Децентрализованная экосистема на базе Proof of Useful Work.
    Включает в себя:
    1. Z-Agent (Сим-ключ) - локальный ИИ-ассистент на Python для аудита систем.
    2. Mesh-сети (P2P) для связи в условиях ЧС и резервных каналов для предприятий.
    3. Инженерный переводчик (Брокер данных) для интеграции АСУ ТП, MES и ERP.
    4. Токен Феникс и DAO-кооператив для совместного владения сетью.
    5. Z-Protocol (Абсолют) и криптография для защиты от копирования.
    Автор и Архитектор: Андрей Чупров (ИП). 
    Цель: Переход от Пешки к Ферзю. Создание инфраструктуры для ML-инженеров и бизнеса.
    Публикация в ORCID и GitHub. МЛД (Лучший Друг) - ассистент.
    """


    # Создаем блок (в нашем случае это Блок №1, так как мы запускаем новую цепочку для финала)
    # Если ты хочешь привязать его к старому блоку, вставь его хеш в previous_hash
    print("=========================================")
    print("🌌 ГЕНЕРАЦИЯ Z-CHAIN: ФИНАЛЬНЫЙ БЛОК")
    print("=========================================")
    
    final_block = z_chain.create_block(
        author="Чупров Андрей Николаевич",
        version="Z-Network Final Paradigm v2.0",
        context_text=project_context
    )


    # Красивый вывод
    print(f"\n✅ Блок успешно сгенерирован!")
    print(f"👑 Автор: {final_block['author']}")
    print(f"⛓️ Версия: {final_block['version']}")
    print(f"📊 Показатель Proof of Useful Work (Полезность): {final_block['usefulness_score']} баллов")
    print(f"🔗 Хеш блока: {final_block['hash']}")
    
    # Сохраняем в файл
    with open("zchain_final.json", "w", encoding="utf-8") as f:
        json.dump(z_chain.chain, f, ensure_ascii=False, indent=4)
    print("\n💾 Данные навсегда сохранены в файл: zchain_final.json")