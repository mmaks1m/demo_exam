# order_service.py - ДОБАВЛЯЕМ МЕТОД ДЛЯ СОХРАНЕНИЯ ТОВАРОВ
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Order, OrderItem, User, PickupPoint, Product

class OrderService:
    @staticmethod
    def get_all_orders():
        """Получение всех заказов с связанными данными (используем joinedload)"""
        db: Session = next(get_db())
        try:
            # Используем joinedload для загрузки всех связанных данных
            orders = db.query(Order)\
                .options(
                    joinedload(Order.user),
                    joinedload(Order.pickup_point),
                    joinedload(Order.order_items).joinedload(OrderItem.product)
                )\
                .order_by(Order.order_date.desc())\
                .all()
            return orders
        except Exception as e:
            print(f"❌ Ошибка при получении заказов: {e}")
            import traceback
            traceback.print_exc()
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_order_by_id(order_id: int):
        """Получение заказа по ID со всеми связанными данными"""
        db: Session = next(get_db())
        try:
            order = db.query(Order)\
                .options(
                    joinedload(Order.user),
                    joinedload(Order.pickup_point),
                    joinedload(Order.order_items).joinedload(OrderItem.product)
                )\
                .filter(Order.id == order_id)\
                .first()
            return order
        finally:
            db.close()
    
    @staticmethod
    def create_order(order_data: dict):
        db: Session = next(get_db())
        try:
            pickup_point_address = order_data.pop('pickup_point_address', None)
            pickup_point_id = order_data.get('pickup_point_id', None)
            
            if pickup_point_address and not pickup_point_id:
                pickup_point = db.query(PickupPoint).filter(
                    PickupPoint.address.ilike(pickup_point_address.strip())
                ).first()
                
                if not pickup_point:
                    pickup_point = PickupPoint(address=pickup_point_address.strip())
                    db.add(pickup_point)
                    db.commit()
                    db.refresh(pickup_point)
                
                order_data['pickup_point_id'] = pickup_point.id
            
            order = Order(**order_data)
            db.add(order)
            db.commit()
            db.refresh(order)
            
            order = db.query(Order)\
                .options(
                    joinedload(Order.user),
                    joinedload(Order.pickup_point)
                )\
                .filter(Order.id == order.id)\
                .first()
            
            return order
        except Exception as e:
            db.rollback()
            print(f"❌ Ошибка при создании заказа: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            db.close()
    
    @staticmethod
    def update_order(order_id: int, order_data: dict):
        """Обновление заказа с обработкой адреса"""
        db: Session = next(get_db())
        try:
            order = db.query(Order).filter(Order.id == order_id).first()
            if not order:
                return None
            
            # Обрабатываем адрес пункта выдачи
            pickup_point_address = order_data.pop('pickup_point_address', None)
            
            if pickup_point_address:
                # Находим или создаем пункт выдачи
                pickup_point = db.query(PickupPoint).filter(
                    PickupPoint.address.ilike(pickup_point_address.strip())
                ).first()
                
                if not pickup_point:
                    pickup_point = PickupPoint(address=pickup_point_address.strip())
                    db.add(pickup_point)
                    db.commit()
                    db.refresh(pickup_point)
                
                order_data['pickup_point_id'] = pickup_point.id
            
            # Обновляем остальные поля
            for key, value in order_data.items():
                setattr(order, key, value)
            
            db.commit()
            db.refresh(order)
            
            # Загружаем связанные данные для возврата
            order = db.query(Order)\
                .options(
                    joinedload(Order.user),
                    joinedload(Order.pickup_point)
                )\
                .filter(Order.id == order.id)\
                .first()
            
            return order
        except Exception as e:
            db.rollback()
            print(f"❌ Ошибка при обновлении заказа: {e}")
            import traceback
            traceback.print_exc()
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
            print(f"❌ Ошибка при удалении заказа: {e}")
            import traceback
            traceback.print_exc()
            return False, f"Ошибка при удалении: {e}"
        finally:
            db.close()
    
    @staticmethod
    def get_all_pickup_points():
        """Получение всех пунктов выдачи"""
        db: Session = next(get_db())
        try:
            points = db.query(PickupPoint).order_by(PickupPoint.address).all()
            return points
        finally:
            db.close()
    
    @staticmethod
    def add_order_items(order_id: int, items_data: list):
        """Добавление товаров в заказ"""
        db: Session = next(get_db())
        try:
            # Удаляем старые товары из заказа
            db.query(OrderItem).filter(OrderItem.order_id == order_id).delete()
            
            # Добавляем новые товары
            for item in items_data:
                order_item = OrderItem(
                    order_id=order_id,
                    product_article=item['product_article'],
                    quantity=item['quantity']
                )
                db.add(order_item)
            
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"❌ Ошибка при добавлении товаров в заказ: {e}")
            return False
        finally:
            db.close()
    
    @staticmethod
    def get_order_items(order_id: int):
        """Получение товаров в заказе"""
        db: Session = next(get_db())
        try:
            items = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
            return items
        finally:
            db.close()