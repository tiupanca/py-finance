import json
import os

DATA_FILE = "finance_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def get_balance(data):
    return sum(t['amount'] for t in data)

def get_category_report(data):
    """Gera um resumo de gastos por categoria"""
    report = {}
    for t in data:
        cat = t['category']
        report[cat] = report.get(cat, 0) + t['amount']
    return report

def delete_transaction(data, index):
    """Remove uma transação pelo índice e salva o ficheiro"""
    try:
        # Remove o item da lista
        data.pop(index)
        save_data(data)
        return True
    except IndexError:
        return False
    
def update_transaction(data, index, new_transaction):
    """Substitui uma transação existente por uma nova"""
    try:
        data[index] = new_transaction
        save_data(data)
        return True
    except IndexError:
        return False
    
import csv

def export_to_csv(data):
    """Exporta as transações para um arquivo CSV compatível com Excel"""
    if not data:
        return False
    
    filename = "extrato_financeiro.csv"
    # Definimos os títulos das colunas
    fields = ["date", "description", "category", "amount"]
    
    try:
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
            writer.writeheader()
            writer.writerows(data)
        return filename
    except Exception:
        return False
    
BUDGET_FILE = "budgets.json"

def load_budgets():
    """Carrega as metas de gastos ou retorna um dicionário vazio"""
    if not os.path.exists(BUDGET_FILE):
        return {}
    with open(BUDGET_FILE, "r") as file:
        return json.load(file)

def save_budgets(budgets):
    """Salva as metas no arquivo JSON"""
    with open(BUDGET_FILE, "w") as file:
        json.dump(budgets, file, indent=4)

def check_budget_status(data, category):
    """Retorna quanto já foi gasto e qual a meta para uma categoria"""
    budgets = load_budgets()
    meta = budgets.get(category)
    
    if meta is None:
        return None  # Não há meta para essa categoria
    
    # Soma quanto já gastamos nessa categoria (apenas valores negativos/despesas)
    gastos_atuais = sum(abs(t['amount']) for t in data if t['category'] == category and t['amount'] < 0)
    
    return {"gasto": gastos_atuais, "meta": meta}    
