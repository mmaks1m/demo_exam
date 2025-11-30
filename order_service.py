from sqlalchemy.orm import Session
from database import get_db
from models import Order, OrderItem, User, PickupPoint, Product

class OrderService:
    @staticmethod
    def get_all_orders():
        """Получение всех заказов с связанными данными"""
        db: Session = next(get_db())
        try:
            orders = db.query(Order).join(User).join(PickupPoint).all()
            return orders
        except Exception as e:
            print(f"Ошибка при получении заказов: {e}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_order_by_id(order_id: int):
        """Получение заказа по ID"""
        db: Session = next(get_db())
        try:
            return db.query(Order).filter(Order.id == order_id).first()
        finally:
            db.close()
    
    @staticmethod
    def create_order(order_data: dict):
        """Создание нового заказа"""
        db: Session = next(get_db())
        try:
            order = Order(**order_data)
            db.add(order)
            db.commit()
            db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании заказа: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def update_order(order_id: int, order_data: dict):
        """Обновление заказа"""
        db: Session = next(get_db())
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                for key, value in order_data.items():
                    setattr(order, key, value)
                db.commit()
                db.refresh(order)
            return order
        except Exception as e:
            db.rollback()
            print(f"Ошибка при обновлении заказа: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def delete_order(order_id: int):
        """Удаление заказа"""
        db: Session = next(get_db())
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if order:
                # Удаляем связанные элементы заказа
                db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
                db.delete(order)
                db.commit()
                return True, "Заказ успешно удален"
            return False, "Заказ не найден"
        except Exception as e:
            db.rollback()
            print(f"Ошибка при удалении заказа: {e}")
            return False, f"Ошибка при удалении: {e}"
        finally:
            db.close()