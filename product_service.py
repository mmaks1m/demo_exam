from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models import Product

class ProductService:
    @staticmethod
    def get_all_products():
        """Получение всех товаров"""
        db: Session = next(get_db())
        try:
            products = db.query(Product).all()
            return products
        except Exception as e:
            print(f"Ошибка при получении товаров: {e}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_products_with_filters(search_text="", supplier_filter="", sort_by="name"):
        """Получение товаров с фильтрацией и сортировкой"""
        db: Session = next(get_db())
        try:
            query = db.query(Product)
            
            # Поиск по тексту (по всем текстовым полям)
            if search_text:
                query = query.filter(
                    or_(
                        Product.name.ilike(f"%{search_text}%"),
                        Product.description.ilike(f"%{search_text}%"),
                        Product.category.ilike(f"%{search_text}%"),
                        Product.manufacturer.ilike(f"%{search_text}%"),
                        Product.supplier.ilike(f"%{search_text}%"),
                        Product.article.ilike(f"%{search_text}%")
                    )
                )
            
            # Фильтрация по поставщику
            if supplier_filter and supplier_filter != "Все поставщики":
                query = query.filter(Product.supplier == supplier_filter)
            
            # Сортировка
            if sort_by == "stock_quantity_asc":
                query = query.order_by(Product.stock_quantity.asc())
            elif sort_by == "stock_quantity_desc":
                query = query.order_by(Product.stock_quantity.desc())
            elif sort_by == "price_asc":
                query = query.order_by(Product.price.asc())
            elif sort_by == "price_desc":
                query = query.order_by(Product.price.desc())
            else:  # сортировка по названию по умолчанию
                query = query.order_by(Product.name.asc())
            
            return query.all()
        except Exception as e:
            print(f"Ошибка при фильтрации товаров: {e}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_all_suppliers():
        """Получение всех уникальных поставщиков"""
        db: Session = next(get_db())
        try:
            suppliers = db.query(Product.supplier).distinct().order_by(Product.supplier).all()
            return [supplier[0] for supplier in suppliers if supplier[0]]  # Извлекаем значения из кортежей
        except Exception as e:
            print(f"Ошибка при получении поставщиков: {e}")
            return []
        finally:
            db.close()
    
    @staticmethod
    def get_product_by_article(article: str):
        """Получение товара по артикулу"""
        db: Session = next(get_db())
        try:
            return db.query(Product).filter(Product.article == article).first()
        finally:
            db.close()
    
    @staticmethod
    def create_product(product_data: dict):
        """Создание нового товара"""
        db: Session = next(get_db())
        try:
            product = Product(**product_data)
            db.add(product)
            db.commit()
            db.refresh(product)
            return product
        except Exception as e:
            db.rollback()
            print(f"Ошибка при создании товара: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def update_product(article: str, product_data: dict):
        """Обновление товара"""
        db: Session = next(get_db())
        try:
            product = db.query(Product).filter(Product.article == article).first()
            if product:
                for key, value in product_data.items():
                    setattr(product, key, value)
                db.commit()
                db.refresh(product)
            return product
        except Exception as e:
            db.rollback()
            print(f"Ошибка при обновлении товара: {e}")
            return None
        finally:
            db.close()
    
    @staticmethod
    def delete_product(article: str):
        """Удаление товара"""
        db: Session = next(get_db())
        try:
            product = db.query(Product).filter(Product.article == article).first()
            if product:
                # Проверяем, есть ли товар в заказах
                if product.order_items:
                    return False, "Товар присутствует в заказе, удаление невозможно"
                
                db.delete(product)
                db.commit()
                return True, "Товар успешно удален"
            return False, "Товар не найден"
        except Exception as e:
            db.rollback()
            print(f"Ошибка при удалении товара: {e}")
            return False, f"Ошибка при удалении: {e}"
        finally:
            db.close()