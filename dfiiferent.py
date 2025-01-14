import json
from Levenshtein import ratio

def compare_jsons(dict1, dict2, output_file="differences.json"):
    # Инициализация счетчиков
    matching_chars = 0
    non_matching_fields = []  # Поля с различающимися значениями
    levenshtein_results = []
    differing_fields = {}
    missing_fields = []

    # Рекурсивная функция для сравнения вложенных структур
    def compare_values(key, value1, value2, path=""):
        nonlocal matching_chars, non_matching_fields, levenshtein_results, differing_fields

        current_path = f"{path}.{key}" if path else key

        if isinstance(value1, dict) and isinstance(value2, dict):
            # Если оба значения - словари, рекурсивно сравниваем их
            for k in value1:
                if k in value2:
                    compare_values(k, value1[k], value2[k], current_path)
                else:
                    missing_fields.append(f"{current_path}.{k}")
            for k in value2:
                if k not in value1:
                    missing_fields.append(f"{current_path}.{k}")
        elif isinstance(value1, list) and isinstance(value2, list):
            # Если оба значения - списки, сравниваем их поэлементно
            for i, (item1, item2) in enumerate(zip(value1, value2)):
                compare_values(str(i), item1, item2, current_path)
        else:
            # Если значения не являются словарями или списками, сравниваем их как строки
            value1_str = str(value1)
            value2_str = str(value2)

            # 1) Кол-во совпадающих символов в значении
            matching_chars += sum(c1 == c2 for c1, c2 in zip(value1_str, value2_str))

            # 2) Кол-во не совпадающих полей
            if value1_str != value2_str:
                non_matching_fields.append(current_path)
                differing_fields[current_path] = {
                    "original": value1,
                    "copy": value2
                }

            # 3) Расстояние Левенштейна в процентах для каждого слова
            words1 = value1_str.split()
            words2 = value2_str.split()
            for word1, word2 in zip(words1, words2):
                similarity = ratio(word1, word2)
                if similarity > 0.01:  # Добавляем только если сходство > 1%
                    levenshtein_results.append((word1, word2, similarity * 100))

    # Начинаем сравнение с корневого уровня
    compare_values("", dict1, dict2)

    # Сохранение различающихся полей в новый JSON
    if differing_fields:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(differing_fields, f, ensure_ascii=False, indent=4)
        print(f"Различающиеся поля сохранены в файл: {output_file}")

    #1) Количество совпадающих символов в значениях:
    #2) Количество не совпадающих полей
    #3) Расстояние Левенштейна в процентах для каждого слова

    # Вывод результатов
    print(f"1) Количество совпадающих символов в значениях: {matching_chars}")
    print(f"2) Количество не совпадающих полей: {len(non_matching_fields)}")
    print("   Не совпадающие поля:")
    for field in non_matching_fields:
        print(f"   - {field}")
    print("3) Расстояние Левенштейна в процентах для каждого слова (совпадение < 100%):")
    for result in levenshtein_results:
        if result[2] < 100:  # Выводим только если сходство < 100%
            print(f"   {result[0]} vs {result[1]} - {result[2]:.2f}%")
    print("4) Различающиеся поля:")
    for key, values in differing_fields.items():
        print(f"   {key}: original = {values['original']}, copy = {values['copy']}")
    print("5) Пропущенные поля во втором JSON по сравнению с первым:")
    for field in missing_fields:
        print(f"   {field}")

# Пример использования
with open('json1.json', 'r', encoding='utf-8') as f:
    json1 = json.load(f)

with open('json2.json', 'r', encoding='utf-8') as f:
    json2 = json.load(f)

compare_jsons(json1, json2)