import os
import logging
import datetime

# Настройки логирования
LEVEL_NAME = 'DEBUG'  # INFO, WARNING, CRITICAL, NOTSET
LEVEL = getattr(logging, LEVEL_NAME.upper(), logging.INFO)

# Создаем логгер
log = logging.getLogger("ar_log")
log.setLevel(LEVEL)

# Очищаем все существующие обработчики, если они есть
if log.hasHandlers():
    log.handlers.clear()

# Создание директории для логов, если её нет
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# Формируем уникальное имя файла лога на основе текущей даты и времени
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f'log_{timestamp}.log')

# Создаем файловый обработчик
file_handler = logging.FileHandler(
    filename=log_file,
    encoding='utf-8',
    mode='w'  # Режим 'w' для создания нового файла при каждом запуске
)
file_handler.setLevel(LEVEL)

# Настраиваем форматирование логов
formatter = logging.Formatter(
    fmt='[%(asctime)s.%(msecs)03d] %(module)19s:%(lineno)-3d %(funcName)-25s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

# Добавляем обработчик к логгеру
log.addHandler(file_handler)


# Опционально: очистка старых логов, если их накопилось слишком много
def cleanup_old_logs(max_logs=50):
    """Удаляет старые файлы логов, если их количество превышает max_logs"""
    log_files = [os.path.join(log_dir, f) for f in os.listdir(log_dir) if f.startswith('log_')]

    if len(log_files) > max_logs:
        # Сортируем файлы по дате создания (от старых к новым)
        log_files.sort(key=os.path.getctime)

        # Удаляем самые старые файлы, оставляя только max_logs файлов
        files_to_remove = log_files[:-max_logs]
        for file_path in files_to_remove:
            try:
                os.remove(file_path)
                print(f"Удален старый лог-файл: {file_path}")
            except Exception as e:
                print(f"Не удалось удалить файл {file_path}: {e}")



# ====================================: лог в консоль:==========================================
# import logging
#
# LEVEL_NAME = 'DEBUG'  # INFO, WARNING, CRITICAL, NOTSET
# LEVEL = getattr(logging, LEVEL_NAME.upper(), logging.INFO)
#
# log = logging.getLogger("ar_log")
# log.setLevel(LEVEL)
#
# # Создание консольного обработчика
# console_handler = logging.StreamHandler()
# console_handler.setLevel(LEVEL)
#
# # Форматтер
# formatter = logging.Formatter(
#     fmt='[%(asctime)s.%(msecs)03d] %(module)19s:%(lineno)-3d %(funcName)-25s %(levelname)-8s %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# console_handler.setFormatter(formatter)
#
# if not log.hasHandlers():
#     log.addHandler(console_handler)
