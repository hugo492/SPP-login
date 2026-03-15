import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SPP - Sistema de Precificação Pro",
    page_icon="🚀",
    layout="wide"
)

# --- ESTILO CSS (Layout Dark Moderno conforme a imagem) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b1117; color: #e6edf3; }
    .block-container { max-width: 1100px !important; padding-top: 2rem !important; }
    
    /* Estilo dos Cards de Input */
    div[data-testid="stVerticalBlock"] > div:has(div.stMarkdown) {
        background-color: #161b22;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #30363d;
        margin-bottom: 15px;
    }

    h3 { font-size: 1rem !important; color: #8b949e !important; text-transform: uppercase; margin-bottom: 15px !important; }

    /* Card de Orçamento Lateral */
    .orcamento-card {
        background-color: #101923;
        border: 1px solid #1f6feb;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
    }

    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    
    /* Regras para Impressão PDF */
    @media print {
        section[data-testid="stSidebar"], .stButton, header, footer, [data-testid="stToolbar"] { display: none !important; }
        .block-container { max-width: 100% !important; margin: 0 !important; }
        .orcamento-card { border: 2px solid #000 !important; color: #000 !important; background: white !important; }
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
    
    # DICIONÁRIO COMPLETO DE ESTADOS (ADICIONADOS OS QUE FALTAVAM)
    base_regional = {
        "AC - Energisa": [1.05, 1.30], "AL - Equatorial": [0.94, 1.10], "AM - Amazonas": [1.02, 1.25],
        "AP - CEA": [0.98, 1.15], "BA - Coelba": [0.92, 1.05], "CE - Enel": [0.94, 1.10],
        "DF - Neoenergia": [0.82, 1.05], "ES - EDP": [0.86, 1.01], "GO - Equatorial": [0.85, 1.02],
        "MA - Equatorial": [0.96, 1.15], "MG - Cemig": [0.91, 1.00], "MS - Energisa": [0.93, 1.08],
        "MT - Energisa": [0.96, 1.12], "PA - Equatorial": [1.05, 1.20], "PB - Energisa": [0.88, 1.08],
        "PE - Neoenergia": [0.89, 1.08], "PI - Equatorial": [0.95, 1.12], "PR - Copel": [0.78, 0.98],
        "RJ - Light": [0.98, 1.02], "RN - Neoenergia": [0.87, 1.08], "RO - Energisa": [0.99, 1.20],
        "RR - Roraima": [1.08, 1.40], "RS - Equatorial": [0.88, 1.03], "SC - Celesc": [0.76, 0.98],
        "SE - Energisa": [0.89, 1.10], "SP - Enel": [0.84, 1.00], "TO - Energisa": [0.96, 1.15]
    }

    impressoras = {
        "Anycubic": [{"n": "Kobra 3 Max", "f": 0.95, "w": 550}, {"n": "Kobra 2 Max", "f": 1.0, "w": 500}],
        "Creality": [{"n": "K1 Max", "f": 0.9, "w": 1000}, {"n": "Ender 3 V3", "f": 1.1, "w": 350}]
    }

    # CONTEÚDO PRINCIPAL
    st.info("💡 Corpo interno sempre em branco para melhor reflexão do LED.")
    col_main, col_summary = st.columns([2, 1], gap="large")

    with col_main:
        # Bloco 1: Texto e Dimensões
        with st.container():
            st.markdown("### 🖊️ Texto e Dimensões")
            texto_letreiro = st.text_input("Texto do Letreiro", "TEXTO EXEMPLO").upper()
            qtd_letras = len(texto_letreiro.replace(" ", ""))
            c1, c2, c3, c4 = st.columns(4)
            c1.number_input("Nº Letras", value=qtd_letras, disabled=True)
            h = c2.number_input("Altura (cm)", value=30)
            w = c3.number_input("Largura (cm)", value=32)
            p = c4.number_input("Profundidade (cm)", value=5)

        # Bloco 2: Localização e Máquina
        with st.container():
            st.markdown("### 📍 Localização e Impressora")
            ca, cb, cc = st.columns(3)
            estado_sel = ca.selectbox("Localização", options=list(base_regional.keys()))
            marca_sel = cb.selectbox("Marca", options=list(impressoras.keys()))
            modelo_sel = cc.selectbox("Modelo", options=impressoras[marca_sel], format_func=lambda x: x['n'])

        # Bloco 3: Materiais
        with st.container():
            st.markdown("### 🧱 Materiais")
            m1, m2 = st.columns(2)
            face_val = m1.selectbox("Material da Face", [(35, "Policarbonato 2mm"), (15, "Acrílico 2mm")], format_func=lambda x: x[1])
            cor_face_val = m2.selectbox("Cor da Face", [(0, "Branca"), (20, "Colorida")], format_func=lambda x: x[1])
            m3, m4 = st.columns(2)
            fundo_val = m3.selectbox("Material do Fundo", [(15, "PVC 5mm"), (0, "Vazado")], format_func=lambda x: x[1])
            corpo_val = m4.selectbox("Material Corpo", [(130, "PETG (UV)"), (100, "PLA")], format_func=lambda x: x[1])

    # CÁLCULOS
    kwh, mult_mat = base_regional[estado_sel]
    custo_mat_base = corpo_val[0] * mult_mat
    preco_corpo = ((h * 2) + (w * 2)) * p * 0.17808 * modelo_sel['f'] * (custo_mat_base / 130)
    energia = ((h + w) / 10) * modelo_sel['f'] * (modelo_sel['w'] / 1000) * kwh
    
    valor_unit = (preco_corpo + (face_val[0] * mult_mat) + (fundo_val[0] * mult_mat) + cor_face_val[0] + energia)
    total_geral = valor_unit * qtd_letras

    with col_summary:
        st.markdown(f"""
            <div class="orcamento-card">
                <span style="color: #58a6ff; font-weight: bold;">🏷️ ORÇAMENTO ESTIMADO</span>
                <h1 style="color: #58a6ff; margin: 10px 0;">R$ {total_geral:,.2f}</h1>
                <small>Unitário: <b>R$ {valor_unit:,.2f}/Un.</b></small>
            </div>
        """, unsafe_allow_html=True)

        with st.container():
            st.markdown("### 📝 Resumo Técnico")
            st.write(f"🔢 **Letras:** {qtd_letras}")
            st.write(f"📐 **Medidas:** {h}x{w}x{p} cm")
            st.write(f"📍 **Tarifa:** {estado_sel} (R$ {kwh})")

        if st.button("💾 GERAR PDF / IMPRIMIR"):
            st.components.v1.html("<script>window.parent.focus(); window.parent.print();</script>", height=0)

else:
    st.title("🔒 SISTEMA RESTRITO")
    st.warning("Efetue o login na lateral.")
