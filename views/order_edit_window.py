# views/order_edit_window.py - ПОЛНОСТЬЮ ПЕРЕРАБОТАННЫЙ
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QDateTimeEdit, QPushButton, 
                             QMessageBox, QFrame, QGridLayout, QTableWidget,
                             QTableWidgetItem, QHeaderView, QSpinBox, QGroupBox)
from PySide6.QtCore import Signal, Qt, QDateTime
from PySide6.QtGui import QFont, QColor

from order_service import OrderService
from product_service import ProductService

class OrderEditWindow(QWidget):
    order_saved = Signal()
    
    def __init__(self, order=None, parent=None):
        super().__init__(parent)
        self.order = order
        self.is_editing = order is not None
        self.pickup_points = []
        self.selected_products = []  # Список выбранных товаров: [{'product': product, 'quantity': int}]
        
        self.setWindowTitle("Редактирование заказа" if self.is_editing else "Добавление заказа")
        self.setFixedSize(800, 600)
        self.setup_ui()
        self.load_pickup_points()
        self.load_products()
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
            color: #000000;
            padding: 5px;
            border-bottom: 2px solid #7FFF00;
        """)
        
        # Основная форма в два столбца
        form_frame = QFrame()
        form_layout = QHBoxLayout(form_frame)
        form_layout.setSpacing(20)
        
        # Левый столбец - основная информация
        left_column = QFrame()
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(15)
        
        # Группа основной информации
        info_group = QGroupBox("Основная информация")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #7FFF00;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #000000;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #000000;
            }
        """)
        
        info_layout = QGridLayout()
        info_layout.setSpacing(12)
        info_layout.setColumnStretch(1, 1)
        
        # Сгенерированный артикул (автоматически)
        info_layout.addWidget(QLabel("Артикул заказа:"), 0, 0)
        self.article_label = QLabel("")
        self.article_label.setStyleSheet("color: #000000; font-weight: bold; background-color: #f0f0f0; padding: 5px; border-radius: 3px;")
        info_layout.addWidget(self.article_label, 0, 1)
        
        # Статус заказа (выпадающий список)
        info_layout.addWidget(QLabel("Статус заказа*:"), 1, 0)
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
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                background-color: white;
                color: #000000;
                selection-background-color: #7FFF00;
                selection-color: #000000;
            }
        """)
        info_layout.addWidget(self.status_combo, 1, 1)
        
        # Адрес пункта выдачи (выпадающий список + возможность ввода нового)
        info_layout.addWidget(QLabel("Адрес пункта выдачи:"), 2, 0)
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
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                background-color: white;
                color: #000000;
                selection-background-color: #7FFF00;
                selection-color: #000000;
            }
        """)
        info_layout.addWidget(self.address_combo, 2, 1)
        
        # Дата заказа
        info_layout.addWidget(QLabel("Дата заказа:"), 3, 0)
        self.order_date_input = QDateTimeEdit()
        self.order_date_input.setDateTime(QDateTime.currentDateTime())
        self.order_date_input.setCalendarPopup(True)
        self.order_date_input.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.order_date_input.setStyleSheet("""
            QDateTimeEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-family: "Times New Roman";
                font-size: 14px;
            }
        """)
        info_layout.addWidget(self.order_date_input, 3, 1)
        
        # Дата доставки
        info_layout.addWidget(QLabel("Дата доставки:"), 4, 0)
        self.delivery_date_input = QDateTimeEdit()
        self.delivery_date_input.setDateTime(QDateTime.currentDateTime().addDays(3))
        self.delivery_date_input.setCalendarPopup(True)
        self.delivery_date_input.setDisplayFormat("dd.MM.yyyy HH:mm")
        self.delivery_date_input.setStyleSheet("""
            QDateTimeEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-family: "Times New Roman";
                font-size: 14px;
            }
        """)
        info_layout.addWidget(self.delivery_date_input, 4, 1)
        
        # Код получения
        info_layout.addWidget(QLabel("Код получения:"), 5, 0)
        self.receive_code_input = QLineEdit()
        self.receive_code_input.setPlaceholderText("4-значный код")
        self.receive_code_input.setMaxLength(4)
        self.receive_code_input.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-family: "Times New Roman";
                font-size: 14px;
            }
        """)
        info_layout.addWidget(self.receive_code_input, 5, 1)
        
        # Пользователь (для администратора при создании)
        if not self.is_editing:
            info_layout.addWidget(QLabel("ID пользователя:"), 6, 0)
            self.user_id_input = QLineEdit()
            self.user_id_input.setPlaceholderText("ID пользователя")
            self.user_id_input.setText("1")
            self.user_id_input.setStyleSheet("""
                QLineEdit {
                    padding: 6px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    background-color: white;
                    color: #000000;
                    font-family: "Times New Roman";
                    font-size: 14px;
                }
            """)
            info_layout.addWidget(self.user_id_input, 6, 1)
        
        info_group.setLayout(info_layout)
        left_layout.addWidget(info_group)
        left_layout.addStretch()
        
        # Правый столбец - товары в заказе
        right_column = QFrame()
        right_layout = QVBoxLayout(right_column)
        right_layout.setSpacing(15)
        
        # Группа товаров
        products_group = QGroupBox("Товары в заказе")
        products_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #7FFF00;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                color: #000000;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #000000;
            }
        """)
        
        products_layout = QVBoxLayout()
        
        # Таблица выбранных товаров
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels(["Артикул", "Название", "Количество", "Действие"])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.products_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                color: #000000;
                border: 1px solid #ccc;
                font-family: "Times New Roman";
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #7FFF00;
                color: #000000;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #ccc;
            }
            QTableWidget::item {
                padding: 5px;
            }
        """)
        
        # Панель добавления товара
        add_product_frame = QFrame()
        add_product_layout = QHBoxLayout(add_product_frame)
        
        # Выбор товара
        add_product_layout.addWidget(QLabel("Товар:"))
        self.product_combo = QComboBox()
        self.product_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-family: "Times New Roman";
                font-size: 14px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #ccc;
                background-color: white;
                color: #000000;
                selection-background-color: #7FFF00;
                selection-color: #000000;
            }
        """)
        add_product_layout.addWidget(self.product_combo)
        
        # Количество
        add_product_layout.addWidget(QLabel("Количество:"))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(999)
        self.quantity_spin.setValue(1)
        self.quantity_spin.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                color: #000000;
                font-family: "Times New Roman";
                font-size: 14px;
            }
        """)
        add_product_layout.addWidget(self.quantity_spin)
        
        # Кнопка добавления
        add_product_btn = QPushButton("Добавить")
        add_product_btn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: black;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 4px;
                border: 2px solid #7FFF00;
                font-family: "Times New Roman";
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00FA9A;
                border-color: #00FA9A;
            }
        """)
        add_product_btn.clicked.connect(self.add_product_to_order)
        add_product_layout.addWidget(add_product_btn)
        
        add_product_layout.addStretch()
        
        products_layout.addWidget(self.products_table)
        products_layout.addWidget(add_product_frame)
        products_group.setLayout(products_layout)
        
        right_layout.addWidget(products_group)
        right_layout.addStretch()
        
        # Собираем форму
        form_layout.addWidget(left_column, 1)
        form_layout.addWidget(right_column, 1)
        
        # Кнопки
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        
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
                background-color: #7FFF00;
                color: black;
                border: 2px solid #7FFF00;
            }
            QPushButton:hover {
                background-color: #00FA9A;
                border-color: #00FA9A;
            }
            QPushButton:pressed {
                background-color: #228B22;
                border-color: #228B22;
            }
        """
        
        cancel_style = """
            QPushButton {
                background-color: #7FFF00;
                color: black;
                border: 2px solid #7FFF00;
            }
            QPushButton:hover {
                background-color: #00FA9A;
                border-color: #00FA9A;
            }
            QPushButton:pressed {
                background-color: #228B22;
                border-color: #228B22;
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
    
    def load_products(self):
        """Загрузка списка товаров для выбора"""
        try:
            products = ProductService.get_all_products()
            self.product_combo.clear()
            for product in products:
                self.product_combo.addItem(f"{product.article} - {product.name}", product.article)
        except Exception as e:
            print(f"❌ Ошибка загрузки товаров: {e}")
    
    def load_data(self):
        """Загрузка данных заказа для редактирования"""
        if self.is_editing and self.order:
            # Загружаем товары из заказа
            if hasattr(self.order, 'order_items') and self.order.order_items:
                for item in self.order.order_items:
                    product = item.product
                    if product:
                        self.selected_products.append({
                            'product': product,
                            'quantity': item.quantity or 1
                        })
            
            # Обновляем артикул заказа
            self.update_order_article()
            
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
            
            # Обновляем таблицу товаров
            self.update_products_table()
    
    def add_product_to_order(self):
        """Добавление товара в заказ"""
        current_index = self.product_combo.currentIndex()
        if current_index < 0:
            QMessageBox.warning(self, "Ошибка", "Выберите товар")
            return
        
        product_article = self.product_combo.currentData()
        quantity = self.quantity_spin.value()
        
        # Проверяем, не добавлен ли уже этот товар
        for item in self.selected_products:
            if item['product'].article == product_article:
                QMessageBox.warning(self, "Ошибка", "Этот товар уже добавлен в заказ")
                return
        
        # Получаем товар из базы
        product = ProductService.get_product_by_article(product_article)
        if not product:
            QMessageBox.warning(self, "Ошибка", "Товар не найден")
            return
        
        # Добавляем товар
        self.selected_products.append({
            'product': product,
            'quantity': quantity
        })
        
        # Обновляем таблицу и артикул
        self.update_products_table()
        self.update_order_article()
    
    def remove_product_from_order(self, row):
        """Удаление товара из заказа"""
        if 0 <= row < len(self.selected_products):
            self.selected_products.pop(row)
            self.update_products_table()
            self.update_order_article()
    
    def update_products_table(self):
        """Обновление таблицы товаров"""
        self.products_table.setRowCount(len(self.selected_products))
        
        for row, item in enumerate(self.selected_products):
            product = item['product']
            quantity = item['quantity']
            
            # Артикул
            self.products_table.setItem(row, 0, QTableWidgetItem(product.article or ""))
            
            # Название
            self.products_table.setItem(row, 1, QTableWidgetItem(product.name or ""))
            
            # Количество
            quantity_item = QTableWidgetItem(str(quantity))
            self.products_table.setItem(row, 2, quantity_item)
            
            # Кнопка удаления
            remove_btn = QPushButton("Удалить")
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF6347;
                    color: white;
                    font-weight: bold;
                    padding: 3px 8px;
                    border-radius: 3px;
                    border: 1px solid #FF6347;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #FF4500;
                    border-color: #FF4500;
                }
            """)
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_product_from_order(r))
            
            # Помещаем кнопку в ячейку
            self.products_table.setCellWidget(row, 3, remove_btn)
    
    def update_order_article(self):
        """Обновление артикула заказа на основе выбранных товаров"""
        if not self.selected_products:
            self.article_label.setText("Без товаров")
            return
        
        # Формируем артикул по формату: артикулxколичествоАртикулxколичество...
        article_parts = []
        for item in self.selected_products:
            product = item['product']
            quantity = item['quantity']
            article = product.article or "БЕЗ_АРТИКУЛА"
            article_parts.append(f"{article}x{quantity}")
        
        final_article = "".join(article_parts)
        self.article_label.setText(final_article)
    
    def save_order(self):
        """Сохранение заказа"""
        # Валидация
        if not self.status_combo.currentText():
            QMessageBox.warning(self, "Ошибка", "Выберите статус заказа")
            return
        
        # Подготовка данных
        order_data = {
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
                    # Сохраняем товары в заказе
                    self.save_order_items(self.order.id)
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
                    # Сохраняем товары в заказе
                    self.save_order_items(result.id)
                    QMessageBox.information(self, "Успех", "Заказ успешно создан")
                    self.order_saved.emit()
                    self.close()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось создать заказ")
                    
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
            print(f"❌ Ошибка при сохранении заказа: {e}")
    
    def save_order_items(self, order_id):
        """Сохранение товаров в заказе"""
        if not self.selected_products:
            return
        
        items_data = []
        for item in self.selected_products:
            items_data.append({
                'product_article': item['product'].article,
                'quantity': item['quantity']
            })
        
        # Используем метод из order_service для сохранения товаров
        from order_service import OrderService
        OrderService.add_order_items(order_id, items_data)