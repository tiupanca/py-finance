import streamlit as st
import pandas as pd
import plotly.express as px
from database import FinanceDatabase
from datetime import datetime

# Configurações da página
st.set_page_config(page_title="PyFinance Pro", page_icon="💰", layout="wide")

# Inicializa o banco de dados
db = FinanceDatabase()
data = db.load_data()
budgets = db.load_budgets()

# Título e Barra Lateral
st.title("💰 PyFinance - Gestão Financeira Inteligente")
st.sidebar.header("Menu de Navegação")
menu = st.sidebar.selectbox("Escolha uma opção", ["Painel Geral", "Adicionar Transação", "Metas e Orçamentos"])

# --- LÓGICA DO PAINEL GERAL ---
if menu == "Painel Geral":
    st.subheader("📊 Resumo Financeiro")
    
    if not data:
        st.info("Nenhum dado registrado ainda. Vá em 'Adicionar Transação'.")
    else:
        df = pd.DataFrame(data)
        saldo = db.get_balance(data)
        
        # Métricas em colunas
        col1, col2, col3 = st.columns(3)
        col1.metric("Saldo Total", f"R$ {saldo:.2f}")
        col2.metric("Total Receitas", f"R$ {df[df['amount'] > 0]['amount'].sum():.2f}")
        col3.metric("Total Despesas", f"R$ {abs(df[df['amount'] < 0]['amount'].sum()):.2f}")

        # Gráficos
        st.divider()
        c1, c2 = st.columns(2)
        
        with c1:
            st.write("### Gastos por Categoria")
            fig = px.pie(df[df['amount'] < 0], values=abs(df['amount']), names='category', hole=.3)
            st.plotly_chart(fig)
            
        with c2:
            st.write("### Histórico Recente")
            st.dataframe(df.sort_values(by='date', ascending=False), use_container_width=True)

# --- LÓGICA DE ADICIONAR ---
elif menu == "Adicionar Transação":
    st.subheader("➕ Nova Movimentação")
    with st.form("form_add"):
        desc = st.text_input("Descrição")
        valor = st.number_input("Valor (Negativo para despesas)", step=0.01)
        cat = st.text_input("Categoria").capitalize()
        submit = st.form_submit_button("Salvar")
        
        if submit:
            nova_t = {
                "description": desc,
                "amount": valor,
                "category": cat,
                "date": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            data.append(nova_t)
            db.save_data(data)
            st.success("Transação salva com sucesso!")

# --- LÓGICA DE METAS ---
elif menu == "Metas e Orçamentos":
    st.subheader("🎯 Suas Metas")
    with st.expander("Definir Nova Meta"):
        cat_meta = st.text_input("Categoria da Meta")
        valor_meta = st.number_input("Valor Limite", min_value=0.0)
        if st.button("Salvar Meta"):
            budgets[cat_meta.capitalize()] = valor_meta
            db.save_budgets(budgets)
            st.success(f"Meta para {cat_meta} definida!")

    st.write("### Progresso das Metas")
    if budgets:
        report = db.get_category_report(data)
        for cat, limite in budgets.items():
            gasto = abs(report.get(cat, 0))
            progresso = min(gasto / limite, 1.0) if limite > 0 else 0
            
            st.write(f"**{cat}**: R$ {gasto:.2f} / R$ {limite:.2f}")
            st.progress(progresso)
            if gasto > limite:
                st.warning(f"Você ultrapassou a meta de {cat}!")