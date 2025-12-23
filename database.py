import json
import os
import csv

class FinanceDatabase:
    def __init__(self, data_file="finance_data.json", budget_file="budgets.json"):
        self.data_file = data_file
        self.budget_file = budget_file

    def load_data(self):
        if not os.path.exists(self.data_file):
            return []
        with open(self.data_file, "r") as file:
            return json.load(file)

    def save_data(self, data):
        with open(self.data_file, "w") as file:
            json.dump(data, file, indent=4)

    def load_budgets(self):
        if not os.path.exists(self.budget_file):
            return {}
        with open(self.budget_file, "r") as file:
            return json.load(file)

    def save_budgets(self, budgets):
        with open(self.budget_file, "w") as file:
            json.dump(budgets, file, indent=4)

    def get_balance(self, data):
        return sum(t['amount'] for t in data)

    def get_category_report(self, data):
        report = {}
        for t in data:
            cat = t['category']
            report[cat] = report.get(cat, 0) + t['amount']
        return report

    def export_to_csv(self, data):
        if not data: return False
        filename = "extrato_financeiro.csv"
        fields = ["date", "description", "category", "amount"]
        try:
            with open(filename, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=fields, delimiter=";")
                writer.writeheader()
                writer.writerows(data)
            return filename
        except Exception:
            return False