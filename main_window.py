from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QListWidget,
                            QTabWidget)
from card_widget import CardWidget
from transaction_widget import TransactionWidget
from data_manager import DataManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Банковские карты")
        self.setMinimumSize(1000, 600)
        
        self.data_manager = DataManager()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Левая панель со списком карт
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.cards_list = QListWidget()
        self.cards_list.itemClicked.connect(self.show_card_details)
        
        add_card_btn = QPushButton("+ Добавить карту")
        add_card_btn.clicked.connect(self.add_new_card)
        
        left_layout.addWidget(self.cards_list)
        left_layout.addWidget(add_card_btn)
        
        # Правая панель с информацией
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Создаем вкладки для карты и транзакций
        self.tab_widget = QTabWidget()
        self.card_widget = CardWidget(self.data_manager, self)
        self.transaction_widget = TransactionWidget(self.data_manager)
        
        self.tab_widget.addTab(self.card_widget, "Информация о карте")
        self.tab_widget.addTab(self.transaction_widget, "Операции")
        
        right_layout.addWidget(self.tab_widget)
        
        # Добавляем панели в главный layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 2)
        
        self.load_cards()

    def load_cards(self):
        self.cards_list.clear()
        cards = self.data_manager.get_cards()
        for card in cards:
            balance = self.data_manager.get_card_balance(card['number'])
            self.cards_list.addItem(f"{card['name']}\n{card['number']}\nБаланс: {balance} ₽")

    def show_card_details(self, item):
        card_number = item.text().split('\n')[1]
        card = self.data_manager.get_card(card_number)
        self.card_widget.display_card(card)
        self.transaction_widget.load_transactions(card_number)

    def add_new_card(self):
        self.card_widget.clear_form()
        self.tab_widget.setCurrentWidget(self.card_widget)

    def refresh_cards(self):
        self.load_cards() 