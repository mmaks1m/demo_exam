import sys
import os
import traceback
from PySide6.QtWidgets import QApplication, QMessageBox

from views.login_window import LoginWindow
from views.main_window import MainWindow

class ApplicationController:
    def __init__(self):
        # Windows consoles may not support the symbols used in diagnostic output.
        for stream in (sys.stdout, sys.stderr):
            if stream is not None and hasattr(stream, "reconfigure"):
                stream.reconfigure(errors="backslashreplace")
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Магазин обуви")
        
        # Загрузка стилей
        if os.path.exists("styles/style.css"):
            with open("styles/style.css", "r", encoding="utf-8") as f:
                self.app.setStyleSheet(f.read())
        
        # Окна
        self.login_window = None
        self.main_window = None
        self.check_database_connection()

    def check_database_connection(self):
        """Проверка доступности базы данных перед открытием окон (#4)"""
        try:
            from database import engine
            with engine.connect() as conn:
                pass
        except Exception as err:
            QMessageBox.critical(
                None,
                "Ошибка подключения к базе данных",
                "Не удалось установить соединение с сервером PostgreSQL.\n\n"
                "Пожалуйста, проверьте:\n"
                "1. Запущена ли служба PostgreSQL на вашем компьютере;\n"
                "2. Заполнены ли корректные параметры подключения в файле config.ini "
                "(секция [database]: host, port, name, user, password).\n\n"
                f"Техническая информация:\n{err}"
            )
        
    def show_login(self):
        window = LoginWindow()
        window.login_success.connect(self.show_main_window)
        window.guest_login.connect(lambda: self.show_main_window(None))
        self.login_window = window
        window.show()
        if self.main_window:
            self.main_window.close()
            self.main_window = None

    def show_main_window(self, user=None):
        try:
            window = MainWindow(user)
            window.logout_requested.connect(self.show_login)
            window.show()
        except Exception as error:
            traceback.print_exc()
            QMessageBox.critical(
                self.login_window, "Ошибка открытия каталога", str(error)
            )
            return
        self.main_window = window
        if self.login_window:
            self.login_window.close()
            self.login_window = None

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