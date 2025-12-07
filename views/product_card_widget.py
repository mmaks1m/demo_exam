# views/product_card_widget.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont, QIcon
import os

class ProductCardWidget(QWidget):
    def __init__(self, product, user):
        super().__init__()
        self.product = product
        self.user = user
        self.setup_ui()
        
    def setup_ui(self):
        # Основной контейнер карточки (горизонтальный)
        card_frame = QFrame()
        card_frame.setFrameStyle(QFrame.Box)
        card_frame.setLineWidth(1)
        card_frame.setFixedHeight(230)
        
        # Устанавливаем иконку приложения для карточки
        if os.path.exists("resources/images/icon.png"):
            self.setWindowIcon(QIcon("resources/images/icon.png"))
        
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        
        main_layout = QHBoxLayout(card_frame)
        main_layout.setContentsMargins(10, 8, 10, 8)
        main_layout.setSpacing(15)
        
        # Левая часть: Изображение
        self.setup_image_section(main_layout)
        
        # Центральная часть: Информация
        self.setup_info_section(main_layout)
        
        # Правая часть: Скидка
        self.setup_discount_section(main_layout)
        
        # Основной layout для всего виджета
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card_frame)
        
        # Подсветка согласно ТЗ
        discount = self.product.discount or 0
        if discount > 15:
            card_frame.setStyleSheet("""
                QFrame {
                    background-color: #2E8B57;
                    border: 1px solid white;
                    border-radius: 5px;
                    margin: 5px;
                }
            """)
            
            # Устанавливаем белый цвет для всех label внутри карточки
            for label in card_frame.findChildren(QLabel):
                label.setStyleSheet("""
                    QLabel {
                        color: white;
                        font-family: "Times New Roman";
                        background-color: transparent;
                        border: 1px solid white;
                        border: none;
                    }
                """)
    
    def setup_image_section(self, main_layout):
        """Левая часть: Изображение товара"""
        left_frame = QFrame()
        left_frame.setFixedSize(190, 190)
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        photo_label = QLabel()
        photo_label.setAlignment(Qt.AlignCenter)
        
        # Загрузка изображения товара
        self.load_product_image(photo_label)
        
        left_layout.addWidget(photo_label)
        main_layout.addWidget(left_frame)
    
    def load_product_image(self, photo_label):
        """Загрузка изображения товара"""
        images_dir = "resources/images"
        image_filename = self.product.image_path
        
        if image_filename and os.path.exists(os.path.join(images_dir, image_filename)):
            try:
                image_path = os.path.join(images_dir, image_filename)
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    photo_label.setPixmap(pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                    return
            except Exception as e:
                print(f"Ошибка загрузки изображения {image_filename}: {e}")
        
        # Используем заглушку
        self.show_default_image(photo_label)
    
    def show_default_image(self, photo_label):
        """Показать изображение-заглушку"""
        default_paths = [
            "resources/images/picture.png",
            "picture.png",
            "resources/picture.png"
        ]
        
        for default_path in default_paths:
            if os.path.exists(default_path):
                try:
                    pixmap = QPixmap(default_path)
                    if not pixmap.isNull():
                        photo_label.setPixmap(pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        return
                except Exception:
                    continue
        
        # Если заглушек нет - показываем текст
        photo_label.setText("Нет\nизображения")
        photo_label.setStyleSheet("""
            border: 1px dashed #ccc; 
            color: #666; 
            font-size: 14px;
            font-family: "Times New Roman";
        """)
        photo_label.setAlignment(Qt.AlignCenter)
    
    def setup_info_section(self, main_layout):
        """Центральная часть: Информация о товаре"""
        center_frame = QFrame()
        center_layout = QVBoxLayout(center_frame)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(4)
        
        original_price = float(self.product.price) if self.product.price else 0
        discount = self.product.discount or 0
        final_price = original_price * (1 - discount / 100)
        
        # Категория и название
        category_name_label = QLabel(f"<b>Категория товара:</b> {self.product.category or 'Не указана'} | <b>Название товара:</b> {self.product.name}")
        category_name_label.setFont(QFont("Times New Roman", 11))
        category_name_label.setMinimumHeight(28)
        category_name_label.setMaximumHeight(32)
        category_name_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        # Описание
        description_label = QLabel(f"<b>Описание товара:</b> {self.product.description or 'Нет описания'}")
        description_label.setFont(QFont("Times New Roman", 11))
        description_label.setWordWrap(True)
        description_label.setMaximumHeight(45)
        description_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        # Производитель
        manufacturer_label = QLabel(f"<b>Производитель:</b> {self.product.manufacturer or 'Не указан'}")
        manufacturer_label.setFont(QFont("Times New Roman", 11))
        manufacturer_label.setMinimumHeight(28)
        manufacturer_label.setMaximumHeight(32)
        manufacturer_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        # Поставщик
        supplier_label = QLabel(f"<b>Поставщик:</b> {self.product.supplier or 'Не указан'}")
        supplier_label.setFont(QFont("Times New Roman", 11))
        supplier_label.setMinimumHeight(28)
        supplier_label.setMaximumHeight(32)
        supplier_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        # Цена
        if discount > 0:
            price_label = QLabel(f"<b>Цена:</b> <span style='color: red; text-decoration: line-through;'>{original_price:.2f} ₽</span> → <b>Итоговая цена:</b> {final_price:.2f} ₽")
        else:
            price_label = QLabel(f"<b>Цена:</b> {original_price:.2f} ₽")
        price_label.setFont(QFont("Times New Roman", 11))
        price_label.setMinimumHeight(28)
        price_label.setMaximumHeight(32)
        price_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        # Единица измерения
        unit_label = QLabel(f"<b>Единица измерения:</b> {self.product.unit or 'шт.'}")
        unit_label.setFont(QFont("Times New Roman", 11))
        unit_label.setMinimumHeight(28)
        unit_label.setMaximumHeight(32)
        unit_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        # Количество на складе - ГОЛУБОЙ если 0
        stock_quantity = self.product.stock_quantity or 0
        quantity_text = f"<b>Количество на складе:</b> {stock_quantity}"
        quantity_label = QLabel(quantity_text)
        quantity_label.setFont(QFont("Times New Roman", 11))
        quantity_label.setMinimumHeight(28)
        quantity_label.setMaximumHeight(32)
        
        # Устанавливаем голубой цвет если количество 0
        if stock_quantity == 0:
            quantity_label.setStyleSheet("color: #1E90FF; border: none; background-color: transparent;")  # DodgerBlue
        else:
            quantity_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        # Добавляем все в центральную часть
        center_layout.addWidget(category_name_label)
        center_layout.addWidget(description_label)
        center_layout.addWidget(manufacturer_label)
        center_layout.addWidget(supplier_label)
        center_layout.addWidget(price_label)
        center_layout.addWidget(unit_label)
        center_layout.addWidget(quantity_label)
        
        main_layout.addWidget(center_frame)
    
    def setup_discount_section(self, main_layout):
        """Правая часть: Скидка"""
        right_frame = QFrame()
        right_frame.setFixedSize(110, 190)
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        discount = self.product.discount or 0
        
        discount_label = QLabel(f"<div style='font-size: 32px; font-weight: bold; text-align: center;'>{discount}%</div>")
        discount_label.setAlignment(Qt.AlignCenter)
        discount_label.setMinimumHeight(70)
        discount_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        discount_text_label = QLabel("<div style='text-align: center; font-size: 14px; font-weight: bold;'>Действующая<br>скидка</div>")
        discount_text_label.setAlignment(Qt.AlignCenter)
        discount_text_label.setMinimumHeight(50)
        discount_text_label.setStyleSheet("color: #000000; border: none; background-color: transparent;")
        
        right_layout.addStretch()
        right_layout.addWidget(discount_label)
        right_layout.addWidget(discount_text_label)
        right_layout.addStretch()
        
        main_layout.addWidget(right_frame)