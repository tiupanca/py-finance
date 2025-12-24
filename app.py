import streamlit as st
import pandas as pd
import plotly.express as px
from database import FinanceDatabase
from datetime import datetime

# Configurações da página
st.set_page_config(page_title="PyFinance Pro v9.0", page_icon="📈", layout="wide")

db = FinanceDatabase()

st.title("📈 PyFinance - Dashboard Analítico")
st.sidebar.header("Configurações")

# --- CARREGAMENTO E TRATAMENTO DE DADOS ---
data = db.load_data()

if data:
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M')
    df['Mes_Ano'] = df['date'].dt.strftime('%m/%Y')
    
    meses_disponiveis = df['Mes_Ano'].unique()
    filtro_mes = st.sidebar.multiselect("Filtrar por Mês/Ano", options=meses_disponiveis, default=meses_disponiveis)
    df_filtrado = df[df['Mes_Ano'].isin(filtro_mes)]
else:
    df_filtrado = pd.DataFrame()

# Menu de Navegação
menu = st.sidebar.radio("Navegação", ["Painel Analítico", "Lançamentos", "Metas"])

# --- PAINEL ANALÍTICO ---
if menu == "Painel Analítico":
    if df_filtrado.empty:
        st.info("Nenhum dado encontrado. Vá em 'Lançamentos' para começar!")
    else:
        saldo = df_filtrado['amount'].sum()
        receitas = df_filtrado[df_filtrado['amount'] > 0]['amount'].sum()
        despesas = abs(df_filtrado[df_filtrado['amount'] < 0]['amount'].sum())
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Saldo no Período", f"R$ {saldo:.2f}")
        c2.metric("Entradas", f"R$ {receitas:.2f}")
        c3.metric("Saídas", f"R$ {despesas:.2f}")

        st.divider()

        col_esq, col_dir = st.columns(2)
        with col_esq:
            st.write("### 🍕 Gastos por Categoria")
            df_gastos = df_filtrado[df_filtrado['amount'] < 0].copy()
            if not df_gastos.empty:
                df_gastos['abs_amount'] = df_gastos['amount'].abs()
                fig_pie = px.pie(df_gastos, values='abs_amount', names='category', hole=.4)
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.write("Sem despesas para exibir no gráfico.")
            
        with col_dir:
            st.write("### 📉 Evolução do Saldo")
            df_timeline = df_filtrado.sort_values('date')
            df_timeline['Saldo_Acumulado'] = df_timeline['amount'].cumsum()
            fig_line = px.line(df_timeline, x='date', y='Saldo_Acumulado')
            st.plotly_chart(fig_line, use_container_width=True)

        st.write("### 📋 Transações do Período")
        # CORREÇÃO DO ERRO DO PRINT: use_container_width=True resolve o erro de 'Width: None'
        st.dataframe(df_filtrado.sort_values('date', ascending=False), use_container_width=True)

# --- LANÇAMENTOS ---
elif menu == "Lançamentos":
    st.subheader("➕ Novo Registro")
    with st.form("add_form", clear_on_submit=True):
        d1, d2 = st.columns(2)
        desc = d1.text_input("Descrição")
        valor = d2.number_input("Valor", step=0.01)
        cat = st.text_input("Categoria").capitalize()
        btn = st.form_submit_button("Salvar")
        
        if btn and desc and cat:
            db.save_data(desc, valor, cat)
            st.success("Dados salvos no SQL!")
            st.rerun()

# --- METAS (AQUI ESTÁ O QUE FALTOU!) ---
elif menu == "Metas":
    st.subheader("🎯 Gestão de Orçamento")
    
    # FORMULÁRIO PARA ADICIONAR (O que estava faltando no seu print)
    with st.expander("➕ Definir Nova Meta Orçamentária", expanded=True):
        with st.form("form_meta"):
            c1, c2 = st.columns(2)
            nova_cat = c1.text_input("Categoria (Ex: Lazer, Alimentação)")
            novo_limite = c2.number_input("Limite Mensal (R$)", min_value=0.0, step=10.0)
            if st.form_submit_button("Salvar Meta"):
                if nova_cat:
                    db.save_budgets(nova_cat.capitalize(), novo_limite)
                    st.success(f"Meta para {nova_cat} definida!")
                    st.rerun()
                else:
                    st.error("Digite uma categoria!")

    # EXIBIÇÃO DO PROGRESSO
    st.divider()
    st.write("### Progresso das Metas Atuais")
    budgets = db.load_budgets()
    report = db.get_category_report()
    
    if budgets:
        for cat, limite in budgets.items():
            # Filtra gastos apenas do mês selecionado se houver dados
            gasto_total = abs(report.get(cat, 0)) if report.get(cat, 0) < 0 else 0
            progresso = min(gasto_total / limite, 1.0) if limite > 0 else 0
            
            st.write(f"**{cat}**: R$ {gasto_total:.2f} consumidos de R$ {limite:.2f}")
            st.progress(progresso)
            if gasto_total > limite:
                st.error(f"⚠️ Alerta: Você estourou o orçamento de {cat}!")
    else:
        st.info("Nenhuma meta definida ainda. Use o campo acima para criar a primeira!")