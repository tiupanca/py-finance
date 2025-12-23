# 💰 PyFinance - Gerenciador de Finanças Pessoais

O **PyFinance** é uma aplicação de linha de comando (CLI) desenvolvida em Python para auxiliar no controle financeiro diário. O projeto permite registrar receitas e despesas, visualizar o saldo total e manter um histórico persistente através de arquivos JSON.

Este projeto foi construído para demonstrar conceitos fundamentais de lógica de programação, manipulação de arquivos e estruturação de software de forma limpa e organizada.

---

## ✨ Funcionalidades

- **Registro de Movimentações:** Adicione entradas (valores positivos) e saídas (valores negativos) com descrição e categoria.
- **Cálculo de Saldo em Tempo Real:** Monitoramento constante do status financeiro (com alertas visuais caso o saldo esteja negativo).
- **Persistência de Dados:** Todos os dados são salvos em um arquivo `json`, permitindo que as informações sejam mantidas mesmo após fechar o programa.
- **Listagem Detalhada:** Interface limpa para visualizar o histórico de transações categorizadas.

## ✨ Funcionalidades (v2.0)

- **Interface Colorida:** Uso da biblioteca `colorama` para feedback visual (Verde para receitas, Vermelho para despesas).
- **Data e Hora Automática:** Registro preciso de quando cada transação foi realizada.
- **Registro de Movimentações:** Adicione entradas e saídas com descrição e categoria.
- **Persistência de Dados:** Histórico salvo em JSON.

## ✨ Funcionalidades (v3.0 - Full CRUD)

- **[C]reate:** Adição de transações com data automática e categorias.
- **[R]ead:** Visualização de histórico detalhado e relatórios por categoria.
- **[U]pdate:** Edição inteligente de registros existentes (com preservação de dados).
- **[D]elete:** Remoção de registros por ID.
- **Feedback Visual:** Interface colorida com `colorama` para melhor legibilidade.
- **Persistência Local:** Armazenamento robusto em JSON.
- **Exportação de Dados:** Gera arquivos `.csv` formatados para abertura direta no Microsoft Excel ou Google Sheets (v5.0).

## 🛠️ Tecnologias Utilizadas

- **Linguagem:** [Python 3.10+](https://www.python.org/)
- **Armazenamento:** JSON (JavaScript Object Notation)
- **Bibliotecas Nativas:** `json` (manipulação de dados) e `os` (interação com o sistema operacional)

## 🏗️ Arquitetura do Projeto

O sistema foi refatorado seguindo princípios de **Separação de Responsabilidades**:
- `finance.py`: Camada de Interface (View) - Lida com a interação com o usuário.
- `database.py`: Camada de Dados (Model) - Lida com leitura, escrita e lógica de cálculo.

## 📦 Como Rodar o Projeto

Siga os passos abaixo para executar a aplicação em sua máquina local:

1. **Certifique-se de ter o Python instalado:**
   Você pode verificar digitando `python --version` no seu terminal.

2. **Clone este repositório:**
   
   `git clone https://github.com/tiupanca/py-finance.git`


3. **Acesse a pasta do projeto:**
   
   `cd py-finance`

4. **Instale as dependências:**

    `pip install colorama`

5. **Execute o programa:**
   
   `python finance.py`

## 🧠 Aprendizados e Desafios

Durante o desenvolvimento deste projeto, apliquei boas práticas de desenvolvimento:

- **Modularização:**  Código dividido em funções específicas, facilitando a manutenção.
- **Tratamento de Erros:**  Uso de blocos try/except para lidar com entradas inválidas.
- **Trabalho com JSON:**  Conversão de dados Python para persistência local.
- **Git & GitHub:**  Fluxo de trabalho com commits organizados e README profissional.
- **Evolução de Software:** Como manter a compatibilidade de dados ao adicionar novas colunas em um sistema já existente.
- **Experiência do Usuário (UX):** Uso de cores no terminal para facilitar a leitura de dados financeiros.
- **Manipulação de Datas:** Uso da biblioteca `datetime` para formatação de logs.

## 👤 Autor


- GitHub: [@tiupanca](https://github.com/tiupanca)
- LinkedIn: [André Sarmento](https://linkedin.com/in/alsod)
- Website: [GTABRASIL](https://gtabrasil.com)