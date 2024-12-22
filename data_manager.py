import json
import os
from datetime import datetime

class DataManager:
    def __init__(self):
        self.cards_file = "cards.json"
        self.transactions_file = "transactions.json"
        
        # Проверяем существование обоих файлов
        files_exist = os.path.exists(self.cards_file) and os.path.exists(self.transactions_file)
        
        self.load_data()
        
        # Если хотя бы одного файла нет, создаем тестовые данные
        if not files_exist:
            self.create_sample_data()

    def load_data(self):
        """Загрузка данных из файлов"""
        if os.path.exists(self.cards_file):
            with open(self.cards_file, 'r') as f:
                self.cards = json.load(f)
        else:
            self.cards = {}
            
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'r') as f:
                self.transactions = json.load(f)
        else:
            self.transactions = {}

    def save_data(self):
        """Сохранение данных в файлы"""
        with open(self.cards_file, 'w') as f:
            json.dump(self.cards, f)
        with open(self.transactions_file, 'w') as f:
            json.dump(self.transactions, f)

    def get_cards(self):
        """Получение списка всех карт"""
        return list(self.cards.values())

    def get_card(self, card_number):
        """Получение информации о конкретной карте"""
        return self.cards.get(card_number)

    def add_card(self, card_data):
        """Добавление новой карты"""
        if card_data['number'] in self.cards:
            raise ValueError("Карта с таким номером уже существует")
        self.cards[card_data['number']] = card_data
        self.save_data()

    def update_card(self, card_data):
        """Обновление информации о карте"""
        self.cards[card_data['number']] = card_data
        self.save_data()

    def delete_card(self, card_number):
        """Удаление карты"""
        if card_number in self.cards:
            del self.cards[card_number]
            if card_number in self.transactions:
                del self.transactions[card_number]
            self.save_data()

    def get_transactions(self, card_number, filters=None):
        """Получение транзакций с учетом фильтров"""
        if card_number not in self.transactions:
            return []
            
        transactions = self.transactions[card_number]
        
        if filters:
            filtered = []
            for trans in transactions:
                if (not filters.get('date_from') or 
                    trans['date'] >= filters['date_from']) and \
                   (not filters.get('date_to') or 
                    trans['date'] <= filters['date_to']) and \
                   (not filters.get('category') or 
                    trans['category'] == filters['category']):
                    filtered.append(trans)
            return filtered
            
        return transactions

    def add_transaction(self, card_number, transaction):
        """Добавление новой транзакции"""
        if card_number not in self.transactions:
            self.transactions[card_number] = []
        self.transactions[card_number].append(transaction)
        self.save_data() 

    def get_card_balance(self, card_number):
        """Получение баланса карты"""
        if card_number not in self.transactions:
            return 0
        
        balance = 0
        for trans in self.transactions[card_number]:
            balance += trans['amount']
        return balance

    def create_sample_data(self):
        """Создание тестовых данных"""
        # Очищаем существующие данные
        self.cards = {}
        self.transactions = {}
        
        # Создаем тестовые карты
        cards_data = [
            {
                'number': '4276123456789012',
                'name': 'Иван Петров',
                'cvc': '123'
            },
            {
                'number': '4276987654321098',
                'name': 'Мария Сидорова',
                'cvc': '456'
            }
        ]
        
        # Добавляем карты
        for card in cards_data:
            self.cards[card['number']] = card
        
        # Создаем тестовые транзакции
        transactions_data = {
            '4276123456789012': [
                {
                    'date': '2024-01-15',
                    'amount': 50000,
                    'category': 'Пополнение',
                    'description': 'Зачисление зарплаты'
                },
                {
                    'date': '2024-01-16',
                    'amount': -1500,
                    'category': 'Покупки',
                    'description': 'Продукты в супермаркете'
                },
                {
                    'date': '2024-01-17',
                    'amount': -3000,
                    'category': 'Развлечения',
                    'description': 'Кино и ресторан'
                }
            ],
            '4276987654321098': [
                {
                    'date': '2024-01-10',
                    'amount': 30000,
                    'category': 'Пополнение',
                    'description': 'Перевод от клиента'
                },
                {
                    'date': '2024-01-12',
                    'amount': -5000,
                    'category': 'Транспорт',
                    'description': 'Такси за неделю'
                },
                {
                    'date': '2024-01-13',
                    'amount': -2000,
                    'category': 'Покупки',
                    'description': 'Хозяйственные товары'
                },
                {
                    'date': '2024-01-14',
                    'amount': -1000,
                    'category': 'Развлечения',
                    'description': 'Подписка на сервис'
                }
            ]
        }
        
        self.transactions = transactions_data
        self.save_data()
  