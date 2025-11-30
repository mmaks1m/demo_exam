from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QFrame, QMessageBox)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QPixmap
import os
from auth_service import AuthService

class LoginWindow(QWidget):
    login_success = Signal(object)  # Передает объект пользователя
    guest_login = Signal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход в систему - Магазин обуви")
        self.setFixedSize(400, 500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)
        
        # Заголовок
        title_label = QLabel("Магазин обуви")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        
        # Логотип
        logo_label = QLabel()
        if os.path.exists("resources/images/logo.png"):
            pixmap = QPixmap("resources/images/logo.png")
            logo_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Форма входа
        form_frame = QFrame()
        form_frame.setFrameStyle(QFrame.StyledPanel)
        form_layout = QVBoxLayout()
        form_layout.setSpacing(15)
        
        # Поле логина
        login_layout = QVBoxLayout()
        login_label = QLabel("Логин:")
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Введите ваш логин")
        login_layout.addWidget(login_label)
        login_layout.addWidget(self.login_input)
        
        # Поле пароля
        password_layout = QVBoxLayout()
        password_label = QLabel("Пароль:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите ваш пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        
        # Кнопки
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        self.login_btn = QPushButton("Войти")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E8B57;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3CB371;
            }
            QPushButton:pressed {
                background-color: #228B22;
            }
        """)
        
        self.guest_btn = QPushButton("Войти как гость")
        self.guest_btn.setMinimumHeight(35)
        
        button_layout.addWidget(self.login_btn)
        button_layout.addWidget(self.guest_btn)
        
        # Собираем форму
        form_layout.addLayout(login_layout)
        form_layout.addLayout(password_layout)
        form_layout.addLayout(button_layout)
        form_frame.setLayout(form_layout)
        
        # Собираем главный layout
        layout.addWidget(title_label)
        layout.addWidget(logo_label)
        layout.addWidget(form_frame)
        
        # Подключаем сигналы
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

        print(f"🔐 Попытка входа: логин='{login}', пароль='{password}'")
        
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