from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,
                             QTableWidgetItem, QPushButton, QDialog,
                             QFormLayout, QLineEdit, QDateEdit, QComboBox, QHBoxLayout, QDialogButtonBox)
from PyQt5.QtCore import Qt, QDate

class TransactionWidget(QWidget):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.current_card = None
        
        layout = QVBoxLayout(self)
        
        # Создание таблицы транзакций
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Дата", "Сумма", "Категория", "Описание"])
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить транзакцию")
        add_btn.clicked.connect(self.add_transaction)
        
        filter_btn = QPushButton("Фильтр")
        filter_btn.clicked.connect(self.show_filter_dialog)
        
        button_layout.addWidget(add_btn)
        button_layout.addWidget(filter_btn)
        
        layout.addLayout(button_layout)
        layout.addWidget(self.table)

    def load_transactions(self, card_number, filters=None):
        """Загрузка транзакций"""
        self.current_card = card_number
        transactions = self.data_manager.get_transactions(card_number, filters)
        
        self.table.setRowCount(len(transactions))
        for i, trans in enumerate(transactions):
            self.table.setItem(i, 0, QTableWidgetItem(trans['date']))
            self.table.setItem(i, 1, QTableWidgetItem(str(trans['amount'])))
            self.table.setItem(i, 2, QTableWidgetItem(trans['category']))
            self.table.setItem(i, 3, QTableWidgetItem(trans['description']))

    def add_transaction(self):
        """Добавление новой транзакции"""
        dialog = TransactionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            transaction = dialog.get_transaction_data()
            self.data_manager.add_transaction(self.current_card, transaction)
            self.load_transactions(self.current_card)

    def show_filter_dialog(self):
        """Показ диалога фильтрации транзакций"""
        dialog = FilterDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            filters = dialog.get_filter_data()
            self.load_transactions(self.current_card, filters)

class TransactionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Новая транзакция")
        
        layout = QFormLayout(self)
        
        self.date_edit = QDateEdit(QDate.currentDate())
        self.amount_edit = QLineEdit()
        self.category_combo = QComboBox()
        self.category_combo.addItems(["Покупки", "Развлечения", "Транспорт", "Другое"])
        self.description_edit = QLineEdit()
        
        layout.addRow("Дата:", self.date_edit)
        layout.addRow("Сумма:", self.amount_edit)
        layout.addRow("Категория:", self.category_combo)
        layout.addRow("Описание:", self.description_edit)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)

    def get_transaction_data(self):
        return {
            'date': self.date_edit.date().toString(Qt.ISODate),
            'amount': float(self.amount_edit.text()),
            'category': self.category_combo.currentText(),
            'description': self.description_edit.text()
        } 

class FilterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Фильтр транзакций")
        
        layout = QFormLayout(self)
        
        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDate(QDate.currentDate())
        
        self.category_combo = QComboBox()
        self.category_combo.addItems(["", "Покупки", "Развлечения", "Транспорт", "Другое"])
        
        layout.addRow("Дата с:", self.date_from)
        layout.addRow("Дата по:", self.date_to)
        layout.addRow("Категория:", self.category_combo)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addRow(buttons)

    def get_filter_data(self):
        """Получение данных фильтра"""
        return {
            'date_from': self.date_from.date().toString(Qt.ISODate) if self.date_from.date() != self.date_from.minimumDate() else None,
            'date_to': self.date_to.date().toString(Qt.ISODate),
            'category': self.category_combo.currentText() if self.category_combo.currentText() else None
        } 