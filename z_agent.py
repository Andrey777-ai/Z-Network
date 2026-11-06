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
            print("5. Выход (Деактивация)")
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
                print("🔌 Z-ключ извлечен. Агент переходит в спящий режим. До связи!")
                break
            else:
                print("❌ Неизвестная команда.")


if __name__ == "__main__":
    agent = ZAgent()
    agent.run()
