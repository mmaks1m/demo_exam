# product_test_service.py - автотест для функции добавления товара
import random
import string
from PySide6.QtWidgets import QMessageBox
from product_service import ProductService

class ProductTestService:
    """Сервис для автоматического тестирования добавления товаров"""
    
    @staticmethod
    def generate_test_article():
        """Генерация артикула в формате F572H7 (буква+3 цифры+буква+цифра)"""
        # Формат: буква + 3 цифры + буква + цифра
        first_char = random.choice(string.ascii_uppercase)
        three_digits = ''.join(random.choices(string.digits, k=3))
        second_char = random.choice(string.ascii_uppercase)
        last_digit = random.choice(string.digits)
        
        return f"{first_char}{three_digits}{second_char}{last_digit}"
    
    @staticmethod
    def run_add_product_tests():
        """Запуск всех тестов добавления товара"""
        results = []
        
        # Позитивный тест кейс
        positive_result = ProductTestService.run_positive_test_case()
        results.append(("Позитивный тест", positive_result))
        
        # ТОЛЬКО один негативный тест кейс с дубликатом артикула
        negative_result = ProductTestService.run_negative_test_case_duplicate_article()
        results.append(("Негативный тест (дубликат артикула)", negative_result))
        
        # Формирование итогового сообщения
        return ProductTestService.format_results(results)
    
    @staticmethod
    def run_positive_test_case():
        try:
            test_article = ProductTestService.generate_test_article()
            print(f"Позитивный тест - артикул: {test_article}")
            
            existing_product = ProductService.get_product_by_article(test_article)
            attempt = 0
            while existing_product and attempt < 10:
                test_article = ProductTestService.generate_test_article()
                existing_product = ProductService.get_product_by_article(test_article)
                attempt += 1
            
            if attempt >= 10:
                return False, "Не удалось сгенерировать уникальный артикул после 10 попыток"
            
            test_data = {
                'article': test_article,
                'name': 'Тестовые туфли Marco Tozzi',
                'category': 'Женская обувь',
                'manufacturer': 'Marco Tozzi',
                'supplier': 'Kari',
                'price': 2700.00,
                'stock_quantity': 10,
                'discount': 14,
                'unit': 'шт.',
                'description': 'Элегантные женские туфли для офиса и вечеринок (создано автотестом)',
                'image_path': None
            }
            

            product = ProductService.create_product(test_data)
            
            if product:
                success = (product.article == test_data['article'] and 
                          product.name == test_data['name'] and 
                          float(product.price) == test_data['price'])
                
                if success:
                    return success, f"Товар успешно создан!\nАртикул: {product.article}\nФормат: F572H7 (буква+3 цифры+буква+цифра)\nТовар сохранен в базе данных"
                else:
                    return False, "Созданный товар не соответствует тестовым данным"
            else:
                return False, "Ошибка: товар не был создан"
                
        except Exception as e:
            return False, f"Исключение при выполнении теста: {str(e)}"
    
    @staticmethod
    def run_negative_test_case_duplicate_article():
        """Негативный тест: дубликат артикула (используем существующий F572H7)"""
        try:
            # Используем существующий артикул из вашего примера
            duplicate_article = "F572H7"
            
            # Проверяем, что товар с таким артикулом действительно существует
            existing_product = ProductService.get_product_by_article(duplicate_article)
            
            if not existing_product:
                # Если товара с артикулом F572H7 нет, создаем его для теста
                print(f"Товар с артикулом {duplicate_article} не найден, создаем для теста...")
                temp_product_data = {
                    'article': duplicate_article,
                    'name': 'Туфли Marco Tozzi',
                    'category': 'Женская обувь',
                    'manufacturer': 'Marco Tozzi',
                    'supplier': 'Kari',
                    'price': 2700.00,
                    'stock_quantity': 5,
                    'discount': 14,
                    'unit': 'шт.',
                    'description': 'Туфли Marco Tozzi женские',
                    'image_path': None
                }
                
                temp_product = ProductService.create_product(temp_product_data)
                if not temp_product:
                    return False, f"Не удалось создать тестовый товар с артикулом {duplicate_article}"
                else:
                    print(f"Создан тестовый товар с артикулом {duplicate_article}")
            
            # Теперь пытаемся создать товар с тем же артикулом
            print(f"Попытка создать товар с дубликатом артикула: {duplicate_article}")
            duplicate_test_data = {
                'article': duplicate_article,  # Дубликат артикула
                'name': 'Дублирующие туфли (тест)',
                'category': 'Женская обувь',
                'manufacturer': 'Marco Tozzi',
                'supplier': 'Kari',
                'price': 2500.00,
                'stock_quantity': 3,
                'discount': 10,
                'unit': 'шт.',
                'description': 'Попытка создания товара с дубликатом артикула F572H7',
                'image_path': None
            }
            
            product = ProductService.create_product(duplicate_test_data)
            
            # Ожидаем, что товар НЕ будет создан из-за дубликата артикула
            if product is None:
                return True, f"Тест пройден: товар с дубликатом артикула не создан\nАртикул-дубликат: {duplicate_article}"
            else:
                # Если по какой-то причине товар создался (баг в системе), удаляем его
                ProductService.delete_product(duplicate_article)
                return False, f"Ошибка: товар с дубликатом артикула был создан\nАртикул: {duplicate_article}"
                
        except Exception as e:
            return False, f"Исключение при выполнении теста: {str(e)}"
    
    @staticmethod
    def format_results(results):
        """Форматирование результатов тестов для отображения"""
        total_tests = len(results)
        passed_tests = sum(1 for _, (success, _) in results if success)
        failed_tests = total_tests - passed_tests
        
        message = f"РЕЗУЛЬТАТЫ АВТОТЕСТА ДОБАВЛЕНИЯ ТОВАРА\n"
        message += "=" * 50 + "\n\n"
        message += f"Всего тестов: {total_tests}\n"
        message += f"Пройдено: {passed_tests}\n"
        message += f"Не пройдено: {failed_tests}\n"
        message += f"Успешность: {(passed_tests/total_tests*100):.1f}%\n\n"
        message += "=" * 50 + "\n\n"
        
        for i, (test_name, (success, detail)) in enumerate(results, 1):
            status = "ПРОЙДЕН" if success else "НЕ ПРОЙДЕН"
            message += f"Тест {i}: {test_name}\n"
            message += f"Статус: {status}\n"
            message += f"Детали: {detail}\n"
            message += "-" * 40 + "\n\n"
        
        # Добавляем информацию о сохранении тестового товара
        if total_tests > 0:
            first_test_name, (first_success, first_detail) = results[0]
            if "сохранен в базе данных" in first_detail and first_success:
                message += "Примечание: позитивный тест оставил товар в базе данных\n"
                message += "   для последующей проверки администратором.\n"
                message += "   Товар можно найти по артикулу в формате F572H7.\n\n"
        
        # Итоговая оценка
        if failed_tests == 0:
            message += "ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!\n"
            message += "Функция добавления товара работает корректно.\n"
        elif passed_tests == 0:
            message += "КРИТИЧЕСКИЕ ОШИБКИ!\n"
            message += "Функция добавления товара работает некорректно.\n"
        else:
            message += "ОБНАРУЖЕНЫ ПРОБЛЕМЫ\n"
            message += "Рекомендуется проверить валидацию данных.\n"
        
        message += "=" * 50
        
        return message, passed_tests == total_tests
    
    @staticmethod
    def show_test_results(parent=None):
        """Отображение результатов тестов в диалоговом окне"""
        try:
            # Запускаем тесты
            result_message, all_passed = ProductTestService.run_add_product_tests()
            
            # Создаем диалоговое окно
            msg_box = QMessageBox(parent)
            msg_box.setWindowTitle("Результаты автотеста добавления товара")
            msg_box.setText(result_message)
            
            # Настраиваем стиль окна
            msg_box.setStyleSheet("""
                QMessageBox {
                    background-color: #FFFFFF;
                    font-family: "Times New Roman";
                    min-width: 700px;
                    min-height: 550px;
                }
                QLabel {
                    color: #000000;
                    font-size: 12px;
                    font-family: "Times New Roman";
                }
                QPushButton {
                    background-color: #7FFF00;
                    color: #000000;
                    font-weight: bold;
                    padding: 8px 16px;
                    border-radius: 4px;
                    border: 2px solid #7FFF00;
                    font-family: "Times New Roman";
                    min-width: 80px;
                }
                QPushButton:hover {
                    background-color: #00FA9A;
                    border-color: #00FA9A;
                }
            """)
            
            # Устанавливаем иконку в зависимости от результата
            if all_passed:
                msg_box.setIcon(QMessageBox.Information)
            else:
                msg_box.setIcon(QMessageBox.Warning)
            
            # Добавляем кнопку закрытия
            msg_box.addButton("Закрыть", QMessageBox.AcceptRole)
            
            # Увеличиваем размер окна
            msg_box.setMinimumSize(750, 600)
            
            # Показываем окно
            return msg_box.exec()
            
        except Exception as e:
            QMessageBox.critical(
                parent,
                "Ошибка автотеста",
                f"Не удалось запустить автотест:\n{str(e)}"
            )
            return None