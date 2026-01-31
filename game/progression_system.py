# game/progression_system.py
import json
from database.models import Session, User, GameStats

class ProgressionSystem:
    def __init__(self, user_id):
        self.user_id = user_id
        self.load_unlockables()
    
    def load_unlockables(self):
        # Define unlockable content
        self.cars = {
            'basic': {'cost': 0, 'speed': 1.0, 'handling': 1.0, 'unlocked': True},
            'neon_racer': {'cost': 5000, 'speed': 1.3, 'handling': 0.9, 'unlocked': False},
            'cyber_speeder': {'cost': 15000, 'speed': 1.8, 'handling': 0.7, 'unlocked': False}
        }
        
        self.tracks = {
            'city': {'cost': 0, 'unlocked': True},
            'neon_highway': {'cost': 10000, 'unlocked': False},
            'cyber_alley': {'cost': 25000, 'unlocked': False}
        }
        
        self.achievements = [
            {'id': 'first_race', 'name': 'Rookie Driver', 'desc': 'Complete your first race', 'xp': 100},
            {'id': 'speed_demon', 'name': 'Speed Demon', 'desc': 'Reach 300km/h', 'xp': 500},
            {'id': 'distance_master', 'name': 'Marathon Runner', 'desc': 'Travel 100km total', 'xp': 2000}
        ]
    
    def check_unlocks(self, session_data):
        session = Session()
        try:
            user = session.query(User).filter_by(user_id=self.user_id).first()
            stats = session.query(GameStats).filter_by(user_id=self.user_id).first()
            
            # Check distance-based unlocks
            total_km = stats.total_distance_km if stats else 0
            
            if total_km >= 5.0 and 'neon_racer' not in user.unlocked_cars:
                user.unlocked_cars.append('neon_racer')
                self.show_unlock_notification("Neon Racer unlocked!")
            
            if total_km >= 20.0 and 'cyber_speeder' not in user.unlocked_cars:
                user.unlocked_cars.append('cyber_speeder')
                self.show_unlock_notification("Cyber Speeder unlocked!")
            
            # Check achievement conditions
            new_achievements = []
            if stats.total_games_played >= 1 and 'first_race' not in stats.achievements_unlocked:
                new_achievements.append('first_race')
            
            if session_data.get('max_speed', 0) >= 300 and 'speed_demon' not in stats.achievements_unlocked:
                new_achievements.append('speed_demon')
            
            if total_km >= 100 and 'distance_master' not in stats.achievements_unlocked:
                new_achievements.append('distance_master')
            
            # Grant new achievements
            for ach_id in new_achievements:
                stats.achievements_unlocked.append(ach_id)
                self.grant_achievement_reward(ach_id)
            
            session.commit()
            return new_achievements
        finally:
            session.close()
    
    def show_unlock_notification(self, message):
        # Would trigger UI notification system
        print(f"✨ UNLOCKED: {message}")
    
    def grant_achievement_reward(self, achievement_id):
        rewards = {
            'first_race': 500,
            'speed_demon': 2000,
            'distance_master': 5000
        }
        # Would add currency to user account
        print(f"💰 Reward granted: {rewards.get(achievement_id, 0)} credits")