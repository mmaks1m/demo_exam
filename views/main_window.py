# views/main_window.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from PySide6.QtWidgets import (QMainWindow, QStackedWidget, QToolBar, 
                             QLabel, QWidget, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QFont, QIcon, QPalette, QColor
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
        
        # УПРОЩЕННЫЙ СТИЛЬ - убираем глобальные стили для QToolButton
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFFFFF;
                font-family: "Times New Roman";
            }
        """)
        
        # Устанавливаем цвет фона через палитру (более надежно)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#FFFFFF"))
        self.setPalette(palette)
        
        self.setup_ui()
        
    def setup_ui(self):
        self.central_widget = QStackedWidget()
        self.central_widget.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(self.central_widget)
        
        self.setup_toolbar()
        self.show_products()
    
    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setObjectName("mainToolbar")  # Даем имя для селектора стилей
        
        # Стиль ТОЛЬКО для этого тулбара
        toolbar.setStyleSheet("""
            QToolBar#mainToolbar {
                background-color: #7FFF00;
                border: none;
                border-bottom: 2px solid #5CB800;
                spacing: 5px;
                padding: 2px 5px;
                margin: 0px;
            }
            /* Стиль для QToolButton внутри этого тулбара */
            QToolBar#mainToolbar QToolButton {
                background-color: #00FA9A;
                color: #000000;
                border: 1px solid #00FA9A;
                border-radius: 4px;
                padding: 5px 15px;
                font-family: "Times New Roman";
                font-weight: bold;
                min-width: 60px;
            }
            QToolBar#mainToolbar QToolButton:hover {
                background-color: #00E58B;
                border-color: #00E58B;
            }
            QToolBar#mainToolbar QToolButton:pressed {
                background-color: #00D07A;
                border-color: #00D07A;
            }
            /* Стиль для QToolButton в состоянии "включено" (нажата) */
            QToolBar#mainToolbar QToolButton:checked {
                background-color: #00D07A;
                border-color: #00D07A;
            }
        """)
        
        self.addToolBar(toolbar)
        
        # Кнопки
        products_action = QAction("Товары", self)
        products_action.triggered.connect(self.show_products)
        toolbar.addAction(products_action)
        
        if self.user and self.user.role.lower() in ['менеджер', 'администратор']:
            orders_action = QAction("Заказы", self)
            orders_action.triggered.connect(self.show_orders)
            toolbar.addAction(orders_action)
        
        # Растягивающий элемент
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        spacer.setStyleSheet("background-color: transparent;")  # Прозрачный фон
        toolbar.addWidget(spacer)
        
        # Кнопка выхода
        logout_action = QAction("Выйти", self)
        logout_action.triggered.connect(self.logout)
        toolbar.addAction(logout_action)
        
        # ФИО пользователя
        if self.user:
            user_text = self.user.full_name
            if self.user.role.lower() == 'клиент':
                role_text = ""
            else:
                role_text = f" ({self.user.role})"
        else:
            user_text = "Гость"
            role_text = ""
        
        user_label = QLabel(f"{user_text}{role_text}")
        user_label.setFont(QFont("Times New Roman", 11, QFont.Bold))
        user_label.setStyleSheet("""
            QLabel {
                color: #000000;
                background-color: #7FFF00;
                padding: 3px 10px;
                border-radius: 3px;
                margin-right: 5px;
                border: 1px solid rgba(0, 0, 0, 0.1);
            }
        """)
        toolbar.addWidget(user_label)
    
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
        
        if self.user and self.user.role.lower() in ['менеджер', 'администратор']:
            self.setWindowTitle("Товары - Магазин обуви (Режим управления)")
        else:
            self.setWindowTitle("Товары - Магазин обуви")
    
    def show_orders(self):
        if self.user and self.user.role.lower() in ['менеджер', 'администратор']:
            print("Открываем заказы...")
            
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
            print("Нет прав для просмотра заказов")