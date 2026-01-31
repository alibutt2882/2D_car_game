# auth/auth_manager.py
import bcrypt
import jwt
import datetime
from database.models import Session, User
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('JWT_SECRET', 'dev-secret-key-please-change-in-production')

class AuthManager:
    def register_user(self, username, email, password):
        session = Session()
        try:
            # Check existing users
            if session.query(User).filter_by(username=username).first():
                return {'success': False, 'error': 'Username already exists'}
            if session.query(User).filter_by(email=email).first():
                return {'success': False, 'error': 'Email already registered'}
            
            # Hash password
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Create user
            user = User(
                username=username,
                email=email,
                password_hash=hashed.decode('utf-8')
            )
            session.add(user)
            session.commit()
            
            # Create related records
            from database.models import GameStats, UserSettings
            stats = GameStats(user_id=user.user_id)
            settings = UserSettings(user_id=user.user_id)
            session.add_all([stats, settings])
            session.commit()
            
            return {'success': True, 'user_id': user.user_id}
        except Exception as e:
            session.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            session.close()

    def login_user(self, identifier, password):
        session = Session()
        try:
            # Find user by username or email
            user = session.query(User).filter(
                (User.username == identifier) | (User.email == identifier)
            ).first()
            
            if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return {'success': False, 'error': 'Invalid credentials'}
            
            # Update last login
            user.last_login = datetime.datetime.utcnow()
            session.commit()
            
            # Generate JWT token
            token = jwt.encode({
                'user_id': user.user_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            }, SECRET_KEY, algorithm='HS256')
            
            return {
                'success': True,
                'token': token,
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'profile_picture': user.profile_picture_path,
                    'theme': user.theme_preference
                }
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            session.close()

    def verify_token(self, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return {'valid': True, 'user_id': payload['user_id']}
        except jwt.ExpiredSignatureError:
            return {'valid': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'valid': False, 'error': 'Invalid token'}