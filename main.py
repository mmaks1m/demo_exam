# main.py - ЕДИНСТВЕННЫЙ ТОЧКА ВХОДА
import sys
import os
import traceback
from PySide6.QtWidgets import QApplication

# Импортируем ВСЕ здесь
from views.login_window import LoginWindow
from views.main_window import MainWindow

class ApplicationController:
    """Простой контроллер приложения"""
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Магазин обуви")
        
        # Загрузка стилей
        if os.path.exists("styles/style.css"):
            with open("styles/style.css", "r", encoding="utf-8") as f:
                self.app.setStyleSheet(f.read())
        
        # Окна
        self.login_window = None
        self.main_window = None
        
    def show_login(self):
        """Показать окно входа"""
        if self.main_window:
            self.main_window.close()
            self.main_window = None
        
        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.show_main_window)
        self.login_window.guest_login.connect(lambda: self.show_main_window(None))
        self.login_window.show()
    
    def show_main_window(self, user=None):
        """Показать главное окно"""
        if self.login_window:
            self.login_window.close()
            self.login_window = None
        
        print(f"✅ Открываем главное окно для: {user.full_name if user else 'Гость'}")
        if user:
            print(f"   Роль: {user.role}")
        
        self.main_window = MainWindow(user)
        self.main_window.logout_requested.connect(self.show_login)
        self.main_window.show()
    
    def run(self):
        """Запустить приложение"""
        self.show_login()
        return self.app.exec()

def main():
    try:
        controller = ApplicationController()
        return controller.run()
    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        traceback.print_exc()
        input("Нажмите Enter для выхода...")
        return 1

if __name__ == "__main__":
    sys.exit(main())