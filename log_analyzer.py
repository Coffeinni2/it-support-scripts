# log analyzer.py
import sys

def count_keyword(filename: str, keyword: str) -> int:
    """Считает, сколько раз keyword встречается в файле."""
    count = 0
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                if keyword in line:
                    count += 1
    except FileNotFoundError:
        print(f"Ошибка: файл '{filename}'не найден.")
        sys.exit(1) # завершить программу с кодом ошибки
    return count

# --- Основная часть---
if __name__ == "__main__":
    # Проверка, передано ли 2 аргумента?
    if len(sys.argv) != 3:
        print("Использование: python3 log_analyzer.py <файл лога> <ключевое слово>")
        print("Пример: python3 log_analyzer.py error.log ERROR")
        sys.exit(1)

    # Получаем аргументы
    logfile = sys.argv[1]
    word = sys.argv[2]

    # Анализируем
    result = count_keyword(logfile, word)
    print(f"Найдено '{word}' в '{logfile}': {result}")