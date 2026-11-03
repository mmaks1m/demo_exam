# views/order_list_window.py - ИСПРАВЛЕННЫЙ С ОБРАБОТКОЙ ОКОН
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QMessageBox, QFrame, QScrollArea)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from order_service import OrderService
from views.order_edit_window import OrderEditWindow
from views.order_card_widget import OrderCardWidget

class OrderListWindow(QWidget):
    """Окно списка заказов в виде карточек"""
    data_updated = Signal()
    
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.orders = []
        self.current_edit_window = None  # Чтобы предотвратить множественное редактирование
        self.setup_ui()
        self.load_orders()
        
        print(f"✅ OrderListWindow создан для: {user.full_name if user else 'Гость'}")
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Заголовок
        title_label = QLabel("Управление заказами")
        title_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: #000000;
            margin: 10px;
            padding: 10px;
            border-radius: 8px;
            border: 2px solid #7FFF00;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Панель кнопок (для администратора)
        if self.user and self.user.role.lower() == 'администратор':
            button_panel = self.create_button_panel()
            layout.addWidget(button_panel)
        
        # Контейнер для заказов
        self.orders_container = QWidget()
        self.orders_layout = QVBoxLayout(self.orders_container)
        self.orders_layout.setSpacing(10)
        self.orders_layout.setContentsMargins(5, 5, 5, 5)
        
        # Скроллируемая область
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.orders_container)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        layout.addWidget(scroll_area, 1)
        self.setLayout(layout)
    
    def create_button_panel(self):
        """Создает панель управления для администратора"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #F8FFF8;
                border: 2px solid #7FFF00;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить заказ")
        add_btn.setMinimumHeight(40)
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #7FFF00;
                color: #000000;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 6px;
                border: 2px solid #7FFF00;
                font-family: "Times New Roman";
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #00FA9A;
                border-color: #00FA9A;
            }
        """)
        add_btn.clicked.connect(self.add_order)
        
        layout.addWidget(add_btn)
        layout.addStretch()
        
        panel.setLayout(layout)
        return panel
    
    def load_orders(self):
        """Загрузка всех заказов"""
        print("   📥 Загружаем заказы...")
        self.orders = OrderService.get_all_orders()
        print(f"   ✅ Загружено заказов: {len(self.orders)}")
        self.display_orders()
    
    def display_orders(self):
        """Отображение заказов в виде карточек"""
        # Очищаем контейнер
        for i in reversed(range(self.orders_layout.count())): 
            widget = self.orders_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
        
        # Добавляем заказы
        if not self.orders:
            no_orders_label = QLabel("ЗАКАЗЫ НЕ НАЙДЕНЫ")
            no_orders_label.setAlignment(Qt.AlignCenter)
            no_orders_label.setStyleSheet("""
                QLabel {
                    font-size: 18px; 
                    color: #000000;
                    padding: 40px;
                    font-family: "Times New Roman";
                    font-weight: bold;
                }
            """)
            self.orders_layout.addWidget(no_orders_label)
            print("   ⚠️ Заказы не найдены")
        else:
            for order in self.orders:
                card = OrderCardWidget(order, self.user)
                
                # Подключаем сигналы (для администратора)
                if self.user and self.user.role.lower() == 'администратор':
                    card.edit_requested.connect(self.edit_order)
                    card.delete_requested.connect(self.delete_order)
                
                self.orders_layout.addWidget(card)
            
            print(f"   ✅ Отображено заказов: {len(self.orders)}")
        
        self.orders_layout.addStretch()
    
    def add_order(self):
        """Добавление нового заказа (только администратор)"""
        if self.user and self.user.role.lower() == 'администратор':
            print("   🆕 Открываем окно добавления заказа")
            
            # Проверяем, нет ли уже открытого окна редактирования
            if self.current_edit_window is not None and self.current_edit_window.isVisible():
                QMessageBox.warning(self, "Предупреждение", 
                                  "Закройте окно редактирования перед созданием нового заказа.")
                return
            
            self.current_edit_window = OrderEditWindow(parent=self)
            self.current_edit_window.order_saved.connect(self.on_order_saved)
            self.current_edit_window.destroyed.connect(lambda: setattr(self, 'current_edit_window', None))
            self.current_edit_window.show()
    
    def edit_order(self, order):
        """Редактирование заказа (только администратор)"""
        if self.user and self.user.role.lower() == 'администратор':
            print(f"   ✏️ Редактирование заказа: {order.id}")
            
            # Проверяем, нет ли уже открытого окна редактирования
            if self.current_edit_window is not None and self.current_edit_window.isVisible():
                QMessageBox.warning(self, "Предупреждение", 
                                  "Закройте окно редактирования перед открытием нового.")
                return
            
            self.current_edit_window = OrderEditWindow(order, parent=self)
            self.current_edit_window.order_saved.connect(self.on_order_saved)
            self.current_edit_window.destroyed.connect(lambda: setattr(self, 'current_edit_window', None))
            self.current_edit_window.show()
    
    def delete_order(self, order):
        """Удаление заказа (только администратор)"""
        if self.user and self.user.role.lower() == 'администратор':
            print(f"   🗑️ Удаление заказа: {order.id}")
            
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
                    self.load_orders()  # Обновляем список
                else:
                    QMessageBox.critical(self, "Ошибка", message)
    
    def on_order_saved(self):
        """Обновление списка после сохранения"""
        print("   🔄 Обновляем список заказов после сохранения")
        self.load_orders()
        # Очищаем ссылку на окно редактирования
        self.current_edit_window = None