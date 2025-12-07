# views/main_window.py - ИСПРАВЛЯЕМ РЕГИСТР РОЛЕЙ
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QToolBar, 
                             QLabel, QWidget, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont, QIcon
import os

class MainWindow(QMainWindow):
    logout_requested = Signal()
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        
        self.setWindowTitle("Магазин обуви")
        self.setGeometry(100, 50, 1200, 700)
        
        if os.path.exists("resources/images/icon.png"):
            self.setWindowIcon(QIcon("resources/images/icon.png"))
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
                font-family: "Times New Roman";
            }
        """)
        
        self.setup_ui()
        
        print(f"🔧 MainWindow создан для: {user.full_name if user else 'Гость'}")
        if user:
            print(f"   Роль пользователя: {user.role}")
    
    def setup_ui(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        self.setup_toolbar()
        self.show_products()
    
    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #7FFF00;
                border: none;
                border-bottom: 2px solid #5CB800;
                spacing: 10px;
                padding: 5px 10px;
            }
            QToolButton {
                background-color: #00FA9A;
                color: #000000;
                border: 1px solid #00FA9A;
                border-radius: 4px;
                padding: 5px 15px;
                font-family: "Times New Roman";
                font-weight: bold;
            }
        """)
        
        # Кнопка "Товары" - ВСЕГДА
        products_action = QAction("Товары", self)
        products_action.triggered.connect(self.show_products)
        toolbar.addAction(products_action)
        
        # Кнопка "Заказы" - ТОЛЬКО для менеджера и администратора (ИСПРАВЛЕНО РЕГИСТР!)
        if self.user and self.user.role.lower() in ['менеджер', 'администратор']:
            orders_action = QAction("Заказы", self)
            orders_action.triggered.connect(self.show_orders)
            toolbar.addAction(orders_action)
            print("   ✅ Кнопка 'Заказы' добавлена")
        
        # Растягивающий элемент
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
        
        # Кнопка "Выйти" - ВСЕГДА
        logout_action = QAction("Выйти", self)
        logout_action.triggered.connect(self.logout)
        toolbar.addAction(logout_action)
        
        # ФИО пользователя или "Гость"
        if self.user:
            user_text = self.user.full_name
            # Для роли "Клиент" не показываем скобки
            if self.user.role.lower() == 'клиент':
                role_text = ""
            else:
                role_text = f" ({self.user.role})"
        else:
            user_text = "Гость"
            role_text = ""
        
        user_label = QLabel(f"👤 {user_text}{role_text}")
        user_label.setFont(QFont("Times New Roman", 11, QFont.Bold))
        user_label.setStyleSheet("""
            QLabel {
                color: #000000;
                background-color: rgba(255, 255, 255, 0.5);
                padding: 5px 15px;
                border-radius: 4px;
            }
        """)
        toolbar.addWidget(user_label)
        
        print(f"   👤 В тулбаре отображается: {user_text}{role_text}")
    
    def logout(self):
        print("🔒 Запрос на выход из системы")
        self.logout_requested.emit()
        self.close()
    
    def show_products(self):
        print("🔄 Открываем товары...")
        
        from views.product_list_window import ProductListWindow
        
        # Удаляем старый виджет если есть
        for i in reversed(range(self.central_widget.count())):
            widget = self.central_widget.widget(i)
            if widget:
                self.central_widget.removeWidget(widget)
                widget.deleteLater()
        
        product_window = ProductListWindow(self.user)
        self.central_widget.addWidget(product_window)
        self.central_widget.setCurrentWidget(product_window)
        
        # Устанавливаем заголовок окна
        if self.user and self.user.role.lower() in ['менеджер', 'администратор']:
            self.setWindowTitle("Товары - Магазин обуви (Режим управления)")
        else:
            self.setWindowTitle("Товары - Магазин обуви")
    
    def show_orders(self):
        # ИСПРАВЛЕНО: проверяем role.lower()
        if self.user and self.user.role.lower() in ['менеджер', 'администратор']:
            print("🔄 Открываем заказы...")
            
            from views.order_list_window import OrderListWindow
            
            for i in reversed(range(self.central_widget.count())):
                widget = self.central_widget.widget(i)
                if widget:
                    self.central_widget.removeWidget(widget)
                    widget.deleteLater()
            
            order_window = OrderListWindow(self.user)
            self.central_widget.addWidget(order_window)
            self.central_widget.setCurrentWidget(order_window)
            
            self.setWindowTitle("Заказы - Магазин обуви")
        else:
            print("⛔ Нет прав для просмотра заказов")