# views/product_list_window.py - ИСПРАВЛЯЕМ РЕГИСТР РОЛЕЙ
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QPushButton, QScrollArea,
                             QFrame, QGridLayout, QMessageBox, QSizePolicy)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QFont, QPalette, QColor

from product_service import ProductService
from views.product_edit_window import ProductEditWindow
from views.product_card_widget import ProductCardWidget

class ProductListWindow(QWidget):
    data_updated = Signal()
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.products = []
        self.current_edit_window = None
        
        # Для отладки
        user_role = user.role if user else None
        user_role_lower = user_role.lower() if user_role else None
        
        print(f"🎯 ProductListWindow создан для: {user.full_name if user else 'Гость'}")
        print(f"   Роль (оригинал): {user_role}")
        print(f"   Роль (нижний регистр): {user_role_lower}")
        
        # Проверяем права
        if user_role_lower in ['менеджер', 'администратор']:
            print("   🛠️ Пользователь имеет права менеджера/администратора")
            self.has_management_rights = True
        else:
            print("   👀 Пользователь не имеет прав управления")
            self.has_management_rights = False
        
        self.setup_ui()
        self.load_products()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # ЗАГОЛОВОК
        title_label = QLabel("КАТАЛОГ ТОВАРОВ")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px; 
                font-weight: bold; 
                color: #2E8B57;
                padding: 10px;
                background-color: #F0FFF0;
                border-radius: 8px;
                border: 2px solid #2E8B57;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # ПАНЕЛЬ УПРАВЛЕНИЯ: только для менеджера и администратора
        if self.has_management_rights:
            print("   🛠️ Создаем панель управления...")
            control_panel = self.create_control_panel()
            layout.addWidget(control_panel)
        else:
            print("   👀 Панель управления не создается")
        
        # Контейнер для товаров
        self.products_container = QWidget()
        self.products_layout = QVBoxLayout(self.products_container)
        self.products_layout.setSpacing(15)
        self.products_layout.setContentsMargins(5, 5, 5, 5)
        
        # Скроллируемая область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.products_container)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        layout.addWidget(scroll_area, 1)
        self.setLayout(layout)
    
    def create_control_panel(self):
        """Создает панель управления для менеджера и администратора"""
        panel = QFrame()
        panel.setObjectName("controlPanel")
        panel.setStyleSheet("""
            QFrame#controlPanel {
                background-color: #F8FFF8;
                border: 2px solid #00FA9A;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setColumnStretch(3, 1)
        
        # === ПОИСК ===
        search_label = QLabel("ПОИСК:")
        search_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        search_label.setStyleSheet("color: #000000;")  # Добавляем черный цвет
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setStyleSheet("""
            QLineEdit#searchInput {
                padding: 8px 12px;
                border: 2px solid #ccc;
                border-radius: 6px;
                background-color: white;
                font-family: "Times New Roman";
                font-size: 14px;
                color: #000000;  /* ЧЕРНЫЙ ТЕКСТ */
            }
            QLineEdit#searchInput:focus {
                border: 2px solid #00FA9A;
                background-color: #F0FFF0;
            }
            QLineEdit#searchInput:hover {
                border: 2px solid #00FA9A;
            }
            QLineEdit#searchInput::placeholder {
                color: #666666;  /* ТЕМНО-СЕРЫЙ ДЛЯ ПЛЕЙСХОЛДЕРА */
            }
        """)
        
        # === ФИЛЬТР ПО ПОСТАВЩИКУ ===
        filter_label = QLabel("ФИЛЬТР:")
        filter_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        filter_label.setStyleSheet("color: #000000;")  # Добавляем черный цвет
        
        self.supplier_filter = QComboBox()
        self.supplier_filter.setObjectName("supplierFilter")
        self.supplier_filter.setMinimumHeight(40)
        self.supplier_filter.setStyleSheet("""
            QComboBox#supplierFilter {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 6px;
                background-color: white;
                font-family: "Times New Roman";
                font-size: 14px;
                color: #000000;  /* ЧЕРНЫЙ ТЕКСТ */
            }
            QComboBox#supplierFilter:hover {
                border: 2px solid #00FA9A;
            }
            QComboBox#supplierFilter:focus {
                border: 2px solid #00FA9A;
            }
            QComboBox#supplierFilter::drop-down {
                border: none;
            }
            QComboBox#supplierFilter QAbstractItemView {
                background-color: white;
                border: 1px solid #ccc;
                color: #000000;  /* ЧЕРНЫЙ ТЕКСТ В ВЫПАДАЮЩЕМ СПИСКЕ */
            }
            QComboBox#supplierFilter QAbstractItemView::item:hover {
                background-color: #00FA9A;
                color: #000000;
            }
            QComboBox#supplierFilter QAbstractItemView::item:selected {
                background-color: #7FFF00;
                color: #000000;
            }
        """)
        
        # === СОРТИРОВКА ===
        sort_label = QLabel("СОРТИРОВКА:")
        sort_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        sort_label.setStyleSheet("color: #000000;")  # Добавляем черный цвет
        
        self.sort_combo = QComboBox()
        self.sort_combo.setObjectName("sortCombo")
        self.sort_combo.setMinimumHeight(40)
        self.sort_combo.addItems([
            "По названию (А-Я)",
            "По названию (Я-А)",
            "По цене (возрастание)",
            "По цене (убывание)",
            "По количеству (возрастание)",
            "По количеству (убывание)"
        ])
        self.sort_combo.setStyleSheet("""
            QComboBox#sortCombo {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 6px;
                background-color: white;
                font-family: "Times New Roman";
                font-size: 14px;
                color: #000000;  /* ЧЕРНЫЙ ТЕКСТ */
            }
            QComboBox#sortCombo:hover {
                border: 2px solid #00FA9A;
            }
            QComboBox#sortCombo:focus {
                border: 2px solid #00FA9A;
            }
            QComboBox#sortCombo::drop-down {
                border: none;
            }
            QComboBox#sortCombo QAbstractItemView {
                background-color: white;
                border: 1px solid #ccc;
                color: #000000;  /* ЧЕРНЫЙ ТЕКСТ В ВЫПАДАЮЩЕМ СПИСКЕ */
            }
            QComboBox#sortCombo QAbstractItemView::item:hover {
                background-color: #00FA9A;
                color: #000000;
            }
            QComboBox#sortCombo QAbstractItemView::item:selected {
                background-color: #7FFF00;
                color: #000000;
            }
        """)
        self.sort_combo.currentTextChanged.connect(self.apply_filters)
        
        # === КНОПКИ ДЛЯ АДМИНИСТРАТОРА ===
        user_role = self.user.role.lower() if self.user else None
        if user_role == 'администратор':
            print("   👑 Добавляем кнопки для администратора")
            
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(10)
            
            self.add_btn = QPushButton("ДОБАВИТЬ ТОВАР")
            self.add_btn.setMinimumHeight(40)
            self.add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #7FFF00;
                    color: black;
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 6px;
                    border: 2px solid #7FFF00;
                    font-family: "Times New Roman";
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #00FA9A;
                    border-color: #00FA9A;
                }
                QPushButton:pressed {
                    background-color: #00FA9A;
                    border-color: #00FA9A;
                }
            """)
            self.add_btn.clicked.connect(self.add_product)
            
            btn_layout.addWidget(self.add_btn)
            btn_layout.addStretch()
        
        # === РАЗМЕЩЕНИЕ ЭЛЕМЕНТОВ ===
        layout.addWidget(search_label, 0, 0)
        layout.addWidget(self.search_input, 0, 1, 1, 3)
        layout.addWidget(filter_label, 1, 0)
        layout.addWidget(self.supplier_filter, 1, 1)
        layout.addWidget(sort_label, 1, 2)
        layout.addWidget(self.sort_combo, 1, 3)
        
        if user_role == 'администратор':
            layout.addLayout(btn_layout, 2, 0, 1, 4)
        
        # Загрузка поставщиков
        self.load_suppliers()
        
        panel.setLayout(layout)
        return panel
    
    def load_suppliers(self):
        """Загрузка списка поставщиков"""
        if self.has_management_rights:
            print("   📦 Загружаем список поставщиков...")
            suppliers = ProductService.get_all_suppliers()
            self.supplier_filter.addItem("Все поставщики")
            for supplier in suppliers:
                if supplier and supplier.strip():
                    self.supplier_filter.addItem(supplier.strip())
            print(f"   ✅ Загружено поставщиков: {len(suppliers)}")
    
    def load_products(self):
        """Загрузка всех товаров (для гостя и клиента)"""
        print("   📥 Загружаем товары...")
        self.products = ProductService.get_all_products()
        print(f"   ✅ Загружено товаров: {len(self.products)}")
        self.display_products()
    
    def apply_filters(self):
        """Применение фильтров в реальном времени"""
        if not self.has_management_rights:
            return
        
        # Получаем значения фильтров
        search_text = self.search_input.text().strip()
        supplier = self.supplier_filter.currentText()
        sort_option = self.sort_combo.currentText()
        
        print(f"   🔍 Применяем фильтры: поиск='{search_text}', поставщик='{supplier}', сортировка='{sort_option}'")
        
        # Преобразуем в параметры для сервиса
        sort_mapping = {
            "По названию (А-Я)": "name_asc",
            "По названию (Я-А)": "name_desc",
            "По цене (возрастание)": "price_asc",
            "По цене (убывание)": "price_desc",
            "По количеству (возрастание)": "stock_quantity_asc",
            "По количеству (убывание)": "stock_quantity_desc"
        }
        
        sort_by = sort_mapping.get(sort_option, "name_asc")
        
        # Применяем фильтры
        self.products = ProductService.get_products_with_filters(
            search_text=search_text,
            supplier_filter=supplier if supplier != "Все поставщики" else "",
            sort_by=sort_by
        )
        
        print(f"   ✅ После фильтрации товаров: {len(self.products)}")
        self.display_products()
    
    def display_products(self):
        """Отображение товаров в виде карточек"""
        print("   🖼️ Отображаем товары...")
        
        # Очищаем контейнер
        for i in reversed(range(self.products_layout.count())): 
            widget = self.products_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        # Добавляем товары
        if not self.products:
            no_products_label = QLabel("ТОВАРЫ НЕ НАЙДЕНЫ")
            no_products_label.setAlignment(Qt.AlignCenter)
            no_products_label.setStyleSheet("""
                QLabel {
                    font-size: 18px; 
                    color: #666666;
                    padding: 40px;
                    font-family: "Times New Roman";
                    font-weight: bold;
                }
            """)
            self.products_layout.addWidget(no_products_label)
            print("   ⚠️ Товары не найдены")
        else:
            for product in self.products:
                card = ProductCardWidget(product, self.user)
                
                # Двойной клик для редактирования (только для администратора)
                user_role = self.user.role.lower() if self.user else None
                if user_role == 'администратор':
                    card.mouseDoubleClickEvent = lambda event, p=product: self.edit_product(p)
                
                self.products_layout.addWidget(card)
            
            print(f"   ✅ Отображено товаров: {len(self.products)}")
        
        self.products_layout.addStretch()
    
    def add_product(self):
        """Добавление нового товара (только администратор)"""
        user_role = self.user.role.lower() if self.user else None
        if user_role == 'администратор':
            print("   🆕 Открываем окно добавления товара")
            
            if self.current_edit_window is not None:
                QMessageBox.warning(self, "Предупреждение", 
                                  "Закройте окно редактирования перед созданием нового товара.")
                return
            
            self.current_edit_window = ProductEditWindow(parent=self)
            self.current_edit_window.product_saved.connect(self.on_product_saved)
            self.current_edit_window.destroyed.connect(lambda: setattr(self, 'current_edit_window', None))
            self.current_edit_window.show()
    
    def edit_product(self, product):
        """Редактирование товара (только администратор)"""
        user_role = self.user.role.lower() if self.user else None
        if user_role == 'администратор':
            print(f"   ✏️ Редактирование товара: {product.name}")
            
            if self.current_edit_window is not None:
                QMessageBox.warning(self, "Предупреждение", 
                                  "Закройте окно редактирования перед открытием нового.")
                return
            
            self.current_edit_window = ProductEditWindow(product, parent=self)
            self.current_edit_window.product_saved.connect(self.on_product_saved)
            self.current_edit_window.destroyed.connect(lambda: setattr(self, 'current_edit_window', None))
            self.current_edit_window.show()
    
    def on_product_saved(self):
        """Обновление списка после сохранения"""
        print("   🔄 Обновляем список после сохранения")
        if self.has_management_rights:
            self.apply_filters()
        else:
            self.load_products()
    
    def keyPressEvent(self, event):
        """Обработка нажатий клавиш"""
        if event.key() == Qt.Key_F5:
            print("   🔄 Обновляем список (F5)")
            if self.has_management_rights:
                self.apply_filters()
            else:
                self.load_products()
        elif event.key() == Qt.Key_Escape:
            user_role = self.user.role.lower() if self.user else None
            if user_role == 'администратор' and self.current_edit_window:
                self.current_edit_window.close()