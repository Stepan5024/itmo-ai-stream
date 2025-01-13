import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import re
import string
from wordcloud import WordCloud
from collections import Counter
from sqlalchemy import create_engine, inspect
import nltk 
from nltk.corpus import stopwords
from natasha import MorphVocab, Doc, Segmenter, NewsMorphTagger, NewsEmbedding

# Глобальный счетчик для отслеживания обработанных строк
processed_rows_counter = 0

# Настройка логгирования
def setup_logging(output_folder, csv_name):
    """
    Настройка логгирования.
    """
    log_file = os.path.join(output_folder, f'{csv_name}_log.txt')
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Функция для предобработки данных
def preprocess_data(df):
    """
    Функция для предобработки данных.
    """
    global processed_rows_counter  # Используем глобальный счетчик

    # Логирование начального состояния данных
    logging.info(f"Initial data shape: {df.shape}")
    logging.info(f"Initial data columns: {df.columns.tolist()}")
    logging.info(f"First 5 rows:\n{df.head()}")

    # Применение правила: если значение > 0.65, то 1, иначе 0
    toxicity_columns = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    for column in toxicity_columns:
        df[column] = df[column].apply(lambda x: 1 if x > 0.65 else 0)
    logging.info("Applied binary transformation to toxicity columns.")
    logging.info(f"Data after binary transformation:\n{df[toxicity_columns].head()}")

    # Удаление дубликатов по столбцу comment_text
    initial_count = len(df)
    df = df.drop_duplicates(subset='comment_text', keep='first')
    removed_count = initial_count - len(df)
    logging.info(f"Removed {removed_count} duplicate rows based on 'comment_text'.")
    logging.info(f"Data shape after removing duplicates: {df.shape}")

    # Очистка текста
    df.loc[:, 'comment_text'] = df['comment_text'].apply(preprocess_text)
    logging.info("Text preprocessing completed.")
    logging.info(f"Sample preprocessed text:\n{df['comment_text'].head()}")

    # Удаление комментариев, состоящих только из спецсимволов или цифр
    initial_count = len(df)
    df = df[~df['comment_text'].apply(is_special_or_numeric)]
    removed_count = initial_count - len(df)
    logging.info(f"Removed {removed_count} rows with special characters or numeric-only comments.")
    logging.info(f"Data shape after removing special/numeric comments: {df.shape}")

    # Удаление коротких комментариев
    initial_count = len(df)
    df = df[df['comment_text'].str.len() >= 2]
    removed_count = initial_count - len(df)
    logging.info(f"Removed {removed_count} rows with short comments (length < 2).")
    logging.info(f"Data shape after removing short comments: {df.shape}")

    # Сброс счетчика после обработки данных
    processed_rows_counter = 0

    return df

# Функция для очистки текста
def preprocess_text(text):
    """
    Функция для предобработки текста.
    """
    global processed_rows_counter  # Используем глобальный счетчик

    # Увеличиваем счетчик строк
    processed_rows_counter += 1

    # Печать в консоль каждые 50 000 строк
    if processed_rows_counter % 50000 == 0:
        print(f"Лемматизировано {processed_rows_counter} строк.")

    # Приведение к нижнему регистру
    text = text.lower()

    # Удаление пунктуации
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Удаление стоп-слов
    text = ' '.join([word for word in text.split() if word not in stop_words])

    # Лемматизация с использованием Natasha
    doc = Doc(text)
    doc.segment(segmenter)  # Токенизация
    doc.tag_morph(morph_tagger)  # Морфологический анализ

    # Извлечение лемм
    for token in doc.tokens:
        token.lemmatize(morph_vocab)  # Лемматизация каждого токена
    lemmas = [token.lemma for token in doc.tokens]
    text = ' '.join(lemmas)

    return text

# Функция для проверки, состоит ли текст только из спецсимволов или цифр
def is_special_or_numeric(text):
    """
    Функция для проверки, состоит ли текст только из спецсимволов или цифр.
    """
    return bool(re.match(r'^[\W\d_]+$', text))

# Функция для сохранения графиков
def save_plots(df, output_folder, csv_name):
    """
    Функция для сохранения графиков.
    """
    # Изучение длины комментариев
    df['comment_length'] = df['comment_text'].apply(len)
    plt.figure(figsize=(10, 6))
    sns.histplot(df['comment_length'], bins=50)
    plt.title('Распределение длины комментариев')
    plt.savefig(os.path.join(output_folder, f'{csv_name}_comment_length.png'))
    plt.close()
    logging.info(f"Comment length statistics:\n{df['comment_length'].describe()}")

    # Распределение количества меток на один комментарий
    labels = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
    df['num_labels'] = df[labels].sum(axis=1)
    plt.figure(figsize=(10, 6))
    sns.countplot(x='num_labels', data=df)
    plt.title('Количество меток на один комментарий')
    plt.savefig(os.path.join(output_folder, f'{csv_name}_num_labels.png'))
    plt.close()
    logging.info(f"Label distribution:\n{df['num_labels'].value_counts().sort_index()}")

    # Распределение для любого типа токсичности
    df['any_toxic'] = df[labels].max(axis=1)
    plt.figure(figsize=(8, 6))
    ax = sns.countplot(x='any_toxic', data=df)
    plt.title('Распределение для любого типа токсичности (any_toxic)')
    for p in ax.patches:
        height = p.get_height()
        percentage = (height / len(df)) * 100
        ax.text(p.get_x() + p.get_width() / 2., height + 0.1, f'{percentage:.1f}%', ha='center')
    plt.savefig(os.path.join(output_folder, f'{csv_name}_any_toxic.png'))
    plt.close()
    logging.info(f"Any toxic distribution:\n{df['any_toxic'].value_counts()}")

    # Облако слов для токсичных и нетоксичных комментариев
    toxic_text = ' '.join(df[df['toxic'] == 1]['comment_text'])
    non_toxic_text = ' '.join(df[df['toxic'] == 0]['comment_text'])
    generate_wordcloud(toxic_text, 'Облако слов для токсичных комментариев', os.path.join(output_folder, f'{csv_name}_toxic_wordcloud.png'))
    generate_wordcloud(non_toxic_text, 'Облако слов для нетоксичных комментариев', os.path.join(output_folder, f'{csv_name}_non_toxic_wordcloud.png'))
    logging.info(f"Top 10 words in toxic comments:\n{Counter(toxic_text.split()).most_common(10)}")
    logging.info(f"Top 10 words in non-toxic comments:\n{Counter(non_toxic_text.split()).most_common(10)}")

    # Распределение меток
    label_counts = df[labels].sum()
    label_percentages = df[labels].mean() * 100
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x=label_counts.index, y=label_counts.values, palette='viridis')
    plt.title('Распределение меток')
    plt.ylabel('Количество комментариев')
    plt.xlabel('Метки')
    plt.xticks(rotation=45)
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x() + p.get_width() / 2., height + 0.1, f'{height / len(df) * 100:.1f}%', ha='center')
    plt.savefig(os.path.join(output_folder, f'{csv_name}_label_distribution.png'))
    plt.close()
    logging.info(f"Label counts:\n{label_counts}")
    logging.info(f"Label percentages:\n{label_percentages}")

# Функция для генерации облака слов
def generate_wordcloud(text, title, save_path):
    """
    Функция для генерации облака слов.
    """
    if len(text) > 1000000:  # Ограничение на длину текста
        text = text[:1000000]
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title)
    plt.savefig(save_path)
    plt.close()

# Функция для обработки одного CSV-файла
def process_csv(file_path, root_folder):
    """
    Функция для обработки одного CSV-файла.
    """
    # Получаем имя файла без расширения
    csv_name = os.path.splitext(os.path.basename(file_path))[0]

    # Создаем папку для результатов внутри корневой папки
    output_folder = os.path.join(root_folder, csv_name)
    os.makedirs(output_folder, exist_ok=True)

    # Настраиваем логгирование
    setup_logging(output_folder, csv_name)

    # Чтение CSV-файла
    df = pd.read_csv(file_path, dtype={0: str})
    logging.info(f'Loaded CSV file: {file_path}')

    # Предобработка данных
    df = preprocess_data(df)
    logging.info('Data preprocessing completed.')

    # Сохранение графиков
    save_plots(df, output_folder, csv_name)
    logging.info('Plots saved.')

    # Сохранение данных в базу данных
    engine = create_engine("sqlite:///ai-stream.db")
    table_name = "cleaned_comments"
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    logging.info(f'Data saved to database table: {table_name}')

# Основная функция
def main(csv_files, root_folder='data_explore'):
    """
    Основная функция, которая обрабатывает список CSV-файлов.
    """
    # Создаем корневую папку, если она не существует
    os.makedirs(root_folder, exist_ok=True)

    for file_path in csv_files:
        if os.path.exists(file_path):
            process_csv(file_path, root_folder)
        else:
            print(f'File {file_path} does not exist.')

if __name__ == "__main__":
    # Инициализация компонентов Natasha
    segmenter = Segmenter()
    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    morph_vocab = MorphVocab()

    # Загрузка стоп-слов для русского языка
    nltk.download('stopwords')
    stop_words = set(stopwords.words('russian'))

    # Пример списка CSV-файлов для обработки
    csv_files = ['final_combined_toxicity_data.csv']

    # Вызов основной функции
    main(csv_files)