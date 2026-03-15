import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SPP - Sistema de Precificação Pro",
    page_icon="🚀",
    layout="wide"
)

# --- ESTILO CSS (Layout Dark Moderno - Centralizado) ---
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

    h3 { font-size: 1rem !important; color: #8b949e !important; text-transform: uppercase; margin-bottom: 10px !important; }

    /* Card de Orçamento Lateral */
    .orcamento-card {
        background-color: #101923;
        border: 1px solid #1f6feb;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
    }

    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; background-color: #238636; color: white; border: none; }
    
    /* Regras para Impressão PDF */
    @media print {
        section[data-testid="stSidebar"], .stButton, header, footer, [data-testid="stToolbar"] { display: none !important; }
        .block-container { max-width: 100% !important; margin: 0 !important; }
        .orcamento-card { border: 2px solid #000 !important; color: #000 !important; background: white !important; -webkit-print-color-adjust: exact; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS E VALIDAÇÃO (LOGIN)
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
    
    # DICIONÁRIO COMPLETO DE IMPRESSORAS
    impressoras = {
        "Anycubic": [
            {"n": "Kobra 3 Max", "f": 0.95, "w": 550},
            {"n": "Kobra 2 Max", "f": 1.0, "w": 500},
            {"n": "Kobra 2 Plus", "f": 1.05, "w": 450}
        ],
        "Bambu Lab": [
            {"n": "X1-Carbon", "f": 0.85, "w": 350},
            {"n": "P1S", "f": 0.88, "w": 350},
            {"n": "A1", "f": 0.92, "w": 300}
        ],
        "Creality": [
            {"n": "K1 Max", "f": 0.9, "w": 1000},
            {"n": "Ender 3 V3", "f": 1.1, "w": 350}
        ],
        "Elegoo": [
            {"n": "Neptune 4 Max", "f": 0.95, "w": 500},
            {"n": "Neptune 4 Plus", "f": 0.98, "w": 480}
        ]
    }

    # CONTEÚDO PRINCIPAL (LAYOUT EM BLOCOS)
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

        # Bloco 2: Configuração da Máquina
        with st.container():
            st.markdown("### ⚙️ Impressora 3D")
            cb, cc = st.columns(2)
            marca_sel = cb.selectbox("Marca", options=list(impressoras.keys()))
            modelo_sel = cc.selectbox("Modelo", options=impressoras[marca_sel], format_func=lambda x: f"{x['n']} ({x['w']}W)")

        # Bloco 3: Materiais
        with st.container():
            st.markdown("### 🧱 Materiais e Acabamento")
            m1, m2 = st.columns(2)
            face_val = m1.selectbox("Material da Face", [(35, "Policarbonato 2mm"), (15, "Acrílico 2mm")], format_func=lambda x: x[1])
            cor_face_val = m2.selectbox("Cor da Face", [(0, "Branca"), (20, "Colorida")], format_func=lambda x: x[1])
            m3, m4 = st.columns(2)
            fundo_val = m3.selectbox("Material do Fundo", [(15, "PVC 5mm"), (0, "Vazado")], format_func=lambda x: x[1])
            corpo_val = m4.selectbox("Material Corpo", [(130, "PETG (UV)"), (100, "PLA")], format_func=lambda x: x[1])

    # 4. LÓGICA DE CÁLCULO (Sem Localização - Valores Base Fixos)
    custo_kwh_base = 0.85  # Valor médio de energia
    mult_material_base = 1.0  # Multiplicador base de material
    
    custo_mat_final = corpo_val[0] * mult_material_base
    preco_corpo = ((h * 2) + (w * 2)) * p * 0.17808 * modelo_sel['f'] * (custo_mat_final / 130)
    energia = ((h + w) / 10) * modelo_sel['f'] * (modelo_sel['w'] / 1000) * custo_kwh_base
    
    valor_unitario = (preco_corpo + (face_val[0] * mult_material_base) + (fundo_val[0] * mult_material_base) + cor_face_val[0] + energia)
    total_geral = valor_unitario * qtd_letras

    with col_summary:
        # Card de Orçamento
        st.markdown(f"""
            <div class="orcamento-card">
                <span style="color: #58a6ff; font-weight: bold; font-size: 0.9rem;">🏷️ ORÇAMENTO TOTAL</span>
                <h1 style="color: #58a6ff; margin: 10px 0; font-size: 2.5rem;">R$ {total_geral:,.2f}</h1>
                <p style="margin: 0;">Unitário: <b>R$ {valor_unitario:,.2f}/Un.</b></p>
            </div>
        """, unsafe_allow_html=True)

        # Resumo Técnico
        with st.container():
            st.markdown("### 📝 Resumo")
            st.write(f"🔢 **Letras:** {qtd_letras}")
            st.write(f"📐 **Medidas:** {h}x{w}x{p} cm")
            st.write(f"⚙️ **Máquina:** {modelo_sel['n']}")
            st.write(f"🧱 **Corpo:** {corpo_val[1]}")

        # Botão de Impressão
        if st.button("💾 GERAR PDF / IMPRIMIR"):
            st.components.v1.html("<script>window.parent.focus(); window.parent.print();</script>", height=0)

else:
    st.title("🔒 SISTEMA RESTRITO")
    st.error("Acesso bloqueado. Verifique suas credenciais na barra lateral.")
    st.sidebar.info("Acesso Admin: hugoadm / 1920")
