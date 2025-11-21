# error_counter.py
# Подсчет любых ключевых слов в лог-файле

def count_keyword(filename: str, keyword: str) -> int:
    """
    Считает, сколько раз слово встречается в файле. 

    Аргументы: 
        filename (str): имя файла для анализа
        keyword (str): ключевое слово для поиска
    
    Возвращает:
        int: количество найденных строк
    """
    count = 0
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            if keyword in line:
                count += 1
    return count

# --- Основная часть скрипта ---
if __name__ == "__main__":
    log_file = "error.log"

    errors = count_keyword(log_file, "ERROR")
    warnings = count_keyword(log_file, "WARNING")

    print(f"Анализ файла: '{log_file}':")
    print(f"Ошибок (ERROR): {errors}")
    print(f"Предупреждений (WARNING): {warnings}")