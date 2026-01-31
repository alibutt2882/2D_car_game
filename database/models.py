# database/models.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    profile_picture_path = Column(String(255), default='assets/avatars/default.png')
    registration_date = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    total_playtime_minutes = Column(Float, default=0.0)
    theme_preference = Column(String(20), default='cyberpunk')
    unlocked_cars = Column(JSON, default=lambda: ['basic'])
    unlocked_tracks = Column(JSON, default=lambda: ['city'])

    stats = relationship("GameStats", uselist=False, back_populates="user")
    sessions = relationship("GameSession", back_populates="user")
    settings = relationship("UserSettings", uselist=False, back_populates="user")

class GameStats(Base):
    __tablename__ = 'game_stats'
    stat_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True)
    total_games_played = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    highest_score = Column(Integer, default=0)
    total_distance_km = Column(Float, default=0.0)
    best_lap_time = Column(Float, default=999.99)  # Lower is better
    favorite_car = Column(String(50), default='basic')
    completion_percentage = Column(Integer, default=0)
    achievements_unlocked = Column(JSON, default=list)

    user = relationship("User", back_populates="stats")

class GameSession(Base):
    __tablename__ = 'sessions'
    session_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    game_mode = Column(String(20), default='endless')
    score = Column(Integer, default=0)
    distance_traveled = Column(Float, default=0.0)
    time_played = Column(Float, default=0.0)
    date_played = Column(DateTime, default=datetime.utcnow)
    cars_used = Column(String(50), default='basic')
    items_collected = Column(Integer, default=0)

    user = relationship("User", back_populates="sessions")

class UserSettings(Base):
    __tablename__ = 'user_settings'
    setting_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), unique=True)
    control_scheme = Column(String(20), default='keyboard')
    sound_volume = Column(Integer, default=70)
    music_volume = Column(Integer, default=50)
    graphics_quality = Column(String(10), default='medium')
    language = Column(String(10), default='en')
    notification_preferences = Column(JSON, default=lambda: {'achievements': True, 'daily_rewards': True})

    user = relationship("User", back_populates="settings")

# Database initialization
engine = create_engine('sqlite:///racing_game.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)