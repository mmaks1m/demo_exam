import sys
import os
from PySide6.QtWidgets import QApplication, QToolBar
from PySide6.QtGui import QIcon, QAction

from views.login_window import LoginWindow
from views.main_window import MainWindow

class ShoeShopApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.current_user = None
        self.main_window = None
        self.setApplicationName("Магазин обуви")
        self.setApplicationVersion("1.0")
        
    def set_current_user(self, user):
        self.current_user = user
    
    def setup_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # Кнопка "Товары" - для всех
        products_action = QAction("Товары", self)
        products_action.triggered.connect(self.show_products)
        toolbar.addAction(products_action)
        
        # Кнопка "Заказы" - только для менеджера и администратора
        if self.user and self.user.role in ['менеджер', 'администратор']:
            orders_action = QAction("Заказы", self)
            orders_action.triggered.connect(self.show_orders)
            toolbar.addAction(orders_action)
        
        toolbar.addSeparator()
        
        # Кнопка выхода
        logout_action = QAction("Выйти", self)
        logout_action.triggered.connect(self.logout)
        toolbar.addAction(logout_action)

def main():
    app = ShoeShopApp(sys.argv)
    
    # Загрузка стилей
    if os.path.exists("styles/style.css"):
        with open("styles/style.css", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    
    login_window = LoginWindow()
    
    def on_login_success(user):
        print(f"🔄 Открываем главное окно для пользователя: {user.full_name}")
        app.set_current_user(user)
        login_window.close()
        
        # Создаем и показываем главное окно
        app.main_window = MainWindow(user)
        app.main_window.show()
        print("✅ Главное окно открыто")

    def on_guest_login():
        print("🔄 Открываем главное окно для гостя")
        app.set_current_user(None)
        login_window.close()
        
        # Создаем и показываем главное окно для гостя
        app.main_window = MainWindow(None)
        app.main_window.show()
        print("✅ Главное окно открыто для гостя")

    # Подключаем сигналы
    login_window.login_success.connect(on_login_success)
    login_window.guest_login.connect(on_guest_login)
    
    login_window.show()
    print("🚀 Приложение запущено, окно входа показано")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())