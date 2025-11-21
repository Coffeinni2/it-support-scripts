# daily_log_analyzer.py
import sys
from datetime import datetime, timedelta
import re

def parse_timestamp(line: str):
    """
    Извлекает дату-время из строки лога вида [2025-11-21T09:12:44].
    Возвращает объект datetime или None, если не найдено.
    """
    match = re.search(r'\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\]', line)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return None
    return None

def count_recent_errors(filename: str, keyword: str = "ERROR", hours: int = 24) -> int:
    """
    Считает строки с keyword в файле, где временная метка — за последние 'hours' часов.
    """
    cutoff_time = datetime.now() - timedelta(hours=hours)
    count = 0

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                log_time = parse_timestamp(line)
                if log_time and log_time >= cutoff_time:
                    if keyword in line:
                        count += 1
    except FileNotFoundError:
        print(f"❌ Файл не найден: {filename}")
        sys.exit(1)

    return count

# --- Основная часть ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python3 daily_log_analyzer.py <файл_лога> [ключевое_слово] [часы]")
        print("Пример: python3 daily_log_analyzer.py error.log ERROR 24")
        sys.exit(1)

    logfile = sys.argv[1]
    keyword = sys.argv[2] if len(sys.argv) > 2 else "ERROR"
    hours = int(sys.argv[3]) if len(sys.argv) > 3 else 24

    result = count_recent_errors(logfile, keyword, hours)

    # Формируем и выводим сообщение
    output_text = f"За последние {hours} ч. найдено '{keyword}': {result}"
    print("✅", output_text)

    # Сохраняем отчёт с временной меткой в файл
    report_line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {output_text}\n"
    with open("report.txt", "a", encoding="utf-8") as report_file:
        report_file.write(report_line)
    
    print("📄 Отчёт сохранён в report.txt")