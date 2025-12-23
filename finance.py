import json
import os

# Nome do arquivo onde os dados serão salvos
DATA_FILE = "finance_data.json"

def load_data():
    """Carrega os dados do arquivo JSON ou retorna uma lista vazia."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    """Salva a lista de transações no arquivo JSON."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_transaction(data):
    """Adiciona uma nova transação (Receita ou Despesa)."""
    try:
        description = input("Descrição da transação: ")
        amount = float(input("Valor (use pontos para centavos, ex: 50.50): "))
        category = input("Categoria (Ex: Alimentação, Lazer, Salário): ")
        
        transaction = {
            "description": description,
            "amount": amount,
            "category": category
        }
        
        data.append(transaction)
        save_data(data)
        print("\n✅ Transação adicionada com sucesso!")
    except ValueError:
        print("\n❌ Erro: Por favor, insira um valor numérico válido.")

def show_balance(data):
    """Calcula e exibe o saldo total."""
    total = sum(t['amount'] for t in data)
    print(f"\n--- SALDO ATUAL: R$ {total:.2f} ---")
    
    if total < 0:
        print("Atenção: Você está no vermelho! 🚨")
    else:
        print("Tudo sob controle! 💰")

def list_transactions(data):
    """Lista todas as transações cadastradas."""
    print("\n--- HISTÓRICO DE TRANSAÇÕES ---")
    if not data:
        print("Nenhuma transação encontrada.")
        return

    for i, t in enumerate(data, 1):
        tipo = "🟢 Receita" if t['amount'] > 0 else "🔴 Despesa"
        print(f"{i}. {t['description']} | {t['category']} | {tipo}: R$ {abs(t['amount']):.2f}")

def main():
    """Função principal que roda o menu."""
    data = load_data()
    
    while True:
        print("\n--- MENU PY-FINANCE ---")
        print("1. Adicionar Transação (Use '-' para despesas)")
        print("2. Ver Saldo Atual")
        print("3. Listar Histórico")
        print("4. Sair")
        
        choice = input("Escolha uma opção: ")
        
        if choice == "1":
            add_transaction(data)
        elif choice == "2":
            show_balance(data)
        elif choice == "3":
            list_transactions(data)
        elif choice == "4":
            print("Saindo... Até logo!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()