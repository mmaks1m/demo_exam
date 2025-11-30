from product_service import ProductService
from auth_service import AuthService
from order_service import OrderService

def test_fixed_connection():
    print("=== ТЕСТИРОВАНИЕ ПОДКЛЮЧЕНИЯ ===")
    
    # Тестируем получение товаров
    products = ProductService.get_all_products()
    print(f"Найдено товаров: {len(products)}")
    if products:
        print("Первый товар:")
        product = products[0]
        print(f"  Артикул: {product.article}")
        print(f"  Название: {product.name}")
        print(f"  Цена: {product.price}")
        print(f"  В наличии: {product.stock_quantity}")
    
    # Тестируем получение поставщиков
    suppliers = ProductService.get_all_suppliers()
    print(f"\nНайдено поставщиков: {len(suppliers)}")
    if suppliers:
        print("Первые 5 поставщиков:", suppliers[:5])
    
    # Тестируем фильтрацию
    filtered_products = ProductService.get_products_with_filters(
        search_text="", 
        supplier_filter="", 
        sort_by="stock_quantity_desc"
    )
    print(f"\nТовары после фильтрации: {len(filtered_products)}")
    
    # Тестируем заказы
    orders = OrderService.get_all_orders()
    print(f"\nНайдено заказов: {len(orders)}")

if __name__ == "__main__":
    test_fixed_connection()