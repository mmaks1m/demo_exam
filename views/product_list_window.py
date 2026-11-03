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
        if self.has_management_rights:
            self.search_input.textChanged.connect(self.apply_filters)
            self.supplier_filter.currentTextChanged.connect(self.apply_filters)
            self.sort_combo.currentTextChanged.connect(self.apply_filters)
    
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
                color: black;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #7FFF00;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # ПАНЕЛЬ УПРАВЛЕНИЯ: только для менеджера и администратора
        if self.has_management_rights:
            print("   🛠️ Создаем панель управления...")
            control_panel = self.create_control_panel()
            layout.addWidget(control_panel)
            self.check_signals()
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
        panel = QFrame()
        panel.setObjectName("controlPanel")
        panel.setStyleSheet("""
            QFrame#controlPanel {
                background-color: #F8FFF8;
                border: 2px solid #7FFF00;
                border-radius: 8px;
                padding: 15px;
                height: 80px
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(15)
        layout.setColumnStretch(3, 1)
        
        search_label = QLabel("ПОИСК:")
        search_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        search_label.setStyleSheet("color: #000000;")
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Введите текст для поиска...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setClearButtonEnabled(True)
        
        filter_label = QLabel("ФИЛЬТР:")
        filter_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        filter_label.setStyleSheet("color: #000000;")
        
        self.supplier_filter = QComboBox()
        self.supplier_filter.setObjectName("supplierFilter")
        self.supplier_filter.setMinimumHeight(40)
        
        sort_label = QLabel("СОРТИРОВКА:")
        sort_label.setFont(QFont("Times New Roman", 10, QFont.Bold))
        sort_label.setStyleSheet("color: #000000;")
        
        self.sort_combo = QComboBox()
        self.sort_combo.setObjectName("sortCombo")
        self.sort_combo.setMinimumHeight(40)
        self.sort_combo.addItems([
            "По названию (А-Я)",
            "По названию (Я-А)",
            "По цена (возрастание)",
            "По цена (убывание)",
            "По количеству (возрастание)",
            "По количеству (убывание)"
        ])
        
        combo_box_style = """
            QComboBox {
                padding: 8px;
                border: 2px solid #ccc;
                border-radius: 6px;
                background-color: white;
                font-family: "Times New Roman";
                font-size: 14px;
                color: #000000;  /* ЧЕРНЫЙ ТЕКСТ В ОСНОВНОМ ПОЛЕ */
            }
            QComboBox:hover {
                border: 2px solid #00FA9A;
                background-color: white;
            }
            QComboBox:focus {
                border: 2px solid #00FA9A;
                background-color: white;
            }
            /* Стиль для стрелки */
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(none);
                border-left: 1px solid #ccc;
                padding-left: 5px;
            }
            /* Стиль для выпадающего списка */
            QComboBox QAbstractItemView {
                border: none;
                border-radius: 6px;
                background-color: white;
                selection-background-color: #00FA9A;
                selection-color: #000000;
                padding: 5px;
                font-family: "Times New Roman";
                font-size: 14px;
                outline: none;
            }
            /* Стиль для элементов в выпадающем списке */
            QComboBox QAbstractItemView::item {
                padding: 8px;
                color: #000000;  /* ЧЕРНЫЙ ТЕКСТ В ВЫПАДАЮЩЕМ СПИСКЕ */
                border-radius: 3px;
                outline: none;
                border: none;
                margin: 2px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #00FA9A;
                outline: none;
                border: none;
                color: #000000;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #00FA9A; 
                outline: none;
                border: none;
                color: #000000;
            }
        """
        
        line_edit_style = """
            QLineEdit {
                padding: 8px 12px;
                border: 2px solid #ccc;
                border-radius: 6px;
                background-color: white;
                font-family: "Times New Roman";
                font-size: 14px;
                color: #000000;
            }
            QLineEdit:focus {
                border: 2px solid #00FA9A;
                background-color: #F0FFF0;
            }
            QLineEdit:hover {
                border: 2px solid #00FA9A;
            }
            QLineEdit::placeholder {
                color: #666666;
            }
        """
        
        self.search_input.setStyleSheet(line_edit_style)
        self.supplier_filter.setStyleSheet(combo_box_style)
        self.sort_combo.setStyleSheet(combo_box_style)
        
        
        user_role = self.user.role.lower() if self.user else None
        if user_role == 'администратор':
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
            
            self.test_btn = QPushButton("Запустить тестирование")
            self.test_btn.setMinimumHeight(40)
            self.test_btn.setToolTip("Запуск автоматического тестирования функции добавления товара")
            self.test_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FFA500;
                    color: black;
                    font-weight: bold;
                    padding: 10px 20px;
                    border-radius: 6px;
                    border: 2px solid #FFA500;
                    font-family: "Times New Roman";
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #FF8C00;
                    border-color: #FF8C00;
                }
                QPushButton:pressed {
                    background-color: #FF4500;
                    border-color: #FF4500;
                }
            """)
            self.test_btn.clicked.connect(self.run_auto_test)
            btn_layout.addWidget(self.test_btn)
        
        layout.addWidget(search_label, 0, 0)
        layout.addWidget(self.search_input, 0, 1, 1, 3)
        layout.addWidget(filter_label, 1, 0)
        layout.addWidget(self.supplier_filter, 1, 1)
        layout.addWidget(sort_label, 1, 2)
        layout.addWidget(self.sort_combo, 1, 3)
        
        if user_role == 'администратор':
            layout.addLayout(btn_layout, 2, 0, 1, 4)
        
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
        print(f"🎯 apply_filters вызван! has_management_rights={self.has_management_rights}")
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
        
        # Применяем фильтры - ОБЯЗАТЕЛЬНО для любых изменений
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
                
                # Подключаем сигнал удаления
                if self.user and self.user.role.lower() == 'администратор':
                    card.delete_requested.connect(self.on_product_deleted)
                    # Подключаем сигнал редактирования по двойному клику
                    card.edit_requested.connect(self.edit_product)
                
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
    
    def check_signals(self):
        """Проверяет, подключены ли сигналы"""
        print("🔍 Проверка сигналов:")
        
        # Проверяем, существуют ли виджеты
        if not hasattr(self, 'search_input') or not self.search_input:
            print("   ❌ search_input не существует")
            return
        
        if not hasattr(self, 'supplier_filter') or not self.supplier_filter:
            print("   ❌ supplier_filter не существует")
            return
        
        if not hasattr(self, 'sort_combo') or not self.sort_combo:
            print("   ❌ sort_combo не существует")
            return
        
        try:
            # В PySide6 receivers принимает строку с именем сигнала
            # Для textChanged сигнала
            search_receivers = self.search_input.receivers("textChanged")
            print(f"   search_input.textChanged receivers: {search_receivers}")
        except Exception as e:
            print(f"   Ошибка проверки search_input: {e}")
        
        try:
            # Для currentTextChanged сигнала QComboBox
            supplier_receivers = self.supplier_filter.receivers("currentTextChanged")
            print(f"   supplier_filter.currentTextChanged receivers: {supplier_receivers}")
        except Exception as e:
            print(f"   Ошибка проверки supplier_filter: {e}")
        
        try:
            sort_receivers = self.sort_combo.receivers("currentTextChanged")
            print(f"   sort_combo.currentTextChanged receivers: {sort_receivers}")
        except Exception as e:
            print(f"   Ошибка проверки sort_combo: {e}")
    
    def on_product_deleted(self, product):
        """Обработчик удаления товара"""
        print(f"   🗑️ Товар удален: {product.name}")
        # Обновляем список
        if self.has_management_rights:
            self.apply_filters()
        else:
            self.load_products()
            
    def run_auto_test(self):
        """Запуск автотеста добавления товара"""
        from product_test_service import ProductTestService
        ProductTestService.show_test_results(self)