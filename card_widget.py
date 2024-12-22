from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout,
                            QLineEdit, QPushButton, QMessageBox, 
                            QHBoxLayout, QGroupBox, QInputDialog, QDialog, QDialogButtonBox)
from PyQt5.QtCore import Qt, QDate
import random

class CardDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление новой карты")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Форма
        form_layout = QFormLayout()
        
        self.first_name_edit = QLineEdit()
        self.last_name_edit = QLineEdit()
        self.number_edit = QLineEdit()
        self.number_edit.setReadOnly(True)
        self.cvc_edit = QLineEdit()
        self.cvc_edit.setReadOnly(True)
        
        form_layout.addRow("Имя:", self.first_name_edit)
        form_layout.addRow("Фамилия:", self.last_name_edit)
        form_layout.addRow("Номер карты:", self.number_edit)
        form_layout.addRow("CVC:", self.cvc_edit)
        
        # Кнопка генерации
        generate_btn = QPushButton("Сгенерировать номер карты и CVC")
        generate_btn.clicked.connect(self.generate_card_details)
        
        # Кнопки OK и Cancel
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        
        layout.addLayout(form_layout)
        layout.addWidget(generate_btn)
        layout.addWidget(buttons)
        
        # Генерируем номер карты и CVC при открытии
        self.generate_card_details()

    def generate_card_details(self):
        """Генерация номера карты и CVC"""
        # Генерация номера карты (16 цифр, начинается с 4)
        card_number = "4" + "".join([str(random.randint(0, 9)) for _ in range(15)])
        # Форматирование номера карты для читаемости (4444 4444 4444 4444)
        formatted_number = " ".join([card_number[i:i+4] for i in range(0, 16, 4)])
        self.number_edit.setText(formatted_number)
        
        # Генерация CVC (3 цифры)
        cvc = "".join([str(random.randint(0, 9)) for _ in range(3)])
        self.cvc_edit.setText(cvc)

    def validate_and_accept(self):
        """Проверка заполнения полей"""
        if not self.first_name_edit.text() or not self.last_name_edit.text():
            QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните имя и фамилию")
            return
        self.accept()

    def get_card_data(self):
        """Получение данных карты"""
        return {
            'number': self.number_edit.text().replace(" ", ""),  # Убираем пробелы
            'name': f"{self.first_name_edit.text()} {self.last_name_edit.text()}",
            'cvc': self.cvc_edit.text()
        }

class CardWidget(QWidget):
    def __init__(self, data_manager, main_window):
        super().__init__()
        self.data_manager = data_manager
        self.main_window = main_window
        self.current_card = None
        
        layout = QVBoxLayout(self)
        
        # Форма с информацией о карте
        form_group = QGroupBox("Данные карты")
        form_layout = QFormLayout()
        
        self.number_edit = QLineEdit()
        self.name_edit = QLineEdit()
        self.balance_edit = QLineEdit()
        self.cvc_edit = QLineEdit()  # Д��бавляем поле CVC
        
        self.balance_edit.setReadOnly(True)
        self.number_edit.setReadOnly(True)  # Делаем поле номера только для чтения
        self.cvc_edit.setReadOnly(True)    # Делаем поле CVC только для чтения
        
        form_layout.addRow("Номер карты:", self.number_edit)
        form_layout.addRow("Имя владельца:", self.name_edit)
        form_layout.addRow("CVC:", self.cvc_edit)
        form_layout.addRow("Баланс:", self.balance_edit)
        form_group.setLayout(form_layout)
        
        # Кнопки операций
        operations_group = QGroupBox("Операции")
        operations_layout = QVBoxLayout()
        
        deposit_btn = QPushButton("Пополнить")
        withdraw_btn = QPushButton("Снять")
        save_btn = QPushButton("Сохранить изменения")
        delete_btn = QPushButton("Удалить карту")
        
        deposit_btn.clicked.connect(self.deposit_money)
        withdraw_btn.clicked.connect(self.withdraw_money)
        save_btn.clicked.connect(self.save_card)
        delete_btn.clicked.connect(self.delete_card)
        
        operations_layout.addWidget(deposit_btn)
        operations_layout.addWidget(withdraw_btn)
        operations_layout.addWidget(save_btn)
        operations_layout.addWidget(delete_btn)
        operations_group.setLayout(operations_layout)
        
        layout.addWidget(form_group)
        layout.addWidget(operations_group)
        layout.addStretch()

    def display_card(self, card):
        """Отображение информации о карте"""
        self.current_card = card
        # Форматируем номер карты для отображения
        formatted_number = " ".join([card['number'][i:i+4] for i in range(0, 16, 4)])
        self.number_edit.setText(formatted_number)
        self.name_edit.setText(card['name'])
        # Проверяем наличие CVC кода
        self.cvc_edit.setText(card.get('cvc', '***'))  # Используем get() с значением по умолчанию
        balance = self.data_manager.get_card_balance(card['number'])
        self.balance_edit.setText(f"{balance} ₽")

    def clear_form(self):
        """Открытие диалога добавления новой карты"""
        dialog = CardDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            card_data = dialog.get_card_data()
            self.data_manager.add_card(card_data)
            self.main_window.refresh_cards()

    def deposit_money(self):
        if not self.current_card:
            return
        amount, ok = QInputDialog.getDouble(self, "Пополнение", 
                                          "Введите сумму:", 0, 0, 1000000, 2)
        if ok:
            self.data_manager.add_transaction(self.current_card['number'], {
                'date': QDate.currentDate().toString(Qt.ISODate),
                'amount': amount,
                'category': 'Пополнение',
                'description': 'Пополнение карты'
            })
            self.display_card(self.current_card)
            self.main_window.refresh_cards()

    def withdraw_money(self):
        if not self.current_card:
            return
        balance = self.data_manager.get_card_balance(self.current_card['number'])
        amount, ok = QInputDialog.getDouble(self, "Снятие", 
                                          "Введите сумму:", 0, 0, balance, 2)
        if ok:
            self.data_manager.add_transaction(self.current_card['number'], {
                'date': QDate.currentDate().toString(Qt.ISODate),
                'amount': -amount,
                'category': 'Снятие',
                'description': 'Снятие с карты'
            })
            self.display_card(self.current_card)
            self.main_window.refresh_cards()

    def save_card(self):
        """Сохранение информации о карте"""
        card_data = {
            'number': self.number_edit.text().replace(" ", ""),  # Убираем пробелы
            'name': self.name_edit.text(),
            'cvc': self.cvc_edit.text()  # Добавляем CVC в данные карты
        }
        
        if self.current_card:
            self.data_manager.update_card(card_data)
        else:
            self.data_manager.add_card(card_data)
        
        self.main_window.refresh_cards()
        QMessageBox.information(self, "Успех", "Карта сохранена")

    def delete_card(self):
        if self.current_card:
            reply = QMessageBox.question(self, "Подтверждение", 
                                       "Удалить карту?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.data_manager.delete_card(self.current_card['number'])
                self.clear_form()
                self.main_window.refresh_cards() 