# views/product_edit_window.py - ИСПРАВЛЯЕМ ЦВЕТ ТЕКСТА
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QDoubleSpinBox, QSpinBox,
                             QTextEdit, QPushButton, QFileDialog, QMessageBox,
                             QFrame, QGridLayout, QGroupBox)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QIcon
import os

from product_service import ProductService

class ProductEditWindow(QWidget):
    product_saved = Signal()
    
    def __init__(self, product=None, parent=None):
        super().__init__(parent)
        self.product = product
        self.is_editing = product is not None
        self.image_path = None
        
        # Устанавливаем иконку
        if os.path.exists("resources/images/icon.png"):
            self.setWindowIcon(QIcon("resources/images/icon.png"))
        
        self.setWindowTitle("Редактирование товара" if self.is_editing else "Добавление товара")
        self.setFixedSize(700, 750)
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title = QLabel("Редактирование товара" if self.is_editing else "Добавление нового товара")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px; color: #000000;")
        
        # Основная форма
        form_group = QGroupBox("Информация о товаре")
        form_group.setStyleSheet("""
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
        
        form_layout = QGridLayout()
        form_layout.setSpacing(15)
        form_layout.setColumnStretch(1, 1)
        
        # Артикул
        form_layout.addWidget(QLabel("Артикул*:"), 0, 0)
        self.article_input = QLineEdit()
        if self.is_editing:
            self.article_input.setReadOnly(True)
            self.article_input.setStyleSheet("background-color: #f0f0f0; color: #000000;")
        else:
            self.article_input.setStyleSheet("color: #000000;")
        form_layout.addWidget(self.article_input, 0, 1)
        
        # Название
        form_layout.addWidget(QLabel("Название*:"), 1, 0)
        self.name_input = QLineEdit()
        self.name_input.setStyleSheet("color: #000000;")
        form_layout.addWidget(self.name_input, 1, 1)
        
        # Категория (выпадающий список)
        form_layout.addWidget(QLabel("Категория*:"), 2, 0)
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems([
            "Кроссовки", "Туфли", "Ботинки", "Сапоги", "Тапочки", 
            "Сандалии", "Мокасины", "Босоножки", "Слипоны"
        ])
        self.category_input.setStyleSheet("""
            QComboBox {
                color: #000000;
                background-color: white;
            }
            QComboBox QAbstractItemView {
                color: #000000;
                background-color: white;
                selection-background-color: #7FFF00;
                selection-color: #000000;
            }
        """)
        form_layout.addWidget(self.category_input, 2, 1)

        # Производитель (выпадающий список)
        form_layout.addWidget(QLabel("Производитель*:"), 3, 0)
        self.manufacturer_input = QComboBox()
        self.manufacturer_input.setEditable(True)
        self.manufacturer_input.addItems([
            "Nike", "Adidas", "Reebok", "Puma", "New Balance",
            "Geox", "Ecco", "Clarks", "Salomon", "Timberland"
        ])
        self.manufacturer_input.setStyleSheet("""
            QComboBox {
                color: #000000;
                background-color: white;
            }
            QComboBox QAbstractItemView {
                color: #000000;
                background-color: white;
                selection-background-color: #7FFF00;
                selection-color: #000000;
            }
        """)
        form_layout.addWidget(self.manufacturer_input, 3, 1)
        
        # Поставщик
        form_layout.addWidget(QLabel("Поставщик:"), 4, 0)
        self.supplier_input = QLineEdit()
        self.supplier_input.setStyleSheet("color: #000000;")
        form_layout.addWidget(self.supplier_input, 4, 1)
        
        # Цена
        form_layout.addWidget(QLabel("Цена*:"), 5, 0)
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(999999.99)
        self.price_input.setMinimum(0)
        self.price_input.setDecimals(2)
        self.price_input.setSuffix(" ₽")
        self.price_input.setStyleSheet("color: #000000;")
        form_layout.addWidget(self.price_input, 5, 1)
        
        # Количество
        form_layout.addWidget(QLabel("Количество:"), 6, 0)
        self.quantity_input = QSpinBox()
        self.quantity_input.setMaximum(999999)
        self.quantity_input.setMinimum(0)
        self.quantity_input.setStyleSheet("color: #000000;")
        form_layout.addWidget(self.quantity_input, 6, 1)
        
        # Скидка
        form_layout.addWidget(QLabel("Скидка (%):"), 7, 0)
        self.discount_input = QSpinBox()
        self.discount_input.setMaximum(100)
        self.discount_input.setMinimum(0)
        self.discount_input.setStyleSheet("color: #000000;")
        form_layout.addWidget(self.discount_input, 7, 1)
        
        # Единица измерения
        form_layout.addWidget(QLabel("Единица измерения:"), 8, 0)
        self.unit_input = QLineEdit()
        self.unit_input.setText("шт.")
        self.unit_input.setStyleSheet("color: #000000;")
        form_layout.addWidget(self.unit_input, 8, 1)
        
        # Изображение
        form_layout.addWidget(QLabel("Изображение:"), 9, 0)
        image_layout = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setFixedSize(150, 150)
        self.image_label.setStyleSheet("border: 2px solid #cccccc; background-color: #f9f9f9; color: #000000;")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("Нет\nизображения")
        
        self.load_image_btn = QPushButton("Загрузить")
        self.load_image_btn.setStyleSheet("background-color: #7FFF00; color: #000000;")
        self.load_image_btn.clicked.connect(self.load_image)
        
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.load_image_btn)
        image_layout.addStretch()
        form_layout.addLayout(image_layout, 9, 1)
        
        # Описание
        form_layout.addWidget(QLabel("Описание:"), 10, 0)
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)
        self.description_input.setStyleSheet("color: #000000;")
        form_layout.addWidget(self.description_input, 10, 1)
        
        form_group.setLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.cancel_btn = QPushButton("Отмена")
        
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: #000000;
                font-weight: bold;
                padding: 10px 25px;
                border-radius: 5px;
                border: 2px solid #7FFF00;
                font-family: "Times New Roman";
            }
            QPushButton:hover {
                background-color: #00FA9A;
                border-color: #00FA9A;
            }
        """)
        
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: #000000;
                font-weight: bold;
                padding: 10px 25px;
                border-radius: 5px;
                border: 2px solid #7FFF00;
                font-family: "Times New Roman";
            }
            QPushButton:hover {
                background-color: #00FA9A;
                border-color: #00FA9A;
            }
        """)
        
        self.save_btn.clicked.connect(self.save_product)
        self.cancel_btn.clicked.connect(self.close)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(title)
        layout.addWidget(form_group)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_data(self):
        if self.is_editing and self.product:
            self.article_input.setText(self.product.article or "")
            self.name_input.setText(self.product.name or "")
            # Используем setCurrentText для QComboBox
            if self.product.category:
                index = self.category_input.findText(self.product.category)
                if index >= 0:
                    self.category_input.setCurrentIndex(index)
                else:
                    self.category_input.setCurrentText(self.product.category)
            
            if self.product.manufacturer:
                index = self.manufacturer_input.findText(self.product.manufacturer)
                if index >= 0:
                    self.manufacturer_input.setCurrentIndex(index)
                else:
                    self.manufacturer_input.setCurrentText(self.product.manufacturer)
            
            self.supplier_input.setText(self.product.supplier or "")
            self.price_input.setValue(float(self.product.price) if self.product.price else 0)
            self.quantity_input.setValue(self.product.stock_quantity or 0)
            self.discount_input.setValue(self.product.discount or 0)
            self.unit_input.setText(self.product.unit or "шт.")
            self.description_input.setPlainText(self.product.description or "")
            
            # Загрузка изображения
            if self.product.image_path:
                image_path = f"resources/images/{self.product.image_path}"
                if os.path.exists(image_path):
                    self.load_image_to_label(image_path)
    
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
            scaled_pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
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
            'category': self.category_input.currentText().strip(),
            'manufacturer': self.manufacturer_input.currentText().strip(),
            'supplier': self.supplier_input.text().strip(),
            'price': self.price_input.value(),
            'stock_quantity': self.quantity_input.value(),
            'discount': self.discount_input.value(),
            'unit': self.unit_input.text().strip(),
            'description': self.description_input.toPlainText().strip(),
        }
        
        # Обработка изображения
        if self.image_path:
            import shutil
            try:
                if self.is_editing:
                    image_name = f"{self.product.article}.png"
                else:
                    image_name = f"{product_data['article']}.png"
                
                dest_path = f"resources/images/{image_name}"
                shutil.copy2(self.image_path, dest_path)
                product_data['image_path'] = image_name
            except Exception as e:
                print(f"Ошибка копирования изображения: {e}")
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить изображение")
        
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