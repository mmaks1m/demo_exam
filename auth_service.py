from sqlalchemy.orm import Session
from database import get_db
from models import User

class AuthService:
    @staticmethod
    def authenticate(login: str, password: str) -> User:
        """Аутентификация пользователя (пароли в базе в чистом виде)"""
        db: Session = next(get_db())
        try:
            print(f"Поиск пользователя: логин='{login}', пароль='{password}'")
            
            user = db.query(User).filter(
                User.login == login,
                User.password == password  # Сравниваем напрямую с тем, что в базе
            ).first()
            
            if user:
                print(f"✅ Успешная аутентификация: {user.full_name} ({user.role})")
                return user
            else:
                print(f"❌ Ошибка аутентификации для логина: {login}")
                # Для отладки проверим, есть ли пользователь с таким логином
                user_by_login = db.query(User).filter(User.login == login).first()
                if user_by_login:
                    print(f"⚠️ Пользователь найден, но пароль не совпадает")
                    print(f"   Пароль в базе: '{user_by_login.password}'")
                    print(f"   Введенный пароль: '{password}'")
                else:
                    print(f"⚠️ Пользователь с логином '{login}' не найден")
                return None
                
        except Exception as e:
            print(f"🚨 Ошибка при аутентификации: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> User:
        """Получение пользователя по ID"""
        db: Session = next(get_db())
        try:
            return db.query(User).filter(User.id == user_id).first()
        finally:
            db.close()