from detoxify import Detoxify
import pandas as pd

# Примеры текстов для анализа
input_text = [
    "example text",
    "exemple de texte",
    "texto de ejemplo",
    "testo di esempio",
    "texto de exemplo",
    "örnek metin",
    "пример текста"
]

# Анализ текста с использованием модели 'multilingual'
results = Detoxify('multilingual').predict(input_text)

# Вывод результатов в виде таблицы
print(pd.DataFrame(results, index=input_text).round(5))