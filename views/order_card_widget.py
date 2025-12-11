# views/order_card_widget.py - ИСПРАВЛЕННЫЙ С ВСЕМИ ПРОБЛЕМАМИ
from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                             QFrame, QPushButton, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor
from datetime import datetime

class OrderCardWidget(QWidget):
    """Виджет карточки заказа"""
    edit_requested = Signal(object)  # Сигнал для редактирования
    delete_requested = Signal(object)  # Сигнал для удаления
    
    def __init__(self, order, user):
        super().__init__()
        self.order = order
        self.user = user
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса карточки"""
        # Основной контейнер карточки
        card_frame = QFrame()
        card_frame.setFrameStyle(QFrame.Box)
        card_frame.setLineWidth(1)
        card_frame.setFixedHeight(260)
        
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        
        main_layout = QHBoxLayout(card_frame)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(20)
        
        # Левая часть - информация о заказе
        left_frame = QFrame()
        left_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        left_layout = QVBoxLayout(left_frame)
        left_layout.setSpacing(8)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Артикул заказа - формируем из товаров в заказе
        article = self.generate_order_article()
        
        article_label = QLabel(f"<b>Артикул заказа:</b> {article}")
        article_label.setFont(QFont("Times New Roman", 12))
        article_label.setStyleSheet("color: #000000;")
        article_label.setWordWrap(True)
        article_label.setMinimumHeight(25)
        
        # Статус заказа (с подсветкой)
        status = getattr(self.order, 'status', 'не указан')
        status_label = QLabel(f"<b>Статус заказа:</b> {status}")
        status_label.setFont(QFont("Times New Roman", 12))
        
        # Подсветка статуса цветом
        status_lower = str(status).lower()
        if status_lower in ['выполнен', 'доставлен']:
            status_label.setStyleSheet("""
                color: #000000; 
                font-weight: bold; 
                background-color: #d4edda; 
                padding: 3px 6px; 
                border-radius: 3px;
                min-height: 25px;
            """)
        elif status_lower in ['отменен', 'отменён']:
            status_label.setStyleSheet("""
                color: #000000; 
                font-weight: bold; 
                background-color: #f8d7da; 
                padding: 3px 6px; 
                border-radius: 3px;
                min-height: 25px;
            """)
        elif status_lower in ['в обработке', 'обработка']:
            status_label.setStyleSheet("""
                color: #000000; 
                font-weight: bold; 
                background-color: #fff3cd; 
                padding: 3px 6px; 
                border-radius: 3px;
                min-height: 25px;
            """)
        else:
            status_label.setStyleSheet("color: #000000; min-height: 25px;")
        
        # Адрес пункта выдачи
        address = "Не указан"
        if hasattr(self.order, 'pickup_point') and self.order.pickup_point:
            address = self.order.pickup_point.address
        
        address_label = QLabel(f"<b>Адрес пункта выдачи:</b> {address}")
        address_label.setFont(QFont("Times New Roman", 12))
        address_label.setStyleSheet("color: #000000;")
        address_label.setWordWrap(True)
        address_label.setMinimumHeight(25)
        
        # Дата заказа
        date_str = "Не указана"
        if hasattr(self.order, 'order_date') and self.order.order_date:
            try:
                date_str = self.order.order_date.strftime("%d.%m.%Y %H:%M")
            except:
                date_str = "Ошибка формата"
        
        date_label = QLabel(f"<b>Дата заказа:</b> {date_str}")
        date_label.setFont(QFont("Times New Roman", 12))
        date_label.setStyleSheet("color: #000000; min-height: 25px;")
        
        # Дата доставки - ДОБАВЛЯЕМ В ПРАВУЮ ЧАСТЬ
        delivery_date_str = "Не указана"
        if hasattr(self.order, 'delivery_date') and self.order.delivery_date:
            try:
                delivery_date_str = self.order.delivery_date.strftime("%d.%m.%Y %H:%M")
            except:
                delivery_date_str = "Ошибка формата"
        
        delivery_label = QLabel(f"<b>Дата доставки:</b> {delivery_date_str}")
        delivery_label.setFont(QFont("Times New Roman", 12))
        delivery_label.setStyleSheet("color: #000000; min-height: 25px;")
        
        # Пользователь (если есть права администратора/менеджера)
        if self.user and self.user.role.lower() in ['администратор', 'менеджер']:
            user_name = "Неизвестно"
            if hasattr(self.order, 'user') and self.order.user:
                user_name = self.order.user.full_name
            
            user_label = QLabel(f"<b>Пользователь:</b> {user_name}")
            user_label.setFont(QFont("Times New Roman", 12))
            user_label.setStyleSheet("color: #000000; min-height: 25px;")
            left_layout.addWidget(user_label)
        
        left_layout.addWidget(article_label)
        left_layout.addWidget(status_label)
        left_layout.addWidget(address_label)
        left_layout.addWidget(date_label)
        left_layout.addStretch()
        
        # Правая часть - дата доставки и кнопки управления
        right_frame = QFrame()
        right_frame.setFixedWidth(200)
        right_layout = QVBoxLayout(right_frame)
        right_layout.setSpacing(10)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Дата доставки в правой части
        right_layout.addWidget(delivery_label)
        right_layout.addStretch()
        
        # Кнопки для администратора
        if self.user and self.user.role.lower() == 'администратор':
            edit_btn = QPushButton("Редактировать")
            edit_btn.setMinimumHeight(40)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7FFF00;
                    color: black;
                    font-weight: bold;
                    border: 2px solid #7FFF00;
                    border-radius: 4px;
                    font-family: "Times New Roman";
                    font-size: 12px;
                    padding: 8px 5px;
                }
                QPushButton:hover {
                    background-color: #00FA9A;
                    border-color: #00FA9A;
                }
                QPushButton:pressed {
                    background-color: #06bf78;
                    border-color: #06bf78;
                }
            """)
            edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.order))
            
            delete_btn = QPushButton("Удалить")
            delete_btn.setMinimumHeight(40)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7FFF00;
                    color: black;
                    font-weight: bold;
                    border: 2px solid #7FFF00;
                    border-radius: 4px;
                    font-family: "Times New Roman";
                    font-size: 12px;
                    padding: 8px 5px;
                }
                QPushButton:hover {
                    background-color: #00FA9A;
                    border-color: #00FA9A;
                }
                QPushButton:pressed {
                    background-color: #06bf78;
                    border-color: #06bf78;
                }
            """)
            delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.order))
            
            right_layout.addWidget(edit_btn)
            right_layout.addWidget(delete_btn)
            right_layout.addStretch()
        
        # Собираем карточку
        main_layout.addWidget(left_frame, 3)  # 3/4 ширины
        main_layout.addWidget(right_frame, 1)  # 1/4 ширины
        
        # Основной layout
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card_frame)
    
    def generate_order_article(self):
        """Генерация артикула заказа на основе товаров в заказе"""
        if not hasattr(self.order, 'order_items') or not self.order.order_items:
            return "Без товаров"
        
        # Собираем артикулы товаров и их количество
        article_parts = []
        for item in self.order.order_items:
            if hasattr(item, 'product') and item.product:
                article = item.product.article or "БЕЗ_АРТИКУЛА"
                quantity = item.quantity or 0
                article_parts.append(f"{article}x{quantity}")
        
        if article_parts:
            return "".join(article_parts)
        else:
            return "Без товаров"