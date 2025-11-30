from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QDateTimeEdit, QPushButton, 
                             QMessageBox, QFrame, QGridLayout)
from PySide6.QtCore import Signal, Qt, QDateTime
from PySide6.QtGui import QFont

from order_service import OrderService
from product_service import ProductService

class OrderEditWindow(QWidget):
    order_saved = Signal()
    
    def __init__(self, order=None, parent=None):
        super().__init__(parent)
        self.order = order
        self.is_editing = order is not None
        
        self.setWindowTitle("Редактирование заказа" if self.is_editing else "Добавление заказа")
        self.setFixedSize(500, 400)
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Редактирование заказа" if self.is_editing else "Добавление нового заказа")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px; color: #2E8B57;")
        
        # Форма
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setColumnStretch(1, 1)
        
        # ID заказа (только для чтения при редактировании)
        form_layout.addWidget(QLabel("ID заказа:"), 0, 0)
        self.id_input = QLineEdit()
        if self.is_editing:
            self.id_input.setReadOnly(True)
            self.id_input.setStyleSheet("background-color: #f0f0f0;")
        else:
            self.id_input.setPlaceholderText("Автоматически")
            self.id_input.setReadOnly(True)
            self.id_input.setStyleSheet("background-color: #f0f0f0; color: #666;")
        form_layout.addWidget(self.id_input, 0, 1)
        
        # Артикул заказа
        form_layout.addWidget(QLabel("Артикул заказа:"), 1, 0)
        self.article_input = QLineEdit()
        if not self.is_editing:
            self.article_input.setPlaceholderText("ORD-")
        form_layout.addWidget(self.article_input, 1, 1)
        
        # Статус
        form_layout.addWidget(QLabel("Статус*:"), 2, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "новый",
            "в обработке", 
            "собран",
            "доставлен",
            "отменен"
        ])
        form_layout.addWidget(self.status_combo, 2, 1)
        
        # Дата заказа
        form_layout.addWidget(QLabel("Дата заказа:"), 3, 0)
        self.order_date_input = QDateTimeEdit()
        self.order_date_input.setDateTime(QDateTime.currentDateTime())
        self.order_date_input.setCalendarPopup(True)
        form_layout.addWidget(self.order_date_input, 3, 1)
        
        # Дата доставки
        form_layout.addWidget(QLabel("Дата доставки:"), 4, 0)
        self.delivery_date_input = QDateTimeEdit()
        self.delivery_date_input.setDateTime(QDateTime.currentDateTime().addDays(3))
        self.delivery_date_input.setCalendarPopup(True)
        form_layout.addWidget(self.delivery_date_input, 4, 1)
        
        # Код получения
        form_layout.addWidget(QLabel("Код получения:"), 5, 0)
        self.receive_code_input = QLineEdit()
        self.receive_code_input.setPlaceholderText("4-значный код")
        form_layout.addWidget(self.receive_code_input, 5, 1)
        
        form_frame.setLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        
        self.save_btn.clicked.connect(self.save_order)
        self.cancel_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(title)
        layout.addWidget(form_frame)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_data(self):
        if self.is_editing and self.order:
            self.id_input.setText(str(self.order.id))
            if hasattr(self.order, 'order_article') and self.order.order_article:
                self.article_input.setText(self.order.order_article)
            else:
                self.article_input.setText(f"ORD-{self.order.id}")
            
            if self.order.status:
                index = self.status_combo.findText(self.order.status, Qt.MatchFixedString)
                if index >= 0:
                    self.status_combo.setCurrentIndex(index)
            
            if self.order.order_date:
                self.order_date_input.setDateTime(QDateTime.fromString(
                    self.order.order_date.strftime("%Y-%m-%d %H:%M:%S"), 
                    "yyyy-MM-dd HH:mm:ss"
                ))
            
            if self.order.delivery_date:
                self.delivery_date_input.setDateTime(QDateTime.fromString(
                    self.order.delivery_date.strftime("%Y-%m-%d %H:%M:%S"), 
                    "yyyy-MM-dd HH:mm:ss"
                ))
            
            if self.order.receive_code:
                self.receive_code_input.setText(str(self.order.receive_code))
    
    def save_order(self):
        # Валидация
        if not self.status_combo.currentText():
            QMessageBox.warning(self, "Ошибка", "Выберите статус заказа")
            return
        
        # Подготовка данных
        order_data = {
            'order_article': self.article_input.text().strip() or f"ORD-{self.order.id if self.is_editing else 'NEW'}",
            'status': self.status_combo.currentText(),
            'order_date': self.order_date_input.dateTime().toPython(),
            'delivery_date': self.delivery_date_input.dateTime().toPython(),
            'receive_code': self.receive_code_input.text().strip() or None
        }
        
        try:
            if self.is_editing:
                result = OrderService.update_order(self.order.id, order_data)
                if result:
                    QMessageBox.information(self, "Успех", "Заказ успешно обновлен")
                    self.order_saved.emit()
                    self.close()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось обновить заказ")
            else:
                # Для нового заказа устанавливаем пользователя по умолчанию
                order_data['user_id'] = 1  # Первый пользователь в системе
                order_data['pickup_point_id'] = 1  # Первый пункт выдачи
                
                result = OrderService.create_order(order_data)
                if result:
                    QMessageBox.information(self, "Успех", "Заказ успешно создан")
                    self.order_saved.emit()
                    self.close()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось создать заказ")
                    
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")