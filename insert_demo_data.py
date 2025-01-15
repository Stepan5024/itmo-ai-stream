from datetime import datetime
from application.db_utils import (
    create_stream,
    create_row_comment,
    create_moderation_entry,
    read_stream,
    read_row_comment,
    read_moderation_entry,
    update_stream,
    update_row_comment,
    update_moderation_entry,
    delete_stream,
    delete_row_comment,
    delete_moderation_entry
)

if __name__ == "__main__":
    create_stream(
        stream_id="stepycdragon",
        start_time=datetime.now(),
        end_time=datetime.now(),
        chanel_name="example_channel"
    )

    # Пример создания записи комментария
    create_row_comment(
        comment_id="comment_456",
        comment_text="Это тестовый комментарий"
    )

    # Пример создания записи в moderation
    create_moderation_entry(
        comment_id="comment_456",
        comment_text="Это тестовый комментарий",
        stream_id="stream_123"
    )

    # Пример чтения записи
    print("Чтение данных из таблицы streams:")
    print(read_stream("stream_123"))

    print("\nЧтение данных из таблицы row_comments:")
    print(read_row_comment("comment_456"))

    print("\nЧтение данных из таблицы moderation:")
    print(read_moderation_entry("comment_456"))

    # Пример обновления записи
    update_stream("stream_123", chanel_name="updated_channel")
    update_row_comment("comment_456", toxic=1)
    update_moderation_entry("comment_456", is_wrong_classificated=True)

    print("\nПосле обновления данных:")
    print(read_stream("stream_123"))
    print(read_row_comment("comment_456"))
    print(read_moderation_entry("comment_456"))

    # Пример удаления записи
    delete_stream("stream_123")
    delete_row_comment("comment_456")
    delete_moderation_entry("comment_456")

    print("\nПосле удаления данных:")
    print(read_stream("stream_123"))  # Должно вернуть пустой DataFrame
    print(read_row_comment("comment_456"))  # Должно вернуть пустой DataFrame
    print(read_moderation_entry("comment_456"))  # Должно вернуть пустой DataFrame