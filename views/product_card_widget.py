# views/product_card_widget.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os

class ProductCardWidget(QWidget):
    def __init__(self, product, user):
        super().__init__()
        self.product = product
        self.user = user
        self.setup_ui()
        
    def setup_ui(self):
        # Основной контейнер карточки
        card_frame = QFrame()
        card_frame.setFrameStyle(QFrame.Box)
        card_frame.setLineWidth(1)
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
                font-family: "Times New Roman";
            }
            QLabel {
                font-family: "Times New Roman";
                background-color: transparent;
            }
        """)
        
        layout = QVBoxLayout(card_frame)
        layout.setSpacing(8)
        
        # Фото товара
        photo_label = QLabel()
        photo_label.setAlignment(Qt.AlignCenter)
        photo_label.setFixedSize(100, 100)
        
        # Проверяем наличие изображения
        image_loaded = False
        if self.product.image_path and os.path.exists(self.product.image_path):
            try:
                pixmap = QPixmap(self.product.image_path)
                if not pixmap.isNull():
                    photo_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    image_loaded = True
            except:
                image_loaded = False
        
        if not image_loaded:
            # Пробуем заглушку
            try:
                if os.path.exists("resources/images/picture.png"):
                    pixmap = QPixmap("resources/images/picture.png")
                    photo_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                else:
                    photo_label.setText("Нет изображения")
                    photo_label.setStyleSheet("border: 1px dashed #ccc; color: #666;")
            except:
                photo_label.setText("Нет изображения")
                photo_label.setStyleSheet("border: 1px dashed #ccc; color: #666;")
        
        # Категория и наименование
        category_label = QLabel(f"<b>Категория товара:</b> {self.product.category or 'Не указана'}")
        name_label = QLabel(f"<b>Наименование товара:</b> {self.product.name}")
        
        # Описание
        description_label = QLabel(f"<b>Описание товара:</b><br>{self.product.description or 'Нет описания'}")
        description_label.setWordWrap(True)
        description_label.setMaximumHeight(60)
        
        # Производитель
        manufacturer_label = QLabel(f"<b>Производитель:</b> {self.product.manufacturer or 'Не указан'}")
        
        # Поставщик
        supplier_label = QLabel(f"<b>Поставщик:</b> {self.product.supplier or 'Не указан'}")
        
        # Цена с учетом скидки
        original_price = float(self.product.price) if self.product.price else 0
        discount = self.product.discount or 0
        final_price = original_price * (1 - discount / 100)
        
        if discount > 0:
            # Цена со скидкой - перечеркнутая красная
            price_label = QLabel(f"<b>Цена:</b> <span style='color: red; text-decoration: line-through;'>{original_price:.2f} ₽</span> <b>Итоговая цена:</b> {final_price:.2f} ₽")
        else:
            # Обычная цена
            price_label = QLabel(f"<b>Цена:</b> {original_price:.2f} ₽")
        
        # Единица измерения и количество
        unit_label = QLabel(f"<b>Единица измерения:</b> {self.product.unit or 'шт.'}")
        quantity_label = QLabel(f"<b>Количество на складе:</b> {self.product.stock_quantity or 0}")
        
        # Скидка
        discount_label = QLabel(f"<b>Действующая скидка:</b> {discount}%")
        
        # Собираем все вместе
        layout.addWidget(photo_label)
        layout.addWidget(category_label)
        layout.addWidget(name_label)
        layout.addWidget(description_label)
        layout.addWidget(manufacturer_label)
        layout.addWidget(supplier_label)
        layout.addWidget(price_label)
        layout.addWidget(unit_label)
        layout.addWidget(quantity_label)
        layout.addWidget(discount_label)
        
        # Подсветка согласно ТЗ
        if discount > 15:
            card_frame.setStyleSheet("""
                QFrame {
                    background-color: #2E8B57;
                    color: white;
                    border: 1px solid #2E8B57;
                    border-radius: 5px;
                    padding: 10px;
                    font-family: "Times New Roman";
                }
                QLabel {
                    background-color: transparent;
                    color: white;
                    font-family: "Times New Roman";
                }
            """)
        elif (self.product.stock_quantity or 0) == 0:
            card_frame.setStyleSheet("""
                QFrame {
                    background-color: lightblue;
                    border: 1px solid lightblue;
                    border-radius: 5px;
                    padding: 10px;
                    font-family: "Times New Roman";
                }
                QLabel {
                    background-color: transparent;
                    font-family: "Times New Roman";
                }
            """)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(card_frame)