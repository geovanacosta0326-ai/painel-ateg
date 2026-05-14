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
# ESTILO PERSONALIZADO
# =========================================
st.markdown("""
<style>

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

/* SUBTÍTULO */
.subtitle {
    font-size: 18px;
    color: #4b4b4b;
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

/* TABELA */
[data-testid="stDataFrame"] {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# TOPO
# =========================================
col_logo, col_titulo = st.columns([1, 5])

with col_logo:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/628/628324.png",
        width=100
    )

with col_titulo:
    st.markdown(
        '<p class="main-title">Painel Consolidado ATEG</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Indicadores gerais de técnicos, projetos e atividades</p>',
        unsafe_allow_html=True
    )

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
query = """
SELECT
    supervisor_atual,
    tecnico,
    projeto,
    atividade
FROM public.mapa_consolidado_ateg
"""

df = pd.read_sql(query, conn)

conn.close()

# =========================================
# KPIs
# =========================================
total_tecnicos = df["tecnico"].nunique()
total_projetos = df["projeto"].nunique()
total_supervisores = df["supervisor_atual"].nunique()
total_atividades = df["atividade"].nunique()

# =========================================
# CARDS KPI
# =========================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">👨‍🌾 Técnicos</div>
        <div class="card-value">{total_tecnicos}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">📁 Projetos</div>
        <div class="card-value">{total_projetos}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">👨‍💼 Supervisores</div>
        <div class="card-value">{total_supervisores}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">🐄 Atividades</div>
        <div class="card-value">{total_atividades}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# =========================================
# SIDEBAR FILTROS
# =========================================
st.sidebar.title("🌱 Filtros")

supervisor = st.sidebar.multiselect(
    "Supervisor",
    options=sorted(df["supervisor_atual"].dropna().unique())
)

projeto = st.sidebar.multiselect(
    "Projeto",
    options=sorted(df["projeto"].dropna().unique())
)

atividade = st.sidebar.multiselect(
    "Atividade",
    options=sorted(df["atividade"].dropna().unique())
)

# =========================================
# FILTROS
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
# GRÁFICO PROJETOS
# =========================================
st.subheader("📊 Técnicos por Projeto")

grafico = (
    df_filtrado.groupby("projeto")["tecnico"]
    .nunique()
    .sort_values(ascending=False)
)

st.bar_chart(grafico)

# =========================================
# TABELA
# =========================================
st.subheader("📋 Dados Consolidados")

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=500
)

# =========================================
# RODAPÉ
# =========================================
st.divider()

st.markdown("""
<center>
    <h4 style='color:#146c2e'>
        🌱 Painel ATEG • Streamlit + PostgreSQL
    </h4>
</center>
""", unsafe_allow_html=True)