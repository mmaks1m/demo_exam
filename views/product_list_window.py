import os
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QPushButton, QTableView,
                             QHeaderView, QMessageBox, QFrame)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, Signal
from PySide6.QtGui import QColor, QFont, QBrush

from product_service import ProductService
from views.product_edit_window import ProductEditWindow

class ProductTableModel(QAbstractTableModel):
    def __init__(self, products=None):
        super().__init__()
        self.products = products or []
        self.headers = ["Артикул", "Наименование", "Категория", "Цена", "В наличии", "Скидка", "Поставщик"]
        
    def rowCount(self, parent=QModelIndex()):
        return len(self.products)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.products)):
            return None
            
        product = self.products[index.row()]
        col = index.column()
        
        if role == Qt.DisplayRole:
            if col == 0: return product.article
            elif col == 1: return product.name
            elif col == 2: return product.category
            elif col == 3: return f"{float(product.price):.2f} ₽"
            elif col == 4: return product.stock_quantity
            elif col == 5: return f"{product.discount}%"
            elif col == 6: return product.supplier
            
        elif role == Qt.BackgroundRole:
            # Подсветка согласно ТЗ
            if product.discount > 15:
                return QBrush(QColor("#2E8B57"))  # SeaGreen
            elif product.stock_quantity == 0:
                return QBrush(QColor("lightblue"))
                
        elif role == Qt.ForegroundRole:
            if product.discount > 0 and col == 3:  # Цена со скидкой
                return QBrush(QColor("red"))
                
        elif role == Qt.FontRole:
            if product.discount > 0 and col == 3:
                font = QFont()
                font.setStrikeOut(True)  # Перечеркнутый текст для старой цены
                return font
                
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

class ProductListWindow(QWidget):
    product_selected = Signal(object)
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.products = []
        print(f"🔄 Создание окна товаров для пользователя: {user.full_name if user else 'Гость'}")
        self.setup_ui()
        self.load_products()
        print("✅ Окно товаров создано")
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Панель поиска и фильтрации
        search_panel = self.create_search_panel()
        layout.addWidget(search_panel)
        
        # Таблица товаров
        self.setup_table()
        layout.addWidget(self.table_view)
        
        # Панель кнопок (для администратора)
        if self.user and self.user.role == 'администратор':
            button_panel = self.create_button_panel()
            layout.addWidget(button_panel)
        
        self.setLayout(layout)
    
    def create_search_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QHBoxLayout()
        
        # Поиск
        search_layout = QVBoxLayout()
        search_label = QLabel("Поиск:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию, описанию, категории...")
        self.search_input.textChanged.connect(self.apply_filters)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        
        # Фильтр по поставщику
        filter_layout = QVBoxLayout()
        filter_label = QLabel("Поставщик:")
        self.supplier_combo = QComboBox()
        self.supplier_combo.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.supplier_combo)
        
        # Сортировка
        sort_layout = QVBoxLayout()
        sort_label = QLabel("Сортировка:")
        self.sort_combo = QComboBox()
        self.sort_combo.addItems([
            "По названию (А-Я)",
            "По названию (Я-А)", 
            "По количеству (возр.)",
            "По количеству (убыв.)",
            "По цене (возр.)",
            "По цене (убыв.)"
        ])
        self.sort_combo.currentTextChanged.connect(self.apply_filters)
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        
        layout.addLayout(search_layout, 4)
        layout.addLayout(filter_layout, 2)
        layout.addLayout(sort_layout, 2)
        
        panel.setLayout(layout)
        return panel
    
    def setup_table(self):
        self.table_view = QTableView()
        # УБРАН аргумент user из ProductTableModel
        self.table_model = ProductTableModel()
        self.table_view.setModel(self.table_model)
        
        # Настройка внешнего вида таблицы
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Название растягивается
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Категория
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Поставщик
        
        # Двойной клик для редактирования (для администратора)
        if self.user and self.user.role == 'администратор':
            self.table_view.doubleClicked.connect(self.edit_product)
    
    def create_button_panel(self):
        panel = QFrame()
        layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить товар")
        self.edit_btn = QPushButton("Редактировать товар")
        self.delete_btn = QPushButton("Удалить товар")
        
        self.add_btn.clicked.connect(self.add_product)
        self.edit_btn.clicked.connect(self.edit_selected_product)
        self.delete_btn.clicked.connect(self.delete_product)
        
        layout.addWidget(self.add_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
    
    def load_products(self):
        self.products = ProductService.get_all_products()
        self.table_model.products = self.products
        self.table_model.layoutChanged.emit()
        
        # Загружаем поставщиков в комбобокс
        suppliers = ProductService.get_all_suppliers()
        self.supplier_combo.clear()
        self.supplier_combo.addItem("Все поставщики")
        self.supplier_combo.addItems(suppliers)
    
    def apply_filters(self):
        search_text = self.search_input.text()
        supplier_filter = self.supplier_combo.currentText()
        if supplier_filter == "Все поставщики":
            supplier_filter = ""
        
        sort_map = {
            "По названию (А-Я)": "name_asc",
            "По названию (Я-А)": "name_desc", 
            "По количеству (возр.)": "stock_quantity_asc",
            "По количеству (убыв.)": "stock_quantity_desc",
            "По цене (возр.)": "price_asc",
            "По цене (убыв.)": "price_desc"
        }
        sort_by = sort_map.get(self.sort_combo.currentText(), "name_asc")
        
        self.products = ProductService.get_products_with_filters(
            search_text, supplier_filter, sort_by
        )
        self.table_model.products = self.products
        self.table_model.layoutChanged.emit()
    
    def add_product(self):
        if self.user and self.user.role == 'администратор':
            edit_window = ProductEditWindow(parent=self)
            edit_window.product_saved.connect(self.load_products)
            edit_window.show()
    
    def edit_selected_product(self):
        selected = self.table_view.selectionModel().selectedRows()
        if selected:
            self.edit_product(selected[0])
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите товар для редактирования")
    
    def edit_product(self, index):
        if self.user and self.user.role == 'администратор':
            product = self.products[index.row()]
            edit_window = ProductEditWindow(product, parent=self)
            edit_window.product_saved.connect(self.load_products)
            edit_window.show()
    
    def delete_product(self):
        if self.user and self.user.role == 'администратор':
            selected = self.table_view.selectionModel().selectedRows()
            if not selected:
                QMessageBox.warning(self, "Ошибка", "Выберите товар для удаления")
                return
            
            product = self.products[selected[0].row()]
            reply = QMessageBox.question(
                self, 
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить товар '{product.name}'?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success, message = ProductService.delete_product(product.article)
                if success:
                    QMessageBox.information(self, "Успех", message)
                    self.load_products()
                else:
                    QMessageBox.critical(self, "Ошибка", message)