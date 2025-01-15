import schedule
import time
from sqlalchemy import create_engine, text
import pandas as pd

# Подключение к базе данных
DATABASE_URI = 'sqlite:///ai-stream.db'
engine = create_engine(DATABASE_URI)

# Функция для выполнения SQL-запросов
def execute_query(query, params=None):
    with engine.connect() as connection:
        if params:
            result = connection.execute(text(query), params)
        else:
            result = connection.execute(text(query))
        return result.fetchall()

# Функция для проверки пропущенных значений
def check_missing_values():
    query = """
        SELECT 
            COUNT(*) AS total_rows,
            SUM(CASE WHEN comment_text IS NULL THEN 1 ELSE 0 END) AS missing_comment_text,
            SUM(CASE WHEN language IS NULL THEN 1 ELSE 0 END) AS missing_language,
            SUM(CASE WHEN is_wrong_classificated IS NULL THEN 1 ELSE 0 END) AS missing_is_wrong_classificated
        FROM cleaned_comments;
    """
    result = execute_query(query)
    print("Проверка пропущенных значений:")
    print(f"Всего строк: {result[0][0]}")
    print(f"Пропущено comment_text: {result[0][1]}")
    print(f"Пропущено language: {result[0][2]}")
    print(f"Пропущено is_wrong_classificated: {result[0][3]}")

# Функция для проверки дубликатов
def check_duplicates():
    query = """
        SELECT comment_text, COUNT(*) AS duplicate_count
        FROM cleaned_comments
        GROUP BY comment_text
        HAVING COUNT(*) > 1;
    """
    result = execute_query(query)
    print("\nПроверка дубликатов:")
    if result:
        for row in result:
            print(f"Дубликат: '{row[0]}' (количество: {row[1]})")
    else:
        print("Дубликаты не найдены.")

# Функция для проверки некорректных форматов данных
def check_data_formats():
    query = """
        SELECT 
            COUNT(*) AS total_rows,
            SUM(CASE WHEN comment_text NOT GLOB '*[a-zA-Z0-9 ]*' THEN 1 ELSE 0 END) AS non_standard_comment_text,
            SUM(CASE WHEN language NOT IN ('en', 'ru') THEN 1 ELSE 0 END) AS invalid_language
        FROM cleaned_comments;
    """
    result = execute_query(query)
    print("\nПроверка некорректных форматов данных:")
    print(f"Всего строк: {result[0][0]}")
    print(f"Комментариев с нестандартными символами: {result[0][1]}")
    print(f"Комментариев с неподдерживаемыми языками: {result[0][2]}")

# Функция для проверки несогласованности данных
def check_inconsistencies():
    query = """
        SELECT 
            COUNT(*) AS total_rows,
            SUM(CASE WHEN is_wrong_classificated = 1 AND toxic = 0 THEN 1 ELSE 0 END) AS inconsistent_classification
        FROM cleaned_comments;
    """
    result = execute_query(query)
    print("\nПроверка несогласованности данных:")
    print(f"Всего строк: {result[0][0]}")
    print(f"Несогласованных классификаций: {result[0][1]}")

# Функция для автоматического исправления данных
def fix_data_issues():
    # Исправление пропущенных значений language (установка значения по умолчанию 'en')
    execute_query("""
        UPDATE cleaned_comments
        SET language = 'en'
        WHERE language IS NULL;
    """)
    print("\nИсправлено: Пропущенные значения language заменены на 'en'.")

    # Удаление дубликатов (оставляем только первую запись)
    execute_query("""
        DELETE FROM cleaned_comments
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM cleaned_comments
            GROUP BY comment_text
        );
    """)
    print("Исправлено: Дубликаты удалены.")

    # Исправление несогласованных классификаций
    execute_query("""
        UPDATE cleaned_comments
        SET is_wrong_classificated = 0
        WHERE is_wrong_classificated = 1 AND toxic = 0;
    """)
    print("Исправлено: Несогласованные классификации исправлены.")

# Основная функция
def main():
    # Проверка качества данных
    check_missing_values()
    check_duplicates()
    check_data_formats()
    check_inconsistencies()

    # Автоматическое исправление данных
    fix_data_issues()

    # Повторная проверка после исправлений
    print("\nПовторная проверка после исправлений:")
    check_missing_values()
    check_duplicates()
    check_data_formats()
    check_inconsistencies()

# Запланированный запуск функции main каждые 3 часа
schedule.every(3).hours.do(main)

# Бесконечный цикл для проверки расписания
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)