from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Stream(Base):
    __tablename__ = 'streams'
    id = Column(String, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    chanel_name = Column(String)

class RowComment(Base):
    __tablename__ = 'row_comments'
    id = Column(String, primary_key=True)
    comment_text = Column(String)
    toxic = Column(Integer)
    severe_toxic = Column(Integer)
    obscene = Column(Integer)
    threat = Column(Integer)
    insult = Column(Integer)
    identity_hate = Column(Integer)

class CleanedComment(Base):
    __tablename__ = 'cleaned_comments'
    id = Column(String, primary_key=True)
    comment_text = Column(String)
    toxic = Column(Integer)
    severe_toxic = Column(Integer)
    obscene = Column(Integer)
    threat = Column(Integer)
    insult = Column(Integer)
    identity_hate = Column(Integer)
    stream_id = Column(String)
    is_wrong_classificated = Column(Boolean)