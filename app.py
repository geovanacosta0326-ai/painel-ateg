import streamlit as st
import pandas as pd
import psycopg2

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="Painel ATEG",
    layout="wide"
)

st.title("📊 Painel Consolidado ATEG")

# =========================================
# CONEXÃO POSTGRES
# =========================================
conn = psycopg2.connect(
    host="177.22.38.27",
    port="6432",
    database="painel_ateg",
    user="postgres",
    password="ranes%2015"
)

# =========================================
# CONSULTA SQL
# =========================================
query = """
SELECT
    supervisor_atual,
    tecnico,
    projeto,
    atividade
FROM public.mapa_consolidado_ateg
"""

# LER DADOS
df = pd.read_sql(query, conn)

# FECHAR CONEXÃO
conn.close()

# =========================================
# KPIs
# =========================================
total_tecnicos = df["tecnico"].nunique()
total_projetos = df["projeto"].nunique()
total_supervisores = df["supervisor_atual"].nunique()
total_atividades = df["atividade"].nunique()

# =========================================
# CARDS
# =========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="👨‍🌾 Técnicos",
        value=total_tecnicos
    )

with col2:
    st.metric(
        label="📁 Projetos",
        value=total_projetos
    )

with col3:
    st.metric(
        label="👨‍💼 Supervisores",
        value=total_supervisores
    )

with col4:
    st.metric(
        label="🐄 Atividades",
        value=total_atividades
    )

st.divider()

# =========================================
# FILTROS
# =========================================
st.sidebar.title("Filtros")

supervisor = st.sidebar.multiselect(
    "Supervisor",
    options=df["supervisor_atual"].dropna().unique()
)

projeto = st.sidebar.multiselect(
    "Projeto",
    options=df["projeto"].dropna().unique()
)

atividade = st.sidebar.multiselect(
    "Atividade",
    options=df["atividade"].dropna().unique()
)

# =========================================
# APLICAR FILTROS
# =========================================
df_filtrado = df.copy()

if supervisor:
    df_filtrado = df_filtrado[
        df_filtrado["supervisor_atual"].isin(supervisor)
    ]

if projeto:
    df_filtrado = df_filtrado[
        df_filtrado["projeto"].isin(projeto)
    ]

if atividade:
    df_filtrado = df_filtrado[
        df_filtrado["atividade"].isin(atividade)
    ]

# =========================================
# TABELA
# =========================================
st.subheader("📋 Dados Consolidados")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=600
)

# =========================================
# RESUMO
# =========================================
st.subheader("📈 Resumo por Projeto")

resumo = (
    df_filtrado
    .groupby("projeto")
    .agg({
        "tecnico": "nunique"
    })
    .reset_index()
)

resumo.columns = ["Projeto", "Total Técnicos"]

st.dataframe(
    resumo,
    use_container_width=True
)