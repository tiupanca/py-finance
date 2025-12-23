import json
import os
from datetime import datetime
from colorama import Fore, Style, init

# Inicializa o colorama para funcionar no Windows e Linux
init(autoreset=True)

DATA_FILE = "finance_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_transaction(data):
    try:
        print(f"\n{Fore.CYAN}--- Nova Transação ---")
        description = input("Descrição: ")
        amount = float(input("Valor (ex: 50.50 ou -20.00): "))
        category = input("Categoria: ")
        # Pega a data e hora atual formatada
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        transaction = {
            "description": description,
            "amount": amount,
            "category": category,
            "date": date_now
        }
        
        data.append(transaction)
        save_data(data)
        print(f"{Fore.GREEN}✅ Adicionado em {date_now}!")
    except ValueError:
        print(f"{Fore.RED}❌ Erro: Valor inválido.")

def show_balance(data):
    total = sum(t['amount'] for t in data)
    cor = Fore.GREEN if total >= 0 else Fore.RED
    print(f"\n{cor}--- SALDO ATUAL: R$ {total:.2f} ---")

def list_transactions(data):
    print(f"\n{Fore.YELLOW}--- HISTÓRICO DE TRANSAÇÕES ---")
    if not data:
        print("Nenhuma transação encontrada.")
        return

    for i, t in enumerate(data, 1):
        # A MÁGICA ESTÁ AQUI: se não tiver 'date', ele usa '---'
        data_transacao = t.get('date', '   Antiga    ')
        
        cor = Fore.GREEN if t['amount'] > 0 else Fore.RED
        simbolo = "+" if t['amount'] > 0 else ""
        
        # Formatando a exibição para ficar alinhada
        desc = t['description'][:15].ljust(15)
        cat = t['category'][:10].ljust(10)
        
        print(f"{Fore.WHITE}{data_transacao} | {desc} | {cat} | {cor}{simbolo}{t['amount']:.2f}")

def main():
    data = load_data()
    while True:
        print(f"\n{Fore.BLUE}======= PY-FINANCE v2.0 =======")
        print("1. Adicionar Transação")
        print("2. Ver Saldo")
        print("3. Listar Histórico")
        print("4. Sair")
        
        choice = input(f"{Fore.YELLOW}Escolha: ")
        
        if choice == "1":
            add_transaction(data)
        elif choice == "2":
            show_balance(data)
        elif choice == "3":
            list_transactions(data)
        elif choice == "4":
            print(f"{Fore.CYAN}Saindo e salvando dados...")
            break
        else:
            print(f"{Fore.RED}Opção inválida!")

if __name__ == "__main__":
    main()