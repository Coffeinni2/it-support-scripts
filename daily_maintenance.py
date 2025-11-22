# daily_maintenance.py
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Модуль для анализа логов
def count_recent_errors_in_file(filepath: str, keyword: str = "ERROR") -> int:
    """Считает ERROR в файле за последние 24 часа (упрощённо — все строки)."""
    count = 0
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if keyword in line:
                    count += 1
    except Exception as e:
        print(f"Не удалось прочитать {filepath}: {e}")
    return count

def archive_old_logs(logs_dir: str):
    """Архивирует все файлы вида *.log.* в папку archive."""
    logs_path = Path(logs_dir)
    archive_path = logs_path / "archive"
    archive_path.mkdir(exist_ok=True)  # создаём, если нет

    archived = 0
    for log_file in logs_path.glob("*.log.*"):
        if log_file.is_file():
            # Формируем имя архива: app.log.1 -> app.log.1.zip
            zip_name = archive_path / f"{log_file.name}.zip"
            shutil.make_archive(str(zip_name).rstrip(".zip"), 'zip', root_dir=str(logs_path), base_dir=log_file.name)
            log_file.unlink()  # удаляем оригинал после архивации
            archived += 1
            print(f"Архивирован: {log_file.name}")
    return archived

def main():
    if len(sys.argv) < 2:
        print("Использование: python3 daily_maintenance.py <папка_с_логами> [ключевое_слово]")
        sys.exit(1)

    logs_dir = sys.argv[1]
    keyword = sys.argv[2] if len(sys.argv) > 2 else "ERROR"

    log_file = Path(logs_dir) / "app.log"
    if not log_file.exists():
        print(f"Основной лог не найден: {log_file}")
        sys.exit(1)

    # 1. Анализируем основной лог
    errors = count_recent_errors_in_file(str(log_file), keyword)
    print(f"Найдено '{keyword}' в {log_file.name}: {errors}")

    # 2. Архивируем старые логи
    archived_count = archive_old_logs(logs_dir)

    # 3. Формируем отчёт
    report = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] " \
             f"Анализ завершён. Ошибок: {errors}. Архивировано файлов: {archived_count}."
    
    report_file = Path("daily_report.txt")
    with open(report_file, "a", encoding="utf-8") as f:
        f.write(report + "\n")
    
    print(f"Сводка: {report}")
    print(f"Отчёт сохранён: {report_file.absolute()}")

if __name__ == "__main__":
    main()