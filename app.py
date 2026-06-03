import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
import time

# Configuração da página
st.set_page_config(
    page_title="Inteligência Eleitoral",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar variáveis de ambiente
load_dotenv()

# Estilo CSS customizado
st.markdown("""
<style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        background-color: #0ea5e9;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0284c7;
    }
    .metric-card {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #0ea5e9;
    }
    .metric-label {
        font-size: 1rem;
        color: #64748b;
    }
</style>
""", unsafe_allow_html=True)

# Função para conectar ao banco
@st.cache_resource
def init_connection():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return None
    try:
        engine = create_engine(db_url)
        return engine
    except Exception as e:
        st.error(f"Erro ao conectar ao banco: {e}")
        return None

# Função para executar query
@st.cache_data(ttl=600)
def run_query(query, params=None):
    engine = init_connection()
    if not engine:
        return pd.DataFrame()
    try:
        df = pd.read_sql(query, engine, params=params)
        return df
    except Exception as e:
        st.error(f"Erro ao executar query: {e}")
        return pd.DataFrame()

# Autenticação (Simulada para MVP)
def login():
    st.sidebar.title("🔐 Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Senha", type="password")
    
    if st.sidebar.button("Entrar"):
        if email == "admin@demo.com" and password == "admin123":
            st.session_state["authenticated"] = True
            st.session_state["user"] = "Admin Demo"
            st.session_state["tenant_id"] = 1
            st.sidebar.success("Login realizado com sucesso!")
            time.sleep(1)
            st.rerun()
        else:
            st.sidebar.error("Email ou senha incorretos.")

def logout():
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["tenant_id"] = None
    st.rerun()

# Inicializar estado da sessão
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Lógica Principal
if not st.session_state["authenticated"]:
    st.title("📊 Inteligência Eleitoral")
    st.markdown("Bem-vindo à plataforma de inteligência eleitoral. Por favor, faça login para continuar.")
    
    # Mostrar dashboard de exemplo
    st.markdown("### Exemplo de Dashboard")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">184</div><div class="metric-label">Municípios Mapeados</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">7</div><div class="metric-label">Eleições (1998-2022)</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">50k+</div><div class="metric-label">Candidatos Analisados</div></div>', unsafe_allow_html=True)
    
    login()
else:
    # Sidebar
    st.sidebar.title(f"Bem-vindo, {st.session_state['user']}")
    menu = st.sidebar.radio("Navegação", ["Dashboard", "Busca de Candidatos", "Análise Geográfica", "Relatórios"])
    
    if st.sidebar.button("Sair"):
        logout()
    
    # Conteúdo Principal
    if menu == "Dashboard":
        st.title("📈 Dashboard Geral")
        
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            ano = st.selectbox("Ano da Eleição", [2022, 2020, 2018, 2016, 2014, 2012, 2010, 2008, 2006, 2004, 2002, 2000, 1998])
        with col2:
            cargo = st.selectbox("Cargo", ["Governador", "Senador", "Deputado Federal", "Deputado Estadual", "Prefeito", "Vereador"])
        
        # Métricas
        st.markdown("### Resumo Estadual")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Eleitores Aptos", "7.1M", "+2.3%")
        with col2:
            st.metric("Comparecimento", "82.5%", "-1.2%")
        with col3:
            st.metric("Votos Válidos", "5.8M", "+4.5%")
        with col4:
            st.metric("Abstenção", "17.5%", "+1.2%")
            
        # Gráficos de exemplo (usando dados mockados se banco não estiver conectado)
        st.markdown("### Evolução de Votos")
        
        # Dados mockados para demonstração
        df_mock = pd.DataFrame({
            "Ano": [2010, 2014, 2018, 2022],
            "Partido A": [1.2, 1.5, 1.8, 2.1],
            "Partido B": [1.8, 1.6, 1.4, 1.2],
            "Partido C": [0.5, 0.8, 1.2, 1.5]
        })
        
        fig = px.line(df_mock, x="Ano", y=["Partido A", "Partido B", "Partido C"], 
                      title="Evolução de Votos por Partido (Milhões)",
                      markers=True)
        st.plotly_chart(fig, use_container_width=True)
        
    elif menu == "Busca de Candidatos":
        st.title("🔍 Busca de Candidatos")
        
        busca = st.text_input("Nome ou CPF do candidato")
        
        if busca:
            st.info(f"Buscando por: {busca}...")
            # Aqui entraria a query real
            
            # Dados mockados
            df_resultados = pd.DataFrame({
                "Nome": ["João da Silva", "Maria Oliveira", "José Santos"],
                "Cargo": ["Deputado Estadual", "Deputado Federal", "Senador"],
                "Partido": ["PT", "PSDB", "MDB"],
                "Votos (2022)": [45000, 85000, 1200000],
                "Situação": ["Eleito", "Suplente", "Não Eleito"]
            })
            
            st.dataframe(df_resultados, use_container_width=True)
            
    elif menu == "Análise Geográfica":
        st.title("🗺️ Análise Geográfica")
        
        st.markdown("### Distribuição de Votos em Pernambuco")
        
        # Mapa mockado
        st.info("Mapa interativo de Pernambuco será renderizado aqui com os dados reais do banco.")
        
        # Exemplo de gráfico de barras
        df_mun = pd.DataFrame({
            "Município": ["Recife", "Jaboatão", "Olinda", "Caruaru", "Petrolina"],
            "Votos": [850000, 320000, 210000, 180000, 160000]
        })
        
        fig_bar = px.bar(df_mun, x="Município", y="Votos", title="Top 5 Municípios por Votos")
        st.plotly_chart(fig_bar, use_container_width=True)
        
    elif menu == "Relatórios":
        st.title("📄 Relatórios")
        
        st.markdown("### Gerar Relatório Consolidado")
        
        tipo = st.selectbox("Tipo de Relatório", ["Análise de Desempenho", "Perfil Demográfico", "Vulnerabilidade Eleitoral"])
        municipio = st.selectbox("Município Alvo", ["Todos", "Recife", "Jaboatão", "Olinda"])
        
        if st.button("Gerar PDF"):
            st.success("Relatório gerado com sucesso! Iniciando download...")
