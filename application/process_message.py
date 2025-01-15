import re
import string
from natasha import MorphVocab, Doc, Segmenter, NewsMorphTagger, NewsEmbedding

# Инициализация компонентов Natasha
segmenter = Segmenter()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
morph_vocab = MorphVocab()

def preprocess_text(text):
    """
    Функция для предобработки текста.
    """
    # Приведение к нижнему регистру
    text = text.lower()

    # Удаление пунктуации
    text = text.translate(str.maketrans('', '', string.punctuation))

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

def is_toxic(comment_text, model):
    """
    Функция для определения токсичности комментария с использованием detoxify.
    """
    # Предобработка текста
    processed_text = preprocess_text(comment_text)
    
    # Предсказание токсичности с использованием модели
    results = model.predict(processed_text)
    
    # Применение порога 0.65 для каждого класса токсичности
    toxic = int(results['toxicity'] > 0.65)
    severe_toxic = int(results['severe_toxicity'] > 0.65)
    obscene = int(results['obscene'] > 0.65)
    threat = int(results['threat'] > 0.65)
    insult = int(results['insult'] > 0.65)
    identity_hate = int(results['identity_attack'] > 0.65)
    
    # Возвращаем результат в виде словаря
    return {
        "toxic": toxic,
        "severe_toxic": severe_toxic,
        "obscene": obscene,
        "threat": threat,
        "insult": insult,
        "identity_hate": identity_hate,
    }