# ==============================================================================
# COMANDOS DE TERMINAL (COPIE E COLE):
# ------------------------------------------------------------------------------
# 1. PARA RODAR O PAINEL LOCALMENTE:
#    streamlit run app.py
#
# 2. PARA EXECUTAR O BACKEND (DEV BURGUER API):
#    cd /c/dev_burguer_api
#    pnpm dev
#
# 3. PARA SUBIR ALTERAÇÕES PARA O GITHUB:
#    git add .
#    git commit -m "ajustes no layout e filtros"
#    git push origin master
# ==============================================================================

import streamlit as st
import pandas as pd
import psycopg2

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================
st.set_page_config(
    page_title="Painel ATEG",
    page_icon="🌱",
    layout="wide"
)

# =========================================
# ESTILO PERSONALIZADO (CSS)
# =========================================
st.markdown("""
<style>
/* REMOVE O TOPO (MENU, DEPLOY, GITHUB) E RODAPÉ */
header {visibility: hidden;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
div.stDeployButton {display:none;}

.stApp {
    background-color: #f4fff4;
}

/* TÍTULO */
.main-title {
    font-size: 42px;
    font-weight: bold;
    color: #146c2e;
    margin-top: 15px;
}

/* CARDS */
.card {
    background-color: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
    border-left: 8px solid #1b8f3a;
    text-align: center;
}

.card-title {
    font-size: 18px;
    color: #666666;
}

.card-value {
    font-size: 38px;
    font-weight: bold;
    color: #146c2e;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #146c2e;
}

section[data-testid="stSidebar"] * {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# TOPO DO PAINEL
# =========================================
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    st.image("https://cdn-icons-png.flaticon.com/512/628/628324.png", width=100)

with col_titulo:
    st.markdown('<p class="main-title">Painel Consolidado ATEG</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:#4b4b4b;">Indicadores gerais de técnicos, projetos e atividades</p>', unsafe_allow_html=True)

st.divider()

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
query = "SELECT supervisor_atual, tecnico, projeto, atividade FROM public.mapa_consolidado_ateg"
df = pd.read_sql(query, conn)
conn.close()

# =========================================
# KPIs E CARDS
# =========================================
col1, col2, col3, col4 = st.columns(4)
metrics = [
    ("👨‍🌾 Técnicos", df["tecnico"].nunique()),
    ("📁 Projetos", df["projeto"].nunique()),
    ("👨‍💼 Supervisores", df["supervisor_atual"].nunique()),
    ("🐄 Atividades", df["atividade"].nunique())
]

for col, (label, value) in zip([col1, col2, col3, col4], metrics):
    with col:
        st.markdown(f'<div class="card"><div class="card-title">{label}</div><div class="card-value">{value}</div></div>', unsafe_allow_html=True)

# =========================================
# SIDEBAR FILTROS (INDEPENDENTES)
# =========================================
st.sidebar.title("🌱 Filtros")

supervisor = st.sidebar.multiselect("Supervisor", options=sorted(df["supervisor_atual"].dropna().unique()))
projeto = st.sidebar.multiselect("Projeto", options=sorted(df["projeto"].dropna().unique()))
atividade = st.sidebar.multiselect("Atividade", options=sorted(df["atividade"].dropna().unique()))

# Lógica de filtragem
df_filtrado = df.copy()
if supervisor: df_filtrado = df_filtrado[df_filtrado["supervisor_atual"].isin(supervisor)]
if projeto: df_filtrado = df_filtrado[df_filtrado["projeto"].isin(projeto)]
if atividade: df_filtrado = df_filtrado[df_filtrado["atividade"].isin(atividade)]

# =========================================
# VISUALIZAÇÕES
# =========================================
st.subheader("📊 Técnicos por Projeto")
st.bar_chart(df_filtrado.groupby("projeto")["tecnico"].nunique().sort_values(ascending=False))

st.subheader("📋 Dados Consolidados")
st.dataframe(df_filtrado, use_container_width=True, height=500)

# =========================================
# RODAPÉ
# =========================================
st.divider()
st.markdown("<center><h4 style='color:#146c2e'>🌱 Painel ATEG • Streamlit + PostgreSQL</h4></center>", unsafe_allow_html=True)