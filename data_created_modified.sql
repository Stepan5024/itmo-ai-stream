ALTER TABLE cleaned_comments ADD COLUMN is_wrong_classificated BOOLEAN DEFAULT FALSE;
ALTER TABLE cleaned_comments ADD COLUMN language TEXT;

ALTER TABLE cleaned_comments ADD COLUMN date_created DATETIME;
ALTER TABLE cleaned_comments ADD COLUMN date_modified DATETIME;

ALTER TABLE row_comments ADD COLUMN date_created DATETIME;
ALTER TABLE row_comments ADD COLUMN date_modified DATETIME;

ALTER TABLE moderation ADD COLUMN date_created DATETIME;
ALTER TABLE moderation ADD COLUMN date_modified DATETIME;

ALTER TABLE streams ADD COLUMN date_created DATETIME;
ALTER TABLE streams ADD COLUMN date_modified DATETIME;

UPDATE cleaned_comments SET date_created = CURRENT_TIMESTAMP, date_modified = CURRENT_TIMESTAMP;
UPDATE row_comments SET date_created = CURRENT_TIMESTAMP, date_modified = CURRENT_TIMESTAMP;
UPDATE moderation SET date_created = CURRENT_TIMESTAMP, date_modified = CURRENT_TIMESTAMP;
UPDATE streams SET date_created = CURRENT_TIMESTAMP, date_modified = CURRENT_TIMESTAMP;

CREATE TRIGGER set_cleaned_comments_dates
AFTER INSERT ON cleaned_comments
BEGIN
    UPDATE cleaned_comments
    SET date_created = CURRENT_TIMESTAMP,
        date_modified = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TRIGGER set_row_comments_dates
AFTER INSERT ON row_comments
BEGIN
    UPDATE row_comments
    SET date_created = CURRENT_TIMESTAMP,
        date_modified = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TRIGGER set_moderation_dates
AFTER INSERT ON moderation
BEGIN
    UPDATE moderation
    SET date_created = CURRENT_TIMESTAMP,
        date_modified = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TRIGGER set_streams_dates
AFTER INSERT ON streams
BEGIN
    UPDATE streams
    SET date_created = CURRENT_TIMESTAMP,
        date_modified = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_cleaned_comments_dates
AFTER UPDATE ON cleaned_comments
BEGIN
    UPDATE cleaned_comments
    SET date_modified = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_row_comments_dates
AFTER UPDATE ON row_comments
BEGIN
    UPDATE row_comments
    SET date_modified = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_moderation_dates
AFTER UPDATE ON moderation
BEGIN
    UPDATE moderation
    SET date_modified = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

CREATE TRIGGER update_streams_dates
AFTER UPDATE ON streams
BEGIN
    UPDATE streams
    SET date_modified = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;