# views/main_window.py
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QStatusBar, 
                             QToolBar, QLabel, QHBoxLayout, QWidget, 
                             QSpacerItem, QSizePolicy)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QFont

from views.product_list_window import ProductListWindow
from views.order_list_window import OrderListWindow

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowTitle("Магазин обуви")
        self.setGeometry(100, 50, 1200, 700)
        
        print(f"🎯 Создано главное окно для пользователя: {user.full_name if user else 'Гость'}")
        
        # Устанавливаем белый фон
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
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
        
        # Показываем окно товаров по умолчанию
        self.show_products()
        
        print("✅ Интерфейс главного окна настроен")
    
    def setup_toolbar(self):
        print("🔄 Создание панели инструментов...")
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setFixedHeight(50)
        self.addToolBar(toolbar)
        
        # Стиль для тулбара
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #7FFF00;  /* Дополнительный фон из руководства */
                border: none;
                border-bottom: 2px solid #5CB800;
                spacing: 10px;
                padding: 5px 10px;
            }
            QToolButton {
                background-color: #00FA9A;  /* Акцентный цвет */
                color: #000000;  /* Черный текст */
                border: 1px solid #00FA9A;
                border-radius: 4px;
                padding: 8px 20px;
                font-family: "Times New Roman";
                font-weight: bold;
                font-size: 11pt;
                min-height: 30px;
            }
            QToolButton:hover {
                background-color: #00E58B;
                border-color: #00E58B;
            }
            QToolButton:pressed {
                background-color: #00D07A;
                border-color: #00D07A;
            }
        """)
        
        # Кнопка "Товары"
        self.products_action = QAction("Товары", self)
        self.products_action.triggered.connect(self.show_products)
        toolbar.addAction(self.products_action)
        
        # Кнопка "Заказы" (только для менеджера и администратора)
        if self.user and self.user.role in ['менеджер', 'администратор']:
            self.orders_action = QAction("Заказы", self)
            self.orders_action.triggered.connect(self.show_orders)
            toolbar.addAction(self.orders_action)
            print("✅ Добавлена кнопка 'Заказы'")
        
        # Растягивающий элемент между кнопками и информацией о пользователе
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer_action = toolbar.addWidget(spacer)
        
        # Создаем виджет с информацией о пользователе
        self.user_widget = self.create_user_widget()
        self.user_widget_action = toolbar.addWidget(self.user_widget)
        
        # Кнопка выхода
        self.logout_action = QAction("Выйти", self)
        self.logout_action.triggered.connect(self.logout)
        toolbar.addAction(self.logout_action)
        
        print("✅ Панель инструментов создана")
    
    def create_user_widget(self):
        """Создаем виджет с информацией о пользователе"""
        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        user_layout.setContentsMargins(10, 0, 10, 0)
        user_layout.setSpacing(8)
        
        # Информация о пользователе
        if self.user:
            # ФИО пользователя
            name_label = QLabel(f"👤 {self.user.full_name}")
            name_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
            name_label.setStyleSheet("""
                QLabel {
                    color: #000000;
                    background-color: rgba(255, 255, 255, 0.7);
                    padding: 5px 10px;
                    border-radius: 4px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
            """)
            
            # Роль пользователя
            role_label = QLabel(f"({self.user.role})")
            role_label.setFont(QFont("Times New Roman", 9))
            role_label.setStyleSheet("""
                QLabel {
                    color: #555555;
                    background-color: rgba(245, 245, 245, 0.7);
                    padding: 5px 10px;
                    border-radius: 4px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    font-style: italic;
                }
            """)
        else:
            # Для гостя
            name_label = QLabel("👤 Гость")
            name_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
            name_label.setStyleSheet("""
                QLabel {
                    color: #000000;
                    background-color: rgba(255, 255, 255, 0.7);
                    padding: 5px 10px;
                    border-radius: 4px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                }
            """)
            
            role_label = QLabel("(неавторизованный)")
            role_label.setFont(QFont("Times New Roman", 9))
            role_label.setStyleSheet("""
                QLabel {
                    color: #555555;
                    background-color: rgba(245, 245, 245, 0.7);
                    padding: 5px 10px;
                    border-radius: 4px;
                    border: 1px solid rgba(0, 0, 0, 0.1);
                    font-style: italic;
                }
            """)
        
        # Добавляем элементы
        user_layout.addWidget(name_label)
        user_layout.addWidget(role_label)
        
        return user_widget
    
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
        
        # Закрываем текущее окно
        self.close()
        
        # Создаем новое окно входа
        from PySide6.QtWidgets import QApplication
        from views.login_window import LoginWindow
        
        app = QApplication.instance()
        login_window = LoginWindow()
        login_window.show()
        
        print("✅ Возврат к окну входа")