from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QStatusBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QToolBar
from views.product_list_window import ProductListWindow
from views.order_list_window import OrderListWindow

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Магазин обуви")
        self.setGeometry(100, 50, 1200, 700)
        
        print(f"🎯 Создано главное окно для пользователя: {user.full_name if user else 'Гость'}")
        
        # Устанавливаем фон для главного окна
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #f8f9fa, stop: 0.5 #e9ecef, stop: 1 #f8f9fa);
            }
        """)
        
        self.setup_ui()
        
    def setup_ui(self):
        print("🔄 Настройка интерфейса главного окна...")
        
        # Центральный виджет
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        # Создаем тулбар
        self.setup_toolbar()
        
        # Создаем статусбар
        self.setup_statusbar()
        
        # Показываем окно товаров по умолчанию
        self.show_products()
        
        print("✅ Интерфейс главного окна настроен")
    
    def setup_toolbar(self):
        print("🔄 Создание панели инструментов...")
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Кнопка "Товары"
        products_action = QAction("Товары", self)
        products_action.triggered.connect(self.show_products)
        toolbar.addAction(products_action)
        
        # Кнопка "Заказы" (только для менеджера и администратора)
        if self.user and self.user.role in ['менеджер', 'администратор']:
            orders_action = QAction("Заказы", self)
            orders_action.triggered.connect(self.show_orders)
            toolbar.addAction(orders_action)
            print("✅ Добавлена кнопка 'Заказы'")
        
        toolbar.addSeparator()
        
        # Кнопка выхода
        logout_action = QAction("Выйти", self)
        logout_action.triggered.connect(self.logout)
        toolbar.addAction(logout_action)
        
        print("✅ Панель инструментов создана")
    
    def setup_statusbar(self):
        statusbar = QStatusBar()
        user_info = f"Пользователь: {self.user.full_name if self.user else 'Гость'} ({self.user.role if self.user else 'Гость'})"
        statusbar.showMessage(user_info)
        self.setStatusBar(statusbar)
        print(f"✅ Статусбар установлен: {user_info}")
    
    def show_products(self):
        """Показать окно списка товаров"""
        print("🔄 Открытие окна товаров...")
        product_window = ProductListWindow(self.user)
        self.central_widget.addWidget(product_window)
        self.central_widget.setCurrentWidget(product_window)
        self.setWindowTitle("Товары - Магазин обуви")
        print("✅ Окно товаров открыто")
    
    def show_orders(self):
        """Показать окно списка заказов (только для менеджера и администратора)"""
        if self.user and self.user.role in ['менеджер', 'администратор']:
            print("🔄 Открытие окна заказов...")
            order_window = OrderListWindow(self.user)
            self.central_widget.addWidget(order_window)
            self.central_widget.setCurrentWidget(order_window)
            self.setWindowTitle("Заказы - Магазин обуви")
            print("✅ Окно заказов открыто")
    
    def logout(self):
        print("🔄 Выход из системы...")
        from views.login_window import LoginWindow
        login_window = LoginWindow()
        login_window.show()
        self.close()
        print("✅ Возврат к окну входа")