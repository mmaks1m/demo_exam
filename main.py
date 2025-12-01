import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from views.login_window import LoginWindow
from views.main_window import MainWindow

class ShoeShopApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.current_user = None
        self.main_window = None
        self.login_window = None
        self.setApplicationName("Магазин обуви")
        self.setApplicationVersion("1.0")
        
    def set_current_user(self, user):
        self.current_user = user

def main():
    app = ShoeShopApp(sys.argv)
    
    # Загрузка стилей
    if os.path.exists("styles/style.css"):
        with open("styles/style.css", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    
    # Создаем окно входа и сохраняем его в app
    app.login_window = LoginWindow()
    
    def on_login_success(user):
        print(f"🔄 Открываем главное окно для пользователя: {user.full_name}")
        app.set_current_user(user)
        app.login_window.close()
        app.login_window = None  # Освобождаем ссылку
        
        # Создаем и показываем главное окно
        app.main_window = MainWindow(user)
        app.main_window.show()
        print("✅ Главное окно открыто")

    def on_guest_login():
        print("🔄 Открываем главное окно для гостя")
        app.set_current_user(None)
        app.login_window.close()
        app.login_window = None  # Освобождаем ссылку
        
        # Создаем и показываем главное окно для гостя
        app.main_window = MainWindow(None)
        app.main_window.show()
        print("✅ Главное окно открыто для гостя")

    # Подключаем сигналы
    app.login_window.login_success.connect(on_login_success)
    app.login_window.guest_login.connect(on_guest_login)
    
    app.login_window.show()
    print("🚀 Приложение запущено, окно входа показано")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())