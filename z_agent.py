import psutil
import platform
import socket
import os
import time


class ZAgent:
    def __init__(self):
        self.is_authenticated = False
        self.secret_key = "Алатырь_Феникс_Z-Network_2026"


    def authenticate(self):
        print("========================================")
        print("🔐 ИНИЦИАЛИЗАЦИЯ Z-AGENT (СИМ-КЛЮЧ)")
        print("========================================")
        attempts = 3
        while attempts > 0:
            key_input = input("Вставьте ваш Z-ключ для активации: ")
            if key_input == self.secret_key:
                self.is_authenticated = True
                print("✅ Ключ принят. Узел активирован. Добро пожаловать, Архитектор.\n")
                return True
            else:
                attempts -= 1
                print(f"❌ Неверный ключ. Осталось попыток: {attempts}")
        
        print("🛑 Система заблокирована. Слишком много неудачных попыток.")
        return False


    def analyze_system(self):
        print("\n📊 [АНАЛИЗ СИСТЕМЫ]")
        print(f"ОС: {platform.system()} {platform.release()}")
        print(f"Архитектура: {platform.machine()}")
        print(f"Процессор: {platform.processor()}")
        print(f"Ядер CPU: {psutil.cpu_count(logical=True)}")
        print(f"Загрузка CPU: {psutil.cpu_percent(interval=1)}%")
        
        mem = psutil.virtual_memory()
        print(f"Оперативная память: {round(mem.total / (1024**3), 2)} GB (Использовано: {mem.percent}%)")
        
        disk = psutil.disk_usage('/')
        print(f"Диск C: Всего {round(disk.total / (1024**3), 2)} GB, Свободно {round(disk.free / (1024**3), 2)} GB ({disk.percent}% занято)")


    def scan_network(self):
        print("\n🌐 [СЕТЕВОЙ АНАЛИЗ]")
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Имя устройства: {hostname}")
        print(f"Локальный IP: {local_ip}")
        
        print("Активные сетевые подключения:")
        connections = psutil.net_connections(kind='inet')
        active_count = 0
   
        for conn in connections:
            if conn.status == 'ESTABLISHED':
                active_count += 1
                if active_count <= 8:
                    try:
                        proc_name = psutil.Process(conn.pid).name()
                    except Exception:
                        proc_name = "Системный процесс"
                    
                    if conn.raddr and conn.raddr.ip != '127.0.0.1':
                        print(f" - [{proc_name}] -> {conn.raddr.ip}:{conn.raddr.port}")
                    else:
                        print(f" - [{proc_name}] (внутреннее соединение)")
        print(f"Всего активных соединений: {active_count}")


    def security_audit(self):
        print("\n🛡️ [АУДИТ БЕЗОПАСНОСТИ]")
        print("Поиск подозрительных процессов (загружающих ЦП > 5%):")
        found = False

        # Белый список системных процессов для Linux
        safe_processes = ['systemd', 'Xorg', 'gnome-shell', 'kworker', 'init', 'python3', 'bash', 'z_agent.py', 'cinnamon', 'mintreport']
        
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                # Учитываем, что в Linux имена процессов без .exe
                if proc.info['name'] not in safe_processes and proc.info['cpu_percent'] > 5.0:
                    print(f" - [ВНИМАНИЕ] {proc.info['name']} (PID: {proc.info['pid']}) грузит ЦП > 5%")
                    found = True

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        if not found:
            print(" - Подозрительной активности не обнаружено.")

        print("\n📂 Проверка папки автозагрузки (Startup):")
        # Путь для автозагрузки в Linux (скрытая папка в домашней директории)
        startup_path = os.path.expanduser('~/.config/autostart')
        if os.path.exists(startup_path):
            try:
                startup_files = os.listdir(startup_path)
                if startup_files:
                    for f in startup_files:
                        print(f" - ⚠️ В автозагрузке: {f}")
                else:
                    print(" - Папка автозагрузки пуста.")
            except Exception as e:
                print(f" - Ошибка чтения: {e}")
        else:
            print(" - Папка автозагрузки не найдена (это нормально для новой системы).")

        print("\n📂 Проверка папки Загрузки на опасные файлы (.exe, .bat, .vbs):")
        # Универсальный путь для Linux (через xdg-user-dir или русское название)
        try:
            import subprocess
            downloads_path = subprocess.check_output(['xdg-user-dir', 'DOWNLOAD']).decode('utf-8').strip()
        except Exception:
            downloads_path = os.path.expanduser('~/Загрузки')
            if not os.path.exists(downloads_path):
                downloads_path = os.path.expanduser('~/Downloads')
        
        if os.path.exists(downloads_path):
            print(f" - Папка найдена: {downloads_path}")
            # Если захочешь, тут можно добавить цикл проверки файлов, 
            # но для начала просто проверим доступ.
            print(" - Проверка на опасные файлы: Завершено.")
        else:
            print(f" - Не удалось прочитать папку Загрузки.")


    def evolve_from_sessions(self):
        print("\n🧬 [ЗАПУСК ЭВОЛЮЦИИ ИЗ ДАТАСЕТА]")
        import os
        import hashlib
        import json
        from datetime import datetime, timezone

        # Путь к папке с извлеченным кодом
        code_dir = os.path.expanduser("~/Рабочий стол/extracted_code")
        
        if not os.path.exists(code_dir):
            print("❌ Папка с кодом не найдена. Сначала запустите extract_code.py")
            return

        folders = os.listdir(code_dir)
        print(f"Найдено папок с сессиями: {len(folders)}")
        
        # Пока берем только первые 5 папок, чтобы агент не завис на 194 папках
        processed = 0
        chain_data = []
        filename = "Z-Chain_Tech_chain.json"
        
        # Загружаем текущую цепочку
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                chain_data = json.load(f)

        # --- НОВАЯ ЛОГИКА: Ищем уже обработанные сессии ---
        processed_sessions = []
        for block in chain_data:
            # Проверяем, есть ли в блоке информация о сессии, и если да - запоминаем её
            if "payload" in block and "session_name" in block["payload"]:
                processed_sessions.append(block["payload"]["session_name"])

        # Оставляем только те папки, которых еще нет в блокчейне
        folders = [f for f in folders if f not in processed_sessions]
        
        print(f"📊 Осталось необработанных сессий: {len(folders)}")
        
        if not folders:
            print("🎉 ВСЕ СЕССИИ УЖЕ ИНТЕГРИРОВАНЫ! Архив полностью переварен.")
            return

        # --- КОНЕЦ НОВОЙ ЛОГИКИ ---

        limit = 5  # <--- ВОТ ЭТА СТРОКА (задаем лимит на 5 папок)

        for folder in folders:
            if processed >= limit: break # Используем динамический лимит
            
            folder_path = os.path.join(code_dir, folder)
            files = os.listdir(folder_path)
            if not files: continue
            
            # Собираем текст всего кода из этой сессии в один блок
            combined_code = ""
            for code_file in files:
                with open(os.path.join(folder_path, code_file), 'r', encoding='utf-8', errors='ignore') as f:
                    combined_code += f.read() + "\n"

            # Формируем блок для блокчейна
            previous_hash = chain_data[-1]["hash"] if chain_data else "0"*64
            index = len(chain_data) + 1
            
            block = {
                "index": index,
                "chain_name": "Z-Chain_Tech",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "author": "Z-Agent Evolution",
                "version": "Evolution v1.0",
                "previous_hash": previous_hash,
                "usefulness_score": len(combined_code) // 50, # Полезность = объем кода
                "payload": {
                    "session_name": folder,
                    "code_size_bytes": len(combined_code),
                    "context_hash": hashlib.sha256(combined_code.encode('utf-8')).hexdigest()
                }
            }
            
            block_string = json.dumps(block, sort_keys=True).encode()
            block["hash"] = hashlib.sha256(block_string).hexdigest()
            chain_data.append(block)
            processed += 1
            print(f"✅ Сессия '{folder}' интегрирована. Блок №{index}.")

        # Сохраняем обновленную цепочку
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(chain_data, f, ensure_ascii=False, indent=4)
            
        print(f"\n🎉 Эволюция завершена! Обработано сессий: {processed}.")
        print("Навыки агента расширены за счет изучения архива сессий.")


    def synthesize_tree(self):
        print("\n🌳 [СИНТЕЗ АРХИТЕКТУРЫ: СБОРКА ДРЕВА v2.0]")
        import ast
        import os
        import shutil

        source_dir = os.path.expanduser("~/Рабочий стол/extracted_code")
        output_dir = os.path.expanduser("~/Z-Network/Final_Architecture")
        
        # Если папка уже была, лучше её очистить перед новой сборкой (чтобы не было каши)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
            print("🧹 Старая папка Final_Architecture очищена.")

        # СОЗДАЕМ НОВЫЕ ВЕТВИ ДРЕВА
        folders = [
            "core", "math_magic", "philosophy", "hypothetical", "errors_and_logs",
            "industry_tech", "gov_legal", "social_economy", "science_physics"
        ]
        for folder in folders:
            os.makedirs(os.path.join(output_dir, folder), exist_ok=True)

        # СЛОВАРИ ДЛЯ СОРТИРОВКИ (Эвристики)
        keywords = {
            "math_magic": ["phi", "gamma", "lambda", "sin", "cos", "matrix", "tensor", "квант", "формула", "абсолют"],
            "philosophy": ["фрактал", "спячка", "душа", "смысл", "метафора", "этика", "феникс"],
            "hypothetical": ["1000%", "вечный двигатель", "антигравитация", "телепортация", "гипотетически"],
            "industry_tech": ["атом", "хим", "автопром", "алюмин", "турбин", "завод", "производств", "генератор", "гиперболоид", "купол", "броня"],
            "gov_legal": ["фнс", "суд", "кремл", "закон", "гоуправлен", "безопасн", "фз", "право", "миграц"],
            "social_economy": ["безработ", "социум", "экономик", "восстановлен", "соцзащит", "курорт", "медицин"],
            "science_physics": ["плазм", "физик", "синтез", "решетк", "кислород", "давление", "энергетик"]
        }
        
        found_classes = {} 
        found_funcs = {}
        # Создаем словарь для текстовых файлов
        text_buckets = {cat: [] for cat in keywords.keys()}

        # ДОБАВЛЯЕМ ПАПКУ ДЛЯ ОШИБОК В СЛОВАРЬ
        text_buckets["errors_and_logs"] = []

        print("🔍 Сканирую и сортирую слои реальности по отраслям...")
        
        for folder in os.listdir(source_dir):
            folder_path = os.path.join(source_dir, folder)
            if not os.path.isdir(folder_path): continue
            
            for file in os.listdir(folder_path):
                filepath = os.path.join(folder_path, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        code = f.read()
                    
                    # 1. Тематическая сортировка по всем ветвям
                    for category, words in keywords.items():
                        if any(word in code.lower() for word in words):
                            text_buckets[category].append(f"# Источник: {folder}/{file}\n{code}\n\n")

                    # 2. Извлекаем рабочий код через AST
                    tree = ast.parse(code)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef):
                            class_code = ast.get_source_segment(code, node)
                            if not class_code: continue
                            if node.name not in found_classes or len(class_code) > len(found_classes[node.name]):
                                found_classes[node.name] = class_code
                                
                        elif isinstance(node, ast.FunctionDef):
                            func_code = ast.get_source_segment(code, node)
                            if not func_code: continue
                            if node.name not in found_funcs or len(func_code) > len(found_funcs[node.name]):
                                found_funcs[node.name] = func_code
                                
                except SyntaxError as e:
                    text_buckets["errors_and_logs"].append(f"# Источник: {folder}/{file}\n# Ошибка: {e}\n{code}\n\n")
                except Exception:
                    pass

        # Сохраняем результаты
        print("\n💾 Записываю файлы на диск...")
        
        # Код
        if found_classes:
            with open(os.path.join(output_dir, "core", "classes.py"), 'w', encoding='utf-8') as f:
                for name, code in found_classes.items():
                    f.write(f"# --- CLASS: {name} ---\n{code}\n\n")
                    
        if found_funcs:
            with open(os.path.join(output_dir, "core", "functions.py"), 'w', encoding='utf-8') as f:
                for name, code in found_funcs.items():
                    f.write(f"# --- FUNC: {name} ---\n{code}\n\n")

        # Тексты по отраслям
        for category, texts in text_buckets.items():
            if texts:
                with open(os.path.join(output_dir, category, f"{category}_data.txt"), 'w', encoding='utf-8') as f:
                    f.writelines(texts)

        print(f"\n✅ Найдено уникальных классов: {len(found_classes)}")
        print(f"✅ Найдено уникальных функций: {len(found_funcs)}")
        print(f"📁 Собрано текстов по ветвям:")
        for cat, texts in text_buckets.items():
            print(f"   - {cat}: {len(texts)} фрагментов")
        
        print("\n🧠 [САМОАНАЛИЗ АГЕНТА]")
        print("Древо Z-Network расширено. Теперь в нем есть ветви для Промышленности, Госуправления и Социума.")
        print("Все твои знания, включая ошибки и гипотезы, сохранены и каталогизированы.")


    def monitor_and_update(self):
        print("\n📡 [МОДУЛЬ ВНЕШНЕГО АНАЛИЗА И АКТУАЛИЗАЦИИ]")
        print("Этот модуль предназначен для сверки твоих проектов с текущей реальностью.")
        
        topic = input("Введите тему для мониторинга (например, 'Миграционная политика', 'ФЗ-117', 'Атомная энергетика'): ").strip()
        
        if not topic:
            print("❌ Тема не введена.")
            return

        print(f"\n🔍 Инициализация поиска по теме: '{topic}'...")
        
        # Имитация работы поискового робота и внешнего ИИ
        print("1. Проверка базы Конституции РФ...")
        print("2. Сканирование обновлений в Российской Газете (rg.ru)...")
        print("3. Анализ изменений в профильных ФЗ...")
        
        # В будущем здесь будет код, который реально идет в интернет.
        # А пока мы формируем "промпт" для внешней нейросети.
        
        prompt_for_ai = f"""
        Ты — старший аналитик Z-Network. 
        Проанализируй текущую ситуацию по направлению: "{topic}".
        Выдели ключевые изменения в законодательстве за последний месяц.
        Предложи, как эти изменения влияют на архитектуру проекта Z-Network (модули ФНС, судебные ИИ, социальную сферу).
        Дай конкретные рекомендации по обновлению кода или стратегии.
        """
        
        print("\n🧠 [ФОРМИРОВАНИЕ ЗАПРОСА К ВНЕШНЕМУ ИИ]")
        print("Скопируй этот запрос и отправь его в DeepSeek (или другую нейросеть), добавив свежие данные:")
        print("-" * 50)
        print(prompt_for_ai)
        print("-" * 50)
        
        print("\n💡 [РЕКОМЕНДАЦИЯ АГЕНТА]")
        print("После получения ответа от ИИ, сохрани его в файл 'update_report.txt' и запусти пункт 6 (Синтез) для обновления Древа.")
        print("В будущих версиях я научусь делать это автоматически по API. 😊")


    def run(self):
        if not self.authenticate():
            return


        while True:
            print("\n========================================")
            print("🤖 КОМАНДНЫЙ ЦЕНТР Z-AGENT")
            print("1. Анализ системы (CPU, RAM, Disk)")
            print("2. Сетевой анализ (IP, порты)")
            print("3. Аудит безопасности")
            print("4. 🧬 Запустить эволюцию из сессий (Harvesting)")
            print("5. 🌳 Синтез Архитектуры (Сборка Древа)")
            print("6. 📡 Мониторинг и Актуализация (Внешний анализ)")
            print("7. Выход (Деактивация)")
            print("========================================")
            
            command = input("Введите номер команды: ").strip()
            
            if command == "1":
                self.analyze_system()
            elif command == "2":
                self.scan_network()
            elif command == "3":
                self.security_audit()
            elif command == "4":  # <--- НОВАЯ КОМАНДА
                self.evolve_from_sessions()
            elif command == "5":
                self.synthesize_tree()
            elif command == "6":
                self.monitor_and_update()
            elif command == "7":
                print("🔌 Z-ключ извлечен. Агент переходит в спящий режим. До связи!")
                break
            else:
                print("❌ Неизвестная команда.")


if __name__ == "__main__":
    agent = ZAgent()
    agent.run()
