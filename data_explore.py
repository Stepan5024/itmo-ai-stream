import os
import pandas as pd
import matplotlib.pyplot as plt
import logging

def preprocess_data(df):
    """
    Функция для предобработки данных.
    Здесь можно добавить любые необходимые шаги предобработки.
    """
    # Пример: удаление строк с пропущенными значениями
    df = df.dropna()
    return df

def save_plots(df, output_folder, csv_name):
    """
    Функция для создания и сохранения графиков.
    """
    # Пример: построение гистограммы для каждого числового столбца
    for i, column in enumerate(df.select_dtypes(include=['float64', 'int64']).columns):
        plt.figure()
        df[column].hist()
        plt.title(f'Histogram of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')
        plt.savefig(os.path.join(output_folder, f'{csv_name}_image_{i}.jpeg'))
        plt.close()

def setup_logging(output_folder, csv_name):
    """
    Настройка логгирования.
    """
    log_file = os.path.join(output_folder, f'{csv_name}_log.txt')
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

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
    df = pd.read_csv(file_path)
    logging.info(f'Loaded CSV file: {file_path}')
    
    # Предобработка данных
    df = preprocess_data(df)
    logging.info('Data preprocessing completed.')
    
    # Сохранение графиков
    save_plots(df, output_folder, csv_name)
    logging.info('Plots saved.')
    
    # Пример вывода информации о данных
    logging.info(f'Processed data shape: {df.shape}')
    logging.info(f'Processed data columns: {df.columns.tolist()}')

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
    # Пример списка CSV-файлов для обработки
    csv_files = ['jigsaw-unintended-bias-train_ru_clean.csv', 
                 'jigsaw-toxic-comment-train-google-ru-cleaned.csv', 
                 'jigsaw-toxic-comment-train.csv']
    
    # Вызов основной функции
    main(csv_files)