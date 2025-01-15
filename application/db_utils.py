from sqlalchemy import create_engine, inspect, text  # Добавлен импорт text
import pandas as pd
from datetime import datetime

# Добавляем путь к корню проекта в sys.path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from application.config import DATABASE_URI

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URI)

# ============================================
# CRUD для таблицы streams
# ============================================

def create_stream(stream_id, start_time, end_time, chanel_name):
    """
    Создает запись о стриме в таблице streams.
    """
    data = {
        'id': stream_id,
        'start_time': start_time,
        'end_time': end_time,
        'chanel_name': chanel_name
    }
    df = pd.DataFrame([data])
    df.to_sql('streams', engine, if_exists='append', index=False)

def read_stream(stream_id):
    """
    Читает запись о стриме по его ID.
    """
    query = f"SELECT * FROM streams WHERE id = '{stream_id}'"
    return pd.read_sql(query, engine)

def update_stream(stream_id, **kwargs):
    """
    Обновляет запись о стриме по его ID.
    """
    set_clause = ', '.join([f"{key} = '{value}'" for key, value in kwargs.items()])
    query = text(f"""
    UPDATE streams
    SET {set_clause}
    WHERE id = :stream_id
    """)
    with engine.connect() as connection:
        connection.execute(query, {"stream_id": stream_id})

def delete_stream(stream_id):
    """
    Удаляет запись о стриме по его ID.
    """
    query = text("DELETE FROM streams WHERE id = :stream_id")
    with engine.connect() as connection:
        connection.execute(query, {"stream_id": stream_id})

# ============================================
# CRUD для таблицы row_comments
# ============================================

def create_row_comment(comment_id, comment_text, toxic=0, severe_toxic=0, obscene=0, threat=0, insult=0, identity_hate=0):
    """
    Создает запись комментария в таблице row_comments.
    """
    data = {
        'id': comment_id,
        'comment_text': comment_text,
        'toxic': toxic,
        'severe_toxic': severe_toxic,
        'obscene': obscene,
        'threat': threat,
        'insult': insult,
        'identity_hate': identity_hate
    }
    df = pd.DataFrame([data])
    df.to_sql('row_comments', engine, if_exists='append', index=False)

def read_row_comment(comment_id):
    """
    Читает запись комментария по его ID.
    """
    query = f"SELECT * FROM row_comments WHERE id = '{comment_id}'"
    return pd.read_sql(query, engine)

def update_row_comment(comment_id, **kwargs):
    """
    Обновляет запись комментария по его ID.
    """
    set_clause = ', '.join([f"{key} = '{value}'" for key, value in kwargs.items()])
    query = text(f"""
    UPDATE row_comments
    SET {set_clause}
    WHERE id = :comment_id
    """)
    with engine.connect() as connection:
        connection.execute(query, {"comment_id": comment_id})

def delete_row_comment(comment_id):
    """
    Удаляет запись комментария по его ID.
    """
    query = text("DELETE FROM row_comments WHERE id = :comment_id")
    with engine.connect() as connection:
        connection.execute(query, {"comment_id": comment_id})

# ============================================
# CRUD для таблицы moderation
# ============================================

def create_moderation_entry(comment_id, comment_text, toxic=0, severe_toxic=0, obscene=0, threat=0, insult=0, identity_hate=0, stream_id=None, is_wrong_classificated=False):
    """
    Создает запись в таблице moderation.
    """
    data = {
        'id': comment_id,
        'comment_text': comment_text,
        'toxic': toxic,
        'severe_toxic': severe_toxic,
        'obscene': obscene,
        'threat': threat,
        'insult': insult,
        'identity_hate': identity_hate,
        'stream_id': stream_id,
        'is_wrong_classificated': is_wrong_classificated
    }
    df = pd.DataFrame([data])
    df.to_sql('moderation', engine, if_exists='append', index=False)

def read_moderation_entry(comment_id):
    """
    Читает запись из таблицы moderation по ID комментария.
    """
    query = f"SELECT * FROM moderation WHERE id = '{comment_id}'"
    return pd.read_sql(query, engine)

def update_moderation_entry(comment_id, **kwargs):
    """
    Обновляет запись в таблице moderation по ID комментария.
    """
    set_clause = ', '.join([f"{key} = '{value}'" for key, value in kwargs.items()])
    query = text(f"""
    UPDATE moderation
    SET {set_clause}
    WHERE id = :comment_id
    """)
    with engine.connect() as connection:
        connection.execute(query, {"comment_id": comment_id})

def delete_moderation_entry(comment_id):
    """
    Удаляет запись из таблицы moderation по ID комментария.
    """
    query = text("DELETE FROM moderation WHERE id = :comment_id")
    with engine.connect() as connection:
        connection.execute(query, {"comment_id": comment_id})