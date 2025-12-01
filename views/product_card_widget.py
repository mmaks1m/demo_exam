# views/product_card_widget.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QFrame, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont
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
        card_frame.setFixedHeight(230)  # Увеличиваем общую высоту карточки
        card_frame.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin: 5px;
            }
        """)
        
        main_layout = QHBoxLayout(card_frame)
        main_layout.setContentsMargins(10, 8, 10, 8)  # Увеличиваем вертикальные отступы
        main_layout.setSpacing(15)
        
        # Левая часть: Изображение (квадрат)
        left_frame = QFrame()
        left_frame.setFixedSize(190, 190)  # Увеличиваем размер блока с изображением
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        photo_label = QLabel()
        photo_label.setAlignment(Qt.AlignCenter)
        
        self.load_product_image(photo_label)
        left_layout.addWidget(photo_label)
        
        # Центральная часть: Информация о товаре
        center_frame = QFrame()
        center_layout = QVBoxLayout(center_frame)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(4)  # Уменьшаем расстояние между строками, чтобы уместить больше
        
        # Получаем данные
        original_price = float(self.product.price) if self.product.price else 0
        discount = self.product.discount or 0
        final_price = original_price * (1 - discount / 100)
        
        # Увеличиваем высоту строк и размер шрифта
        def create_info_label(text, font_size=12, is_bold=False):
            label = QLabel(text)
            font = QFont("Times New Roman", font_size)
            if is_bold:
                font.setBold(True)
            label.setFont(font)
            label.setMinimumHeight(28)  # Увеличиваем высоту строки
            label.setMaximumHeight(32)  # Увеличиваем максимальную высоту
            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            label.setStyleSheet("""
                QLabel {
                    border: none;
                    color: #000000;
                    font-family: "Times New Roman";
                    background-color: transparent;
                }
            """)
            return label
        
        # Создаем строки с увеличенным текстом
        category_name_label = create_info_label(f"<b>Категория товара:</b> {self.product.category or 'Не указана'} | <b>Название товара:</b> {self.product.name}", 11, True)
        
        description_label = create_info_label(f"<b>Описание товара:</b> {self.product.description or 'Нет описания'}", 11)
        description_label.setWordWrap(True)
        description_label.setMaximumHeight(45)
        
        manufacturer_label = create_info_label(f"<b>Производитель:</b> {self.product.manufacturer or 'Не указан'}", 11)
        
        supplier_label = create_info_label(f"<b>Поставщик:</b> {self.product.supplier or 'Не указан'}", 11)
        
        if discount > 0:
            price_label = create_info_label(f"<b>Цена:</b> <span style='color: red; text-decoration: line-through;'>{original_price:.2f} ₽</span> → <b>Итоговая цена:</b> {final_price:.2f} ₽", 11)
        else:
            price_label = create_info_label(f"<b>Цена:</b> {original_price:.2f} ₽", 11)
        
        unit_label = create_info_label(f"<b>Единица измерения:</b> {self.product.unit or 'шт.'}", 11)
        
        quantity_label = create_info_label(f"<b>Количество на складе:</b> {self.product.stock_quantity or 0}", 11)
        
        # Добавляем все в центральную часть
        center_layout.addWidget(category_name_label)
        center_layout.addWidget(description_label)
        center_layout.addWidget(manufacturer_label)
        center_layout.addWidget(supplier_label)
        center_layout.addWidget(price_label)
        center_layout.addWidget(unit_label)
        center_layout.addWidget(quantity_label)
        
        # Правая часть: Скидка
        right_frame = QFrame()
        right_frame.setFixedSize(110, 190)  # Увеличиваем ширину блока скидки
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        discount_label = QLabel(f"<div style='font-size: 32px; font-weight: bold; text-align: center;'>{discount}%</div>")
        discount_label.setAlignment(Qt.AlignCenter)
        discount_label.setMinimumHeight(70)  # Увеличиваем высоту блока скидки
        discount_label.setStyleSheet("""
            QLabel {
                border: none;
                color: #000000;
                font-family: "Times New Roman";
                background-color: transparent;
            }
        """)
        
        discount_text_label = QLabel("<div style='text-align: center; font-size: 14px; font-weight: bold;'>Действующая<br>скидка</div>")
        discount_text_label.setAlignment(Qt.AlignCenter)
        discount_text_label.setMinimumHeight(50)
        discount_text_label.setStyleSheet("""
            QLabel {
                border: none;
                color: #000000;
                font-family: "Times New Roman";
                background-color: transparent;
            }
        """)
        
        right_layout.addStretch()
        right_layout.addWidget(discount_label)
        right_layout.addWidget(discount_text_label)
        right_layout.addStretch()
        
        # Собираем все вместе
        main_layout.addWidget(left_frame)
        main_layout.addWidget(center_frame)
        main_layout.addWidget(right_frame)
        
        # Основной layout для всего виджета
        outer_layout = QVBoxLayout(self)
        outer_layout.addWidget(card_frame)
        
        # Подсветка согласно ТЗ (только если скидка > 15%)
        if discount > 15:
            # Для зеленого фона устанавливаем контрастные цвета
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
                        border: none;
                        color: white;
                        font-family: "Times New Roman";
                        background-color: transparent;
                    }
                """)
            
            # Для цены со скидкой на зеленом фоне - светлый красный вместо обычного
            if discount > 0:
                price_label.setText(f"<b>Цена:</b> <span style='color: #FFCCCB; text-decoration: line-through;'>{original_price:.2f} ₽</span> → <b>Итоговая цена:</b> {final_price:.2f} ₽")
                
                # Обновляем стиль для ценового label отдельно
                price_label.setStyleSheet("""
                    QLabel {
                        border: none;
                        color: white;
                        font-family: "Times New Roman";
                        background-color: transparent;
                    }
                """)
    
    def load_product_image(self, photo_label):
        # Путь к папке с изображениями
        images_dir = "resources/images"
        
        # Проверяем, существует ли папка
        if not os.path.exists(images_dir):
            print(f"⚠️  Папка {images_dir} не существует!")
            self.show_default_image(photo_label)
            return
        
        # Получаем имя файла из базы данных
        image_filename = self.product.image_path
        
        if image_filename and image_filename != "picture.png":
            # Пробуем загрузить конкретное изображение товара
            image_path = os.path.join(images_dir, image_filename)
            
            if os.path.exists(image_path):
                try:
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        photo_label.setPixmap(pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        return
                    else:
                        print(f"⚠️  Не удалось загрузить изображение: {image_path}")
                except Exception as e:
                    print(f"❌ Ошибка загрузки изображения {image_path}: {e}")
            else:
                print(f"⚠️  Изображение не найдено: {image_path}")
        
        # Если не нашли конкретное изображение или оно picture.png, показываем заглушку
        self.show_default_image(photo_label)
    
    def show_default_image(self, photo_label):
        """Показать изображение-заглушку"""
        # Пути к возможным заглушкам
        possible_defaults = [
            "resources/images/picture.png",
            "picture.png",
            "resources/picture.png"
        ]
        
        for default_path in possible_defaults:
            if os.path.exists(default_path):
                try:
                    pixmap = QPixmap(default_path)
                    if not pixmap.isNull():
                        photo_label.setPixmap(pixmap.scaled(180, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                        return
                except Exception as e:
                    print(f"❌ Ошибка загрузки заглушки {default_path}: {e}")
        
        # Если заглушек нет - показываем текст
        photo_label.setText("Нет\nизображения")
        photo_label.setStyleSheet("""
            border: 1px dashed #ccc; 
            color: #666; 
            font-size: 14px;
            font-family: "Times New Roman";
        """)
        photo_label.setAlignment(Qt.AlignCenter)
        print("⚠️  Заглушка не найдена, показан текст")