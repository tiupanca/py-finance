from datetime import datetime
from colorama import Fore, Style, init
from database import FinanceDatabase

init(autoreset=True)

# Criamos o objeto que gerencia o banco de dados
db = FinanceDatabase()

def add_transaction(data):
    try:
        print(f"\n{Fore.CYAN}--- Nova Transação ---")
        desc = input("Descrição: ")
        amount = float(input("Valor (ex: 50.50 ou -20.00): "))
        cat = input("Categoria: ").capitalize()
        
        # Lógica de Metas
        budgets = db.load_budgets()
        if amount < 0 and cat in budgets:
            gasto_atual = sum(abs(t['amount']) for t in data if t['category'] == cat and t['amount'] < 0)
            if gasto_atual + abs(amount) > budgets[cat]:
                print(f"\n{Fore.RED}⚠️ ALERTA: Esta despesa ultrapassa a meta de R$ {budgets[cat]:.2f}!")
                input("Pressione Enter para continuar mesmo assim...")

        data.append({
            "description": desc,
            "amount": amount,
            "category": cat,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        db.save_data(data)
        print(f"{Fore.GREEN}✅ Registrado com sucesso!")
    except ValueError:
        print(f"{Fore.RED}❌ Erro: Valor inválido.")

def list_transactions(data):
    print(f"\n{Fore.YELLOW}--- HISTÓRICO DETALHADO ---")
    if not data:
        print("Vazio.")
        return
    for i, t in enumerate(data):
        data_t = t.get('date', '---')
        cor = Fore.GREEN if t['amount'] > 0 else Fore.RED
        print(f"{Fore.WHITE}[{i}] {data_t} | {t['description'][:15]:<15} | {cor}{t['amount']:>8.2f}")

def show_report(data):
    print(f"\n{Fore.MAGENTA}--- RELATÓRIO E METAS ---")
    report = db.get_category_report(data)
    budgets = db.load_budgets()
    for cat, total in report.items():
        meta = budgets.get(cat)
        meta_str = f" / Meta: R$ {meta:.2f}" if meta else ""
        cor = Fore.GREEN if total > 0 else Fore.RED
        if meta and abs(total) > meta and total < 0:
            cor = Fore.LIGHTRED_EX
            meta_str += " 🚨 (ESTOUROU!)"
        print(f"{Fore.WHITE}{cat:<15}: {cor}R$ {total:.2f}{Fore.WHITE}{meta_str}")

def delete_item_ui(data):
    list_transactions(data)
    try:
        idx = int(input(f"\n{Fore.YELLOW}ID para apagar (-1 cancela): "))
        if idx == -1: return
        data.pop(idx)
        db.save_data(data)
        print(f"{Fore.GREEN}✅ Removido!")
    except (ValueError, IndexError):
        print(f"{Fore.RED}❌ ID inválido.")

def set_budget_ui():
    budgets = db.load_budgets()
    print(f"\n{Fore.CYAN}--- Definir Metas ---")
    cat = input("Categoria: ").capitalize()
    try:
        limite = float(input(f"Limite para {cat}: R$ "))
        budgets[cat] = limite
        db.save_budgets(budgets)
        print(f"{Fore.GREEN}✅ Meta definida!")
    except ValueError:
        print(f"{Fore.RED}❌ Valor inválido.")

def main():
    data = db.load_data()
    while True:
        saldo = db.get_balance(data)
        cor_saldo = Fore.GREEN if saldo >= 0 else Fore.RED
        print(f"\n{Fore.BLUE}======= PY-FINANCE v6.0 (POO) =======")
        print(f"SALDO ATUAL: {cor_saldo}R$ {saldo:.2f}")
        print(f"{Fore.WHITE}1. Add | 2. Lista | 3. Relatório | 4. Apagar | 5. Metas | 6. Exportar | 7. Sair")
        
        choice = input(f"{Fore.YELLOW}Escolha: ")
        if choice == "1": add_transaction(data)
        elif choice == "2": list_transactions(data)
        elif choice == "3": show_report(data)
        elif choice == "4": delete_item_ui(data)
        elif choice == "5": set_budget_ui()
        elif choice == "6":
            arq = db.export_to_csv(data)
            print(f"{Fore.GREEN}✅ Exportado: {arq}" if arq else f"{Fore.RED}❌ Falha")
        elif choice == "7": break

if __name__ == "__main__":
    main()