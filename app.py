import streamlit as st
import pandas as pd
import plotly.express as px
from database import FinanceDatabase
from datetime import datetime

# Configurações da página
st.set_page_config(page_title="PyFinance Pro SQL", page_icon="💰", layout="wide")

# Inicializa o banco de dados SQL (Classe v8.0)
db = FinanceDatabase()

# Título e Barra Lateral
st.title("💰 PyFinance - Gestão Financeira com SQL")
st.sidebar.header("Menu de Navegação")
menu = st.sidebar.selectbox("Escolha uma opção", ["Painel Geral", "Adicionar Transação", "Metas e Orçamentos"])

# --- LÓGICA DO PAINEL GERAL ---
if menu == "Painel Geral":
    st.subheader("📊 Resumo Financeiro")
    
    # Busca dados atualizados do SQL
    data = db.load_data()
    saldo = db.get_balance()
    
    if not data:
        st.info("Nenhum dado registrado ainda. Vá em 'Adicionar Transação'.")
    else:
        df = pd.DataFrame(data)
        
        # Métricas em colunas
        col1, col2, col3 = st.columns(3)
        col1.metric("Saldo Total", f"R$ {saldo:.2f}")
        
        # Filtra receitas e despesas para as métricas
        receitas = df[df['amount'] > 0]['amount'].sum()
        despesas = abs(df[df['amount'] < 0]['amount'].sum())
        
        col2.metric("Total Receitas", f"R$ {receitas:.2f}")
        col3.metric("Total Despesas", f"R$ {despesas:.2f}")

        st.divider()
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("### Gastos por Categoria")
            # Gráfico apenas com valores negativos (despesas)
            df_gastos = df[df['amount'] < 0].copy()
            df_gastos['abs_amount'] = df_gastos['amount'].abs()
            fig = px.pie(df_gastos, values='abs_amount', names='category', hole=.3)
            st.plotly_chart(fig)
            
        with c2:
            st.write("### Histórico Recente (SQL)")
            # Exibe a tabela vinda do banco de dados
            st.dataframe(df, use_container_width=True)

# --- LÓGICA DE ADICIONAR ---
elif menu == "Adicionar Transação":
    st.subheader("➕ Nova Movimentação")
    with st.form("form_add"):
        desc = st.text_input("Descrição")
        valor = st.number_input("Valor (Positivo para Ganho, Negativo para Gasto)", step=0.01)
        cat = st.text_input("Categoria").capitalize()
        submit = st.form_submit_button("Salvar no Banco de Dados")
        
        if submit:
            if desc and cat:
                # SALVA DIRETO NO SQL
                db.save_data(desc, valor, cat)
                st.success(f"Sucesso! '{desc}' foi registrado no banco de dados.")
            else:
                st.error("Preencha todos os campos!")

# --- LÓGICA DE METAS ---
elif menu == "Metas e Orçamentos":
    st.subheader("🎯 Orçamentos Definidos")
    
    with st.expander("Definir Nova Meta"):
        cat_meta = st.text_input("Categoria")
        valor_meta = st.number_input("Limite Mensal", min_value=0.0)
        if st.button("Salvar Meta"):
            db.save_budgets(cat_meta.capitalize(), valor_meta)
            st.success("Meta atualizada!")

    # Carrega metas e relatório do banco
    budgets = db.load_budgets()
    report = db.get_category_report()
    
    if budgets:
        st.write("### Progresso")
        for cat, limite in budgets.items():
            # Pega o gasto total (valores negativos) para a categoria
            gasto_total = abs(report.get(cat, 0)) if report.get(cat, 0) < 0 else 0
            progresso = min(gasto_total / limite, 1.0) if limite > 0 else 0
            
            st.write(f"**{cat}**: R$ {gasto_total:.2f} de R$ {limite:.2f}")
            st.progress(progresso)