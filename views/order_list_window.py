from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QTableView, QPushButton, QMessageBox, QFrame,
                             QHeaderView)
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex
from PySide6.QtGui import QColor, QBrush

from order_service import OrderService
from views.order_edit_window import OrderEditWindow

class OrderTableModel(QAbstractTableModel):
    def __init__(self, orders=None):
        super().__init__()
        self.orders = orders or []
        self.headers = ["ID", "Артикул", "Статус", "Пользователь", "Дата заказа", "Дата доставки", "Пункт выдачи"]
        
    def rowCount(self, parent=QModelIndex()):
        return len(self.orders)
    
    def columnCount(self, parent=QModelIndex()):
        return len(self.headers)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.orders)):
            return None
            
        order = self.orders[index.row()]
        col = index.column()
        
        if role == Qt.DisplayRole:
            if col == 0: return order.id
            elif col == 1: return order.order_article if hasattr(order, 'order_article') else f"ORD-{order.id}"
            elif col == 2: return order.status
            elif col == 3: return order.user.full_name if order.user else "Неизвестно"
            elif col == 4: return order.order_date.strftime("%d.%m.%Y %H:%M") if order.order_date else ""
            elif col == 5: return order.delivery_date.strftime("%d.%m.%Y %H:%M") if order.delivery_date else ""
            elif col == 6: return order.pickup_point.address if order.pickup_point else "Не указан"
            
        elif role == Qt.BackgroundRole:
            # Подсветка статусов
            status = order.status.lower()
            if status in ['выполнен', 'доставлен']:
                return QBrush(QColor("#d4edda"))  # Зеленый
            elif status in ['отменен', 'отменён']:
                return QBrush(QColor("#f8d7da"))  # Красный
            elif status in ['в обработке', 'обработка']:
                return QBrush(QColor("#fff3cd"))  # Желтый
                
        return None
    
    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.headers[section]
        return None

class OrderListWindow(QWidget):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.orders = []
        self.setup_ui()
        self.load_orders()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel("Управление заказами")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2E8B57; margin: 10px;")
        
        # Таблица заказов
        self.setup_table()
        
        # Панель кнопок (для администратора)
        if self.user and self.user.role == 'администратор':
            button_panel = self.create_button_panel()
            layout.addWidget(button_panel)
        
        layout.addWidget(title_label)
        layout.addWidget(self.table_view)
        
        self.setLayout(layout)
    
    def setup_table(self):
        self.table_view = QTableView()
        self.table_model = OrderTableModel()
        self.table_view.setModel(self.table_model)
        
        # Настройка внешнего вида таблицы
        header = self.table_view.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # Пользователь растягивается
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Пункт выдачи
        
        # Двойной клик для редактирования
        if self.user and self.user.role in ['менеджер', 'администратор']:
            self.table_view.doubleClicked.connect(self.edit_order)
    
    def create_button_panel(self):
        panel = QFrame()
        layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Добавить заказ")
        self.edit_btn = QPushButton("Редактировать заказ")
        self.delete_btn = QPushButton("Удалить заказ")
        
        self.add_btn.clicked.connect(self.add_order)
        self.edit_btn.clicked.connect(self.edit_selected_order)
        self.delete_btn.clicked.connect(self.delete_order)
        
        layout.addWidget(self.add_btn)
        layout.addWidget(self.edit_btn)
        layout.addWidget(self.delete_btn)
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
    
    def load_orders(self):
        self.orders = OrderService.get_all_orders()
        self.table_model.orders = self.orders
        self.table_model.layoutChanged.emit()
    
    def add_order(self):
        if self.user and self.user.role == 'администратор':
            edit_window = OrderEditWindow(parent=self)
            edit_window.order_saved.connect(self.load_orders)
            edit_window.show()
    
    def edit_selected_order(self):
        selected = self.table_view.selectionModel().selectedRows()
        if selected:
            self.edit_order(selected[0])
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите заказ для редактирования")
    
    def edit_order(self, index):
        if self.user and self.user.role in ['менеджер', 'администратор']:
            order = self.orders[index.row()]
            edit_window = OrderEditWindow(order, parent=self)
            edit_window.order_saved.connect(self.load_orders)
            edit_window.show()
    
    def delete_order(self):
        if self.user and self.user.role == 'администратор':
            selected = self.table_view.selectionModel().selectedRows()
            if not selected:
                QMessageBox.warning(self, "Ошибка", "Выберите заказ для удаления")
                return
            
            order = self.orders[selected[0].row()]
            reply = QMessageBox.question(
                self, 
                "Подтверждение удаления",
                f"Вы уверены, что хотите удалить заказ #{order.id}?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                success, message = OrderService.delete_order(order.id)
                if success:
                    QMessageBox.information(self, "Успех", message)
                    self.load_orders()
                else:
                    QMessageBox.critical(self, "Ошибка", message)