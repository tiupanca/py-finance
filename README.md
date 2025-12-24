# 💰 PyFinance Pro - Dashboard Financeiro Inteligente

O **PyFinance** evoluiu de um simples script de terminal para uma aplicação web completa. É uma ferramenta de gestão financeira que permite o controle total de gastos, receitas e definição de metas orçamentárias, utilizando uma arquitetura profissional e visualização de dados moderna.

---

## ✨ Funcionalidades (v7.0)

* **Interface Web Interativa:** Dashboard moderno desenvolvido com Streamlit para uma experiência de usuário fluida e visual.
* **Visualização de Dados:** Gráficos dinâmicos e interativos que mostram a distribuição de gastos por categoria.
* **Gestão de Metas (Budgets):** Definição de limites mensais com barras de progresso que mostram o consumo do orçamento em tempo real.
* **Sistema CRUD Completo:** Capacidade de Adicionar, Listar, Editar e Excluir transações de forma simples.
* **Exportação de Relatórios:** Geração de arquivos CSV formatados especificamente para abertura no Microsoft Excel ou Google Sheets.
* **Arquitetura Profissional:** Construído com Programação Orientada a Objetos (POO), facilitando a manutenção e futuras expansões.

---

## 🏗️ Estrutura do Software

O projeto foi organizado seguindo o princípio de separação de responsabilidades:

1. **database.py**: O cérebro do projeto. Contém a classe `FinanceDatabase` que gerencia a persistência de dados em arquivos JSON e os cálculos matemáticos.
2. **app.py**: A face do projeto. Gerencia a interface web, os gráficos e a interação direta com o usuário.
3. **finance.py**: Versão clássica via terminal, mantida para testes e operações rápidas via linha de comando.

---

## 🛠️ Tecnologias e Ferramentas

* **Linguagem:** Python 3.10+
* **Framework Web:** Streamlit
* **Bibliotecas de Dados:** Pandas e Plotly
* **Estilização:** Colorama (para a versão terminal)
* **Armazenamento:** JSON (Banco de dados local em formato de arquivo)

---

## 📦 Como Instalar e Executar

Siga os passos abaixo para rodar o projeto na sua máquina:

### 1. Clonar o Repositório
Baixe os arquivos do projeto para sua máquina local através do Git.

### 2. Instalar as Dependências
Você precisará das bibliotecas básicas. No terminal, execute:
pip install streamlit pandas plotly colorama

### 3. Executar a Aplicação
Para iniciar o servidor web do projeto, utilize o comando:
**streamlit run app.py**

### 4. Acessar o Sistema
O Dashboard abrirá automaticamente no seu navegador padrão (geralmente em http://localhost:8501).

---

## 🚀 Próximos Passos no Desenvolvimento

- [ ] Implementação de sistema de login e proteção de dados por usuário.
- [ ] Migração do sistema de arquivos JSON para um banco de dados SQL (SQLite).
- [ ] Criação de filtros inteligentes por datas e períodos específicos.
- [ ] Integração com inteligência artificial para previsão de gastos futuros.

## 👤 Autor


- GitHub: [@tiupanca](https://github.com/tiupanca)
- LinkedIn: [André Sarmento](https://linkedin.com/in/alsod)
- Website: [GTABRASIL](https://gtabrasil.com)