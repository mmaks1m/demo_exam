# views/login_window.py - ИСПРАВЛЕННАЯ ВЕРСИЯ
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QMessageBox)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QPixmap, QIcon
import os
from auth_service import AuthService

class LoginWindow(QWidget):
    login_success = Signal(object)
    guest_login = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему - Магазин обуви")
        self.setFixedSize(1000, 850)  # Увеличили высоту для иконки
        if os.path.exists("resources/images/icon.png"):
            self.setWindowIcon(QIcon("resources/images/icon.png"))
        self.setup_ui()
        
    def setup_ui(self):
        self.setStyleSheet("""
            LoginWindow {
                background-color: #FFFFFF;
                font-family: "Times New Roman";
            }
            QLabel {
                font-family: "Times New Roman";
                color: #000000;
            }
            QLineEdit {
                font-family: "Times New Roman";
                background-color: white;
                color: #000000;
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)  
        layout.setContentsMargins(50, 30, 50, 30)
        
        icon_label = QLabel()
        if os.path.exists("resources/images/icon.png"):
            pixmap = QPixmap("resources/images/icon.png")
            scaled_pixmap = pixmap.scaled(120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            icon_label.setPixmap(scaled_pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel("Магазин обуви")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Times New Roman", 20, QFont.Bold))
        title_label.setStyleSheet("color: #000000; margin-bottom: 5px;")
        
        form_frame = QFrame()
        form_frame.setObjectName("loginForm")
        form_frame.setStyleSheet("""
            QFrame#loginForm {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
                margin-top: 10px;
            }
        """)
        
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(20, 15, 20, 15)
        
        form_title = QLabel("Вход в систему")
        form_title.setAlignment(Qt.AlignCenter)
        form_title.setFont(QFont("Times New Roman", 14, QFont.Bold))
        form_title.setStyleSheet("color: #000000; margin-bottom: 10px;")
        
        login_layout = QVBoxLayout()
        login_label = QLabel("Логин:")
        login_label.setStyleSheet("color: #000000; font-weight: bold;")
        
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите ваш логин")
        self.login_input.setMinimumHeight(35)
        
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_input)
        
        password_layout = QVBoxLayout()
        password_label = QLabel("Пароль:")
        password_label.setStyleSheet("color: #000000; font-weight: bold;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(35)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        self.login_btn = QPushButton("Войти")
        self.login_btn.setObjectName("login_btn")
        self.login_btn.setMinimumHeight(45)  
        self.login_btn.setStyleSheet("""
            QPushButton#login_btn {
                background-color: #7FFF00;  
                color: #000000;
                border: 2px solid #5CB800;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12pt;
                font-family: "Times New Roman";
            }
            QPushButton#login_btn:hover {
                background-color: #00FA9A;  
                border-color: #00E58B;
            }
            QPushButton#login_btn:pressed {
                background-color: #00D07A;
                border-color: #00D07A;
            }
        """)
        
        self.guest_btn = QPushButton("Войти как гость")
        self.guest_btn.setObjectName("guest_btn")
        self.guest_btn.setMinimumHeight(45)  
        self.guest_btn.setStyleSheet("""
            QPushButton#guest_btn {
                background-color: #7FFF00;  
                color: #000000;
                border: 2px solid #5CB800;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12pt;  
                font-family: "Times New Roman";
            }
            QPushButton#guest_btn:hover {
                background-color: #00FA9A;  
                border-color: #00E58B;
            }
            QPushButton#guest_btn:pressed {
                background-color: #00D07A;
                border-color: #00D07A;
            }
        """)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.guest_btn)
        
        form_layout.addWidget(form_title)
        form_layout.addLayout(login_layout)
        form_layout.addLayout(password_layout)
        form_layout.addLayout(button_layout)
        form_frame.setLayout(form_layout)
        
        layout.addWidget(icon_label)  
        layout.addWidget(title_label)
        layout.addWidget(form_frame)
        layout.addStretch()
        
        self.login_btn.clicked.connect(self.authenticate)
        self.guest_btn.clicked.connect(self.guest_login)
        self.password_input.returnPressed.connect(self.authenticate)
        
        self.setLayout(layout)
    
    def authenticate(self):
        login = self.login_input.text().strip()
        password = self.password_input.text()

        if not login:
            QMessageBox.warning(self, "Ошибка", "Введите логин")
            self.login_input.setFocus()
            return

        if not password:
            QMessageBox.warning(self, "Ошибка", "Введите пароль")
            self.password_input.setFocus()
            return

        # Показываем индикатор загрузки
        self.login_btn.setText("Вход...")
        self.login_btn.setEnabled(False)

        print(f"Попытка входа: логин='{login}', пароль='{password}'")
        
        # Передаем пароль как есть, без хеширования
        user = AuthService.authenticate(login, password)

        # Восстанавливаем кнопку
        self.login_btn.setText("Войти")
        self.login_btn.setEnabled(True)

        if user:
            print(f"✅ Успешный вход: {user.full_name}")
            self.login_success.emit(user)
        else:
            print("❌ Неверный логин или пароль")
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")
            self.password_input.clear()
            self.password_input.setFocus()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def guest_login_handler(self):
        self.guest_login.emit()