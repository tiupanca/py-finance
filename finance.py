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
    print(f"\n{Fore.YELLOW}--- HISTÓRICO DETALHADO ---")
    if not data:
        print("Nenhuma transação encontrada.")
        return

    # Usamos o enumerate para mostrar um número de 1 até o total de itens
    for i, t in enumerate(data):
        data_t = t.get('date', '   Antiga    ')
        cor = Fore.GREEN if t['amount'] > 0 else Fore.RED
        # O [i] mostra o índice para o utilizador saber o que apagar
        print(f"{Fore.WHITE}[{i}] {data_t} | {t['description'][:15]:<15} | {cor}{t['amount']:>8.2f}")

def delete_item_ui(data):
    """Interface para apagar um item"""
    list_transactions(data)
    try:
        idx = int(input(f"\n{Fore.YELLOW}Digite o número [id] para apagar (ou -1 para cancelar): "))
        if idx == -1: return
        
        if database.delete_transaction(data, idx):
            print(f"{Fore.GREEN}✅ Transação removida!")
        else:
            print(f"{Fore.RED}❌ ID não encontrado.")
    except ValueError:
        print(f"{Fore.RED}❌ Digite um número válido.")

def show_report(data):
    print(f"\n{Fore.MAGENTA}--- RESUMO POR CATEGORIA ---")
    report = database.get_category_report(data)
    for cat, total in report.items():
        cor = Fore.GREEN if total > 0 else Fore.RED
        print(f"{Fore.WHITE}{cat:<15}: {cor}R$ {total:.2f}")

def update_item_ui(data):
    """Interface para editar um item existente"""
    list_transactions(data)
    try:
        idx = int(input(f"\n{Fore.YELLOW}Digite o [id] que deseja editar (ou -1 para cancelar): "))
        if idx == -1: return
        
        item_antigo = data[idx]
        print(f"\n{Fore.CYAN}--- Editando (Deixe em branco para manter o atual) ---")
        
        desc = input(f"Nova Descrição [{item_antigo['description']}]: ") or item_antigo['description']
        
        valor_input = input(f"Novo Valor [{item_antigo['amount']}]: ")
        valor = float(valor_input) if valor_input else item_antigo['amount']
        
        cat = input(f"Nova Categoria [{item_antigo['category']}]: ") or item_antigo['category']
        
        # Mantemos a data original da criação ou atualizamos? Vamos manter a original.
        nova_transacao = {
            "description": desc,
            "amount": valor,
            "category": cat.capitalize(),
            "date": item_antigo.get('date', datetime.now().strftime("%d/%m/%Y %H:%M"))
        }
        
        if database.update_transaction(data, idx, nova_transacao):
            print(f"{Fore.GREEN}✅ Transação atualizada!")
    except (ValueError, IndexError):
        print(f"{Fore.RED}❌ Erro ao atualizar. Verifique os dados.")

def main():
    data = database.load_data()
    while True:
        saldo = database.get_balance(data)
        cor_saldo = Fore.GREEN if saldo >= 0 else Fore.RED
        
        print(f"\n{Fore.BLUE}======= PY-FINANCE v4.0 =======")
        print(f"SALDO ATUAL: {cor_saldo}R$ {saldo:.2f}")
        print(f"{Fore.WHITE}1. Add | 2. Histórico | 3. Relatório | 4. Apagar | 5. Editar | 6. Sair")
        
        choice = input(f"{Fore.YELLOW}Escolha: ")
        
        if choice == "1": add_transaction(data)
        elif choice == "2": list_transactions(data)
        elif choice == "3": show_report(data)
        elif choice == "4": delete_item_ui(data)
        elif choice == "5": update_item_ui(data)
        elif choice == "6": break

if __name__ == "__main__":
    main()