import sqlite3
import csv
from datetime import datetime

class FinanceDatabase:
    def __init__(self, db_name="finance.db"):
        self.db_name = db_name
        self.create_tables()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_tables(self):
        """Cria as tabelas de transações e metas se não existirem"""
        with self.connect() as conn:
            cursor = conn.cursor()
            # Tabela de Transações
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL,
                    date TEXT NOT NULL
                )
            """)
            # Tabela de Metas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS budgets (
                    category TEXT PRIMARY KEY,
                    limit_amount REAL NOT NULL
                )
            """)
            conn.commit()

    def save_data(self, description, amount, category):
        """Salva uma nova transação no SQL"""
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (description, amount, category, date) VALUES (?, ?, ?, ?)",
                (description, amount, category, date_now)
            )
            conn.commit()

    def load_data(self):
        """Lê todas as transações do SQL"""
        with self.connect() as conn:
            conn.row_factory = sqlite3.Row # Permite acessar como dicionário
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions ORDER BY id DESC")
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_balance(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM transactions")
            res = cursor.fetchone()[0]
            return res if res else 0.0

    def save_budgets(self, category, limit_amount):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO budgets (category, limit_amount) VALUES (?, ?)",
                (category, limit_amount)
            )
            conn.commit()

    def load_budgets(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM budgets")
            return {row[0]: row[1] for row in cursor.fetchall()}

    def get_category_report(self):
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category, SUM(amount) FROM transactions GROUP BY category")
            return {row[0]: row[1] for row in cursor.fetchall()}