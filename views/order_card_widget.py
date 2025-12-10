# views/order_card_widget.py - ИСПРАВЛЕННЫЙ
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
        card_frame.setFixedHeight(180)
        
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 2px solid #7FFF00;
                border-radius: 8px;
                margin: 8px;
            }
        """)
        
        main_layout = QHBoxLayout(card_frame)
        main_layout.setContentsMargins(15, 12, 15, 12)
        main_layout.setSpacing(20)
        
        # Левая часть (2/3 ширины) - информация о заказе
        left_frame = QFrame()
        left_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        left_layout = QVBoxLayout(left_frame)
        left_layout.setSpacing(8)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Артикул заказа - БЕЗОПАСНАЯ ПРОВЕРКА
        article = "Не указан"
        if hasattr(self.order, 'order_article') and self.order.order_article:
            article = self.order.order_article
        elif hasattr(self.order, 'id'):
            article = f"ORD-{self.order.id}"
        
        article_label = QLabel(f"<b>Артикул заказа:</b> {article}")
        article_label.setFont(QFont("Times New Roman", 12, QFont.Bold))
        article_label.setStyleSheet("color: #000000;")
        
        # Статус заказа (с подсветкой) - БЕЗОПАСНАЯ ПРОВЕРКА
        status = getattr(self.order, 'status', 'не указан')
        status_label = QLabel(f"<b>Статус заказа:</b> {status}")
        status_label.setFont(QFont("Times New Roman", 12))
        
        # Подсветка статуса цветом
        status_lower = str(status).lower()
        if status_lower in ['выполнен', 'доставлен']:
            status_label.setStyleSheet("color: #28a745; font-weight: bold;")
        elif status_lower in ['отменен', 'отменён']:
            status_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        elif status_lower in ['в обработке', 'обработка']:
            status_label.setStyleSheet("color: #ffc107; font-weight: bold;")
        else:
            status_label.setStyleSheet("color: #000000;")
        
        # Адрес пункта выдачи - БЕЗОПАСНАЯ ПРОВЕРКА
        address = "Не указан"
        if hasattr(self.order, 'pickup_point') and self.order.pickup_point:
            address = self.order.pickup_point.address
        
        address_label = QLabel(f"<b>Адрес пункта выдачи:</b> {address}")
        address_label.setFont(QFont("Times New Roman", 12))
        address_label.setStyleSheet("color: #000000;")
        address_label.setWordWrap(True)
        
        # Дата заказа - БЕЗОПАСНАЯ ПРОВЕРКА
        date_str = "Не указана"
        if hasattr(self.order, 'order_date') and self.order.order_date:
            try:
                date_str = self.order.order_date.strftime("%d.%m.%Y %H:%M")
            except:
                date_str = "Ошибка формата"
        
        date_label = QLabel(f"<b>Дата заказа:</b> {date_str}")
        date_label.setFont(QFont("Times New Roman", 12))
        date_label.setStyleSheet("color: #000000;")
        
        # Пользователь (если есть права администратора/менеджера)
        if self.user and self.user.role.lower() in ['администратор', 'менеджер']:
            user_name = "Неизвестно"
            if hasattr(self.order, 'user') and self.order.user:
                user_name = self.order.user.full_name
            
            user_label = QLabel(f"<b>Пользователь:</b> {user_name}")
            user_label.setFont(QFont("Times New Roman", 12))
            user_label.setStyleSheet("color: #666666;")
            left_layout.addWidget(user_label)
        
        left_layout.addWidget(article_label)
        left_layout.addWidget(status_label)
        left_layout.addWidget(address_label)
        left_layout.addWidget(date_label)
        left_layout.addStretch()
        
        # Правая часть (1/3 ширины) - дата доставки и кнопки
        right_frame = QFrame()
        right_frame.setFixedWidth(220)
        right_layout = QVBoxLayout(right_frame)
        right_layout.setSpacing(15)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # Дата доставки - БЕЗОПАСНАЯ ПРОВЕРКА
        delivery_date_str = "Не указана"
        if hasattr(self.order, 'delivery_date') and self.order.delivery_date:
            try:
                delivery_date_str = self.order.delivery_date.strftime("%d.%m.%Y")
            except:
                delivery_date_str = "Ошибка формата"
        
        delivery_label = QLabel(f"<div style='text-align: center; font-size: 16px; font-weight: bold;'>Дата доставки:</div>")
        delivery_date = QLabel(f"<div style='text-align: center; font-size: 24px; font-weight: bold; color: #2E8B57;'>{delivery_date_str}</div>")
        
        delivery_label.setAlignment(Qt.AlignCenter)
        delivery_date.setAlignment(Qt.AlignCenter)
        
        # Кнопки для администратора
        if self.user and self.user.role.lower() == 'администратор':
            btn_layout = QVBoxLayout()
            btn_layout.setSpacing(8)
            
            edit_btn = QPushButton("✏️ Редактировать")
            edit_btn.setMinimumHeight(35)
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    font-weight: bold;
                    border: 2px solid #007bff;
                    border-radius: 4px;
                    font-family: "Times New Roman";
                }
                QPushButton:hover {
                    background-color: #0056b3;
                    border-color: #0056b3;
                }
            """)
            edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.order))
            
            delete_btn = QPushButton("🗑️ Удалить")
            delete_btn.setMinimumHeight(35)
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #dc3545;
                    color: white;
                    font-weight: bold;
                    border: 2px solid #dc3545;
                    border-radius: 4px;
                    font-family: "Times New Roman";
                }
                QPushButton:hover {
                    background-color: #c82333;
                    border-color: #c82333;
                }
            """)
            delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.order))
            
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.addStretch()
        
        right_layout.addWidget(delivery_label)
        right_layout.addWidget(delivery_date)
        
        if self.user and self.user.role.lower() == 'администратор':
            right_layout.addLayout(btn_layout)
        else:
            right_layout.addStretch()
        
        # Собираем карточку
        main_layout.addWidget(left_frame, 2)  # 2/3 ширины
        main_layout.addWidget(right_frame, 1)  # 1/3 ширины
        
        # Основной layout
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card_frame)