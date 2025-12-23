from datetime import datetime
from colorama import Fore, Style, init
import database  # Importamos o nosso outro arquivo

init(autoreset=True)

def add_transaction(data):
    try:
        print(f"\n{Fore.CYAN}--- Nova Transação ---")
        description = input("Descrição: ")
        amount = float(input("Valor (ex: 50.50 ou -20.00): "))
        category = input("Categoria: ").capitalize()
        date_now = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        transaction = {
            "description": description,
            "amount": amount,
            "category": category,
            "date": date_now
        }
        
        data.append(transaction)
        database.save_data(data) # Chama a lógica do outro arquivo
        print(f"{Fore.GREEN}✅ Registado com sucesso!")
    except ValueError:
        print(f"{Fore.RED}❌ Erro: Insira um número válido.")

def list_transactions(data):
    print(f"\n{Fore.YELLOW}--- HISTÓRICO ---")
    if not data:
        print("Vazio.")
        return
    for t in data:
        data_t = t.get('date', '---')
        cor = Fore.GREEN if t['amount'] > 0 else Fore.RED
        print(f"{Fore.WHITE}{data_t} | {t['description'][:15]:<15} | {cor}{t['amount']:>8.2f}")

def show_report(data):
    print(f"\n{Fore.MAGENTA}--- RESUMO POR CATEGORIA ---")
    report = database.get_category_report(data)
    for cat, total in report.items():
        cor = Fore.GREEN if total > 0 else Fore.RED
        print(f"{Fore.WHITE}{cat:<15}: {cor}R$ {total:.2f}")

def main():
    data = database.load_data()
    while True:
        saldo = database.get_balance(data)
        cor_saldo = Fore.GREEN if saldo >= 0 else Fore.RED
        
        print(f"\n{Fore.BLUE}======= PY-FINANCE v3.0 =======")
        print(f"SALDO ATUAL: {cor_saldo}R$ {saldo:.2f}")
        print(f"{Fore.WHITE}1. Adicionar | 2. Histórico | 3. Relatório | 4. Sair")
        
        choice = input(f"{Fore.YELLOW}Escolha: ")
        
        if choice == "1":
            add_transaction(data)
        elif choice == "2":
            list_transactions(data)
        elif choice == "3":
            show_report(data)
        elif choice == "4":
            break
        else:
            print(f"{Fore.RED}Inválido!")

if __name__ == "__main__":
    main()