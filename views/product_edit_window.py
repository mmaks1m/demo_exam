from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox,
                             QTextEdit, QPushButton, QFileDialog, QMessageBox,
                             QFrame, QGridLayout)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

from product_service import ProductService
import os

class ProductEditWindow(QWidget):
    product_saved = Signal()
    
    def __init__(self, product=None, parent=None):
        super().__init__(parent)
        self.product = product
        self.is_editing = product is not None
        self.image_path = None
        
        self.setWindowTitle("Редактирование товара" if self.is_editing else "Добавление товара")
        self.setFixedSize(600, 700)
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Редактирование товара" if self.is_editing else "Добавление нового товара")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        
        # Форма
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setColumnStretch(1, 1)
        
        # Артикул (только для чтения при редактировании)
        form_layout.addWidget(QLabel("Артикул:"), 0, 0)
        self.article_input = QLineEdit()
        if self.is_editing:
            self.article_input.setReadOnly(True)
            self.article_input.setStyleSheet("background-color: #f0f0f0;")
        form_layout.addWidget(self.article_input, 0, 1)
        
        # Название
        form_layout.addWidget(QLabel("Название*:"), 1, 0)
        self.name_input = QLineEdit()
        form_layout.addWidget(self.name_input, 1, 1)
        
        # Категория
        form_layout.addWidget(QLabel("Категория:"), 2, 0)
        self.category_input = QLineEdit()
        form_layout.addWidget(self.category_input, 2, 1)
        
        # Производитель
        form_layout.addWidget(QLabel("Производитель:"), 3, 0)
        self.manufacturer_input = QLineEdit()
        form_layout.addWidget(self.manufacturer_input, 3, 1)
        
        # Поставщик
        form_layout.addWidget(QLabel("Поставщик:"), 4, 0)
        self.supplier_input = QLineEdit()
        form_layout.addWidget(self.supplier_input, 4, 1)
        
        # Цена
        form_layout.addWidget(QLabel("Цена*:"), 5, 0)
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(999999.99)
        self.price_input.setMinimum(0)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(" ₽")
        form_layout.addWidget(self.price_input, 5, 1)
        
        # Количество
        form_layout.addWidget(QLabel("Количество:"), 6, 0)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(999999)
        self.quantity_input.setMinimum(0)
        form_layout.addWidget(self.quantity_input, 6, 1)
        
        # Скидка
        form_layout.addWidget(QLabel("Скидка (%):"), 7, 0)
        self.discount_input = QSpinBox()
        self.discount_input.setMaximum(100)
        self.discount_input.setMinimum(0)
        form_layout.addWidget(self.discount_input, 7, 1)
        
        # Единица измерения
        form_layout.addWidget(QLabel("Единица измерения:"), 8, 0)
        self.unit_input = QLineEdit()
        self.unit_input.setText("шт.")
        form_layout.addWidget(self.unit_input, 8, 1)
        
        # Изображение
        form_layout.addWidget(QLabel("Изображение:"), 9, 0)
        image_layout = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background-color: #f9f9f9;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Нет\nизображения")
        
        self.load_image_btn = QPushButton("Загрузить")
        self.load_image_btn.clicked.connect(self.load_image)
        
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.load_image_btn)
        image_layout.addStretch()
        form_layout.addLayout(image_layout, 9, 1)
        
        # Описание
        form_layout.addWidget(QLabel("Описание:"), 10, 0)
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)
        form_layout.addWidget(self.description_input, 10, 1)
        
        form_frame.setLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        
        self.save_btn.clicked.connect(self.save_product)
        self.cancel_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(title)
        layout.addWidget(form_frame)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_data(self):
        if self.is_editing and self.product:
            self.article_input.setText(self.product.article)
            self.name_input.setText(self.product.name)
            self.category_input.setText(self.product.category or "")
            self.manufacturer_input.setText(self.product.manufacturer or "")
            self.supplier_input.setText(self.product.supplier or "")
            self.price_input.setValue(float(self.product.price) if self.product.price else 0)
            self.quantity_input.setValue(self.product.stock_quantity or 0)
            self.discount_input.setValue(self.product.discount or 0)
            self.unit_input.setText(self.product.unit or "шт.")
            self.description_input.setPlainText(self.product.description or "")
            
            # Загрузка изображения
            if self.product.image_path and os.path.exists(self.product.image_path):
                self.load_image_to_label(self.product.image_path)
    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            self.image_path = file_path
            self.load_image_to_label(file_path)
    
    def load_image_to_label(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")
    
    def save_product(self):
        # Валидация
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Ошибка", "Введите название товара")
            return
        
        if self.price_input.value() <= 0:
            QMessageBox.warning(self, "Ошибка", "Цена должна быть положительной")
            return
        
        # Подготовка данных
        product_data = {
            'article': self.article_input.text().strip(),
            'name': self.name_input.text().strip(),
            'category': self.category_input.text().strip(),
            'manufacturer': self.manufacturer_input.text().strip(),
            'supplier': self.supplier_input.text().strip(),
            'price': self.price_input.value(),
            'stock_quantity': self.quantity_input.value(),
            'discount': self.discount_input.value(),
            'unit': self.unit_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
            'image_path': self.image_path or ''
        }
        
        try:
            if self.is_editing:
                result = ProductService.update_product(self.product.article, product_data)
                if result:
                    QMessageBox.information(self, "Успех", "Товар успешно обновлен")
                    self.product_saved.emit()
                    self.close()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось обновить товар")
            else:
                if not product_data['article']:
                    QMessageBox.warning(self, "Ошибка", "Введите артикул товара")
                    return
                    
                result = ProductService.create_product(product_data)
                if result:
                    QMessageBox.information(self, "Успех", "Товар успешно создан")
                    self.product_saved.emit()
                    self.close()
                else:
                    QMessageBox.critical(self, "Ошибка", "Не удалось создать товар")
                    
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")