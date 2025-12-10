# views/order_edit_window.py - ДОБАВИМ ВЫБОР АДРЕСА ИЗ БАЗЫ
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QDateTimeEdit, QPushButton, 
                             QMessageBox, QFrame, QGridLayout)
from PySide6.QtCore import Signal, Qt, QDateTime
from PySide6.QtGui import QFont

from order_service import OrderService

class OrderEditWindow(QWidget):
    order_saved = Signal()
    
    def __init__(self, order=None, parent=None):
        super().__init__(parent)
        self.order = order
        self.is_editing = order is not None
        self.pickup_points = []
        
        self.setWindowTitle("Редактирование заказа" if self.is_editing else "Добавление заказа")
        self.setFixedSize(500, 450)
        self.setup_ui()
        self.load_pickup_points()
        self.load_data()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Заголовок
        title = QLabel("Редактирование заказа" if self.is_editing else "Добавление нового заказа")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 16px; 
            font-weight: bold; 
            margin: 5px; 
            color: #2E8B57;
            padding: 5px;
            border-bottom: 2px solid #7FFF00;
        """)
        
        # Форма
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #F8FFF8;
                border: 1px solid #00FA9A;
                border-radius: 8px;
                padding: 5px;
            }
        """)
        
        form_layout = QGridLayout()
        form_layout.setSpacing(12)
        form_layout.setColumnStretch(1, 1)
        
        # Артикул заказа
        form_layout.addWidget(QLabel("Артикул заказа*:"), 0, 0)
        self.article_input = QLineEdit()
        if not self.is_editing:
            self.article_input.setPlaceholderText("ORD-")
        form_layout.addWidget(self.article_input, 0, 1)
        
        # Статус заказа (выпадающий список)
        form_layout.addWidget(QLabel("Статус заказа*:"), 1, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "новый",
            "в обработке", 
            "собран",
            "доставлен",
            "отменен"
        ])
        self.status_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-family: "Times New Roman";
            }
        """)
        form_layout.addWidget(self.status_combo, 1, 1)
        
        # Адрес пункта выдачи (выпадающий список + возможность ввода нового)
        form_layout.addWidget(QLabel("Адрес пункта выдачи:"), 2, 0)
        self.address_combo = QComboBox()
        self.address_combo.setEditable(True)
        self.address_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-family: "Times New Roman";
            }
        """)
        form_layout.addWidget(self.address_combo, 2, 1)
        
        # Дата заказа
        form_layout.addWidget(QLabel("Дата заказа:"), 3, 0)
        self.order_date_input = QDateTimeEdit()
        self.order_date_input.setDateTime(QDateTime.currentDateTime())
        self.order_date_input.setCalendarPopup(True)
        self.order_date_input.setDisplayFormat("dd.MM.yyyy HH:mm")
        form_layout.addWidget(self.order_date_input, 3, 1)
        
        # Дата выдачи (доставки)
        form_layout.addWidget(QLabel("Дата выдачи (доставки):"), 4, 0)
        self.delivery_date_input = QDateTimeEdit()
        self.delivery_date_input.setDateTime(QDateTime.currentDateTime().addDays(3))
        self.delivery_date_input.setCalendarPopup(True)
        self.delivery_date_input.setDisplayFormat("dd.MM.yyyy HH:mm")
        form_layout.addWidget(self.delivery_date_input, 4, 1)
        
        # Код получения (если требуется)
        form_layout.addWidget(QLabel("Код получения:"), 5, 0)
        self.receive_code_input = QLineEdit()
        self.receive_code_input.setPlaceholderText("4-значный код")
        self.receive_code_input.setMaxLength(4)
        form_layout.addWidget(self.receive_code_input, 5, 1)
        
        # Пользователь (для администратора при создании)
        if not self.is_editing:
            form_layout.addWidget(QLabel("ID пользователя:"), 6, 0)
            self.user_id_input = QLineEdit()
            self.user_id_input.setPlaceholderText("ID пользователя")
            self.user_id_input.setText("1")  # По умолчанию
            form_layout.addWidget(self.user_id_input, 6, 1)
        
        form_frame.setLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.save_btn = QPushButton("💾 Сохранить")
        self.cancel_btn = QPushButton("❌ Отмена")
        
        self.save_btn.setMinimumHeight(40)
        self.cancel_btn.setMinimumHeight(40)
        
        # Стиль кнопок
        button_style = """
            QPushButton {
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 6px;
                font-family: "Times New Roman";
                font-size: 14px;
            }
        """
        
        save_style = """
            QPushButton {
                background-color: #2E8B57;
                color: white;
                border: 2px solid #2E8B57;
            }
            QPushButton:hover {
                background-color: #3CB371;
                border-color: #3CB371;
            }
            QPushButton:pressed {
                background-color: #228B22;
                border-color: #228B22;
            }
        """
        
        cancel_style = """
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: 2px solid #6c757d;
            }
            QPushButton:hover {
                background-color: #5a6268;
                border-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
                border-color: #545b62;
            }
        """
        
        self.save_btn.setStyleSheet(button_style + save_style)
        self.cancel_btn.setStyleSheet(button_style + cancel_style)
        
        self.save_btn.clicked.connect(self.save_order)
        self.cancel_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(title)
        layout.addWidget(form_frame)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_pickup_points(self):
        """Загрузка списка пунктов выдачи"""
        try:
            self.pickup_points = OrderService.get_all_pickup_points()
            self.address_combo.clear()
            self.address_combo.addItem("")  # Пустой элемент
            for point in self.pickup_points:
                if point and point.address:
                    self.address_combo.addItem(point.address)
        except Exception as e:
            print(f"❌ Ошибка загрузки пунктов выдачи: {e}")
    
    def load_data(self):
        """Загрузка данных заказа для редактирования"""
        if self.is_editing and self.order:
            # Артикул
            if hasattr(self.order, 'order_article') and self.order.order_article:
                self.article_input.setText(self.order.order_article)
            else:
                self.article_input.setText(f"ORD-{self.order.id}")
            
            # Статус
            if self.order.status:
                index = self.status_combo.findText(self.order.status, Qt.MatchFixedString)
                if index >= 0:
                    self.status_combo.setCurrentIndex(index)
            
            # Адрес
            if self.order.pickup_point and self.order.pickup_point.address:
                address = self.order.pickup_point.address
                index = self.address_combo.findText(address, Qt.MatchFixedString)
                if index >= 0:
                    self.address_combo.setCurrentIndex(index)
                else:
                    self.address_combo.setCurrentText(address)
            
            # Дата заказа
            if self.order.order_date:
                self.order_date_input.setDateTime(QDateTime.fromString(
                    self.order.order_date.strftime("%Y-%m-%d %H:%M:%S"), 
                    "yyyy-MM-dd HH:mm:ss"
                ))
            
            # Дата доставки
            if self.order.delivery_date:
                self.delivery_date_input.setDateTime(QDateTime.fromString(
                    self.order.delivery_date.strftime("%Y-%m-%d %H:%M:%S"), 
                    "yyyy-MM-dd HH:mm:ss"
                ))
            
            # Код получения
            if self.order.receive_code:
                self.receive_code_input.setText(str(self.order.receive_code))
    
    def save_order(self):
        """Сохранение заказа"""
        # Валидация
        if not self.article_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите артикул заказа")
            self.article_input.setFocus()
            return
        
        if not self.status_combo.currentText():
            QMessageBox.warning(self, "Ошибка", "Выберите статус заказа")
            return
        
        # Подготовка данных
        order_data = {
            'order_article': self.article_input.text().strip(),
            'status': self.status_combo.currentText(),
            'order_date': self.order_date_input.dateTime().toPython(),
            'delivery_date': self.delivery_date_input.dateTime().toPython(),
            'receive_code': self.receive_code_input.text().strip() or None
        }
        
        # Адрес пункта выдачи
        address = self.address_combo.currentText().strip()
        if address:
            order_data['pickup_point_address'] = address
        
        try:
            if self.is_editing:
                # Обновление существующего заказа
                result = OrderService.update_order(self.order.id, order_data)
                if result:
                    QMessageBox.information(self, "Успех", "Заказ успешно обновлен")
                    self.order_saved.emit()
                    self.close()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось обновить заказ")
            else:
                # Создание нового заказа
                order_data['user_id'] = int(self.user_id_input.text()) if hasattr(self, 'user_id_input') else 1
                
                result = OrderService.create_order(order_data)
                if result:
                    QMessageBox.information(self, "Успех", "Заказ успешно создан")
                    self.order_saved.emit()
                    self.close()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось создать заказ")
                    
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            print(f"❌ Ошибка при сохранении заказа: {e}")