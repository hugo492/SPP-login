import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SPP - Sistema de Precificação Pro",
    page_icon="🚀",
    layout="wide"
)

# --- ESTILO CSS PERSONALIZADO (Layout Dark Moderno) ---
st.markdown("""
    <style>
    /* Fundo principal */
    .stApp {
        background-color: #0b1117;
        color: #e6edf3;
    }
    
    /* Centralização e largura do conteúdo */
    .block-container {
        max-width: 1100px !important;
        padding-top: 2rem !important;
    }

    /* Estilo dos Cards (Blocos de Input) */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }

    /* Títulos dos blocos */
    h3 {
        font-size: 1rem !important;
        color: #8b949e !important;
        text-transform: uppercase;
        margin-bottom: 15px !important;
    }

    /* Customização de Inputs e Selectbox */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #0d1117 !important;
        border: 1px solid #30363d !important;
        color: white !important;
        border-radius: 8px !important;
    }

    /* Card de Orçamento (Lateral Direita) */
    .orcamento-card {
        background-color: #101923;
        border: 1px solid #1f6feb;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
    }

    /* Botões */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS E VALIDAÇÃO
URL_PLANILHA = "SUA_URL_DA_PLANILHA_CSV_AQUI"

def verificar_acesso(email):
    if not email: return False
    try:
        df = pd.read_csv(URL_PLANILHA)
        return email.lower().strip() in df['email'].str.lower().str.strip().tolist()
    except: return False

# 3. BARRA LATERAL (LOGIN)
st.sidebar.image("https://spp.uniplenotech.com.br/wp-content/uploads/2024/02/logo-spp.png", width=150)
email_user = st.sidebar.text_input("E-mail de Compra", placeholder="exemplo@email.com")
senha_mestre = st.sidebar.text_input("Chave de Ativação", type="password")

is_admin = (email_user.lower().strip() == "hugoadm" and senha_mestre == "1920")
acesso_liberado = is_admin or (verificar_acesso(email_user) and senha_mestre == "HUGO2026")

if acesso_liberado:
    st.sidebar.success("✅ Acesso Liberado")
    
    # Cabeçalho Superior
    st.info("💡 Corpo interno sempre em branco para melhor reflexão do LED.")

    # DIVISÃO EM COLUNAS (Inputs à esquerda, Resumo à direita)
    col_main, col_summary = st.columns([2, 1], gap="large")

    with col_main:
        # Bloco 1: Texto e Dimensões
        with st.container():
            st.markdown("### 🖊️ Texto e Dimensões")
            texto_letreiro = st.text_input("Texto do Letreiro", "HUGO SANTOS").upper()
            c1, c2, c3, c4 = st.columns(4)
            c1.number_input("Nº Letras", value=10, disabled=True)
            c2.number_input("Altura (cm)", value=20)
            c3.number_input("Largura (cm)", value=15)
            c4.number_input("Profundidade (cm)", value=5)

        # Bloco 2: Localização e Impressora
        with st.container():
            st.markdown("### 📍 Localização e Impressora")
            ca, cb, cc = st.columns(3)
            ca.selectbox("Localização", ["Santa Catarina (92%)", "Bahia (105%)"])
            cb.selectbox("Marca", ["Anycubic", "Creality"])
            cc.selectbox("Modelo", ["Kobra 3 Max (550W)", "Kobra 2 Max"])

        # Bloco 3: Materiais
        with st.container():
            st.markdown("### 🧱 Materiais")
            m1, m2 = st.columns(2)
            m1.selectbox("Material da Face (50% OFF)", ["Acrílico 3mm", "Acrílico 2mm"])
            m2.selectbox("Cor da Face", ["Face Colorida (Definir)", "Face Branca"])
            m3, m4 = st.columns(2)
            m3.selectbox("Material do Fundo", ["Sem Fundo (Vazado)", "PVC 5mm"])
            m4.selectbox("Material do Corpo", ["Uso Externo (PETG c/ UV)", "PLA"])

    with col_summary:
        # Bloco de Orçamento Estilizado
        st.markdown(f"""
            <div class="orcamento-card">
                <span style="color: #58a6ff; font-weight: bold;">🏷️ VALORES PROMOCIONAIS</span>
                <h1 style="color: #58a6ff; margin: 10px 0;">R$ 659,15</h1>
                <small>Unitário: <b>R$ 65,92/Un.</b></small>
            </div>
        """, unsafe_allow_html=True)

        # Resumo Técnico
        with st.container():
            st.markdown("### 📝 Resumo")
            st.write(f"📄 **Texto:** {texto_letreiro}")
            st.write("🔢 **Letras:** 10")
            st.write("📐 **Dimensões:** 20×15×5 cm")
            
        # Botões de Ação
        st.button("🔴 Salvar PDF")
        st.button("🟢 Iniciar Produção")

else:
    st.title("🔒 SISTEMA RESTRITO")
    st.warning("Efetue o login na barra lateral para acessar a calculadora.")
