from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from database import get_db
from models import Product, OrderItem
import os

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
        db: Session = next(get_db())
        try:
            query = db.query(Product)
            
            if search_text:
                search_text = search_text.strip()
                print(f"🔍 Поисковый запрос: '{search_text}'")
    
                words = [word.strip() for word in search_text.split() if word.strip()]
                print(f"🔍 Слова для поиска: {words}")
                
                if words:
                    for word in words:
                        word_condition = or_(
                            Product.name.ilike(f"%{word}%"),
                            Product.description.ilike(f"%{word}%"),
                            Product.category.ilike(f"%{word}%"),
                            Product.manufacturer.ilike(f"%{word}%"),
                            Product.supplier.ilike(f"%{word}%"),
                            Product.article.ilike(f"%{word}%")
                        )
                        query = query.filter(word_condition)
            
            # Фильтрация по поставщику
            if supplier_filter and supplier_filter != "Все поставщики":
                query = query.filter(Product.supplier == supplier_filter)
                print(f"🔍 Фильтр по поставщику: {supplier_filter}")
            
            # Сортировка
            sort_mapping = {
                "stock_quantity_asc": Product.stock_quantity.asc(),
                "stock_quantity_desc": Product.stock_quantity.desc(),
                "price_asc": Product.price.asc(),
                "price_desc": Product.price.desc(),
                "name_desc": Product.name.desc(),
                "name_asc": Product.name.asc()
            }
            
            sort_order = sort_mapping.get(sort_by, Product.name.asc())
            query = query.order_by(sort_order)
            
            results = query.all()
            print(f"✅ Найдено товаров: {len(results)}")
            
            return results
            
        except Exception as e:
            print(f"❌ Ошибка при фильтрации товаров: {e}")
            import traceback
            traceback.print_exc()
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
    def can_delete_product(article: str):
        """Проверяет, можно ли удалить товар (не присутствует в заказе)"""
        db: Session = next(get_db())
        try:
            # Проверяем, есть ли товар в order_items
            product_in_order = db.query(OrderItem).filter(
                OrderItem.product_article == article
            ).first()
            
            return product_in_order is None  # Можно удалить если нет в заказах
        finally:
            db.close()
    
    @staticmethod
    def delete_product(article: str):
        db: Session = next(get_db())
        try:
            product = db.query(Product).filter(Product.article == article).first()
            if not product:
                return False, "Товар не найден"
            
            if not ProductService.can_delete_product(article):
                return False, "Товар присутствует в заказе, удаление невозможно"
            
            if product.image_path and os.path.exists(f"resources/images/{product.image_path}"):
                try:
                    os.remove(f"resources/images/{product.image_path}")
                except Exception as e:
                    print(f"Не удалось удалить изображение: {e}")
            
            db.delete(product)
            db.commit()
            return True, "Товар успешно удален"
        except Exception as e:
            db.rollback()
            print(f"Ошибка при удалении товара: {e}")
            return False, f"Ошибка при удалении: {e}"
        finally:
            db.close()
            
            