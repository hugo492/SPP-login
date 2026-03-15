import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SPP - Sistema de Precificação Pro",
    page_icon="🚀",
    layout="wide"
)

# --- ESTILO CSS (VISUAL MODERNO + REGRAS DE IMPRESSÃO) ---
st.markdown("""
    <style>
    /* Estilo para visualização no navegador */
    .stApp { background-color: #0e1117; }
    .preview-box {
        background: radial-gradient(circle, #1e293b 0%, #000000 100%);
        padding: 40px; border-radius: 15px; text-align: center;
        border: 3px solid #334155; margin-bottom: 20px;
    }
    .preview-text { font-size: 55px; font-weight: 900; color: white; text-transform: uppercase; transition: all 0.5s; }
    .led-on { text-shadow: 0 0 15px #fff, 0 0 25px #60a5fa; color: #fff; }
    .led-rgb { animation: rgbCycle 3s infinite linear; }
    
    @keyframes rgbCycle {
        0% { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
        33% { color: #00ff00; text-shadow: 0 0 15px #00ff00; }
        66% { color: #0000ff; text-shadow: 0 0 15px #0000ff; }
        100% { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
    }

    /* REGRAS DE IMPRESSÃO (PDF) */
    @media print {
        section[data-testid="stSidebar"], 
        .stButton, 
        header, 
        footer, 
        [data-testid="stToolbar"],
        .no-print {
            display: none !important;
        }
        .main .block-container {
            padding: 0 !important;
            margin: 0 !important;
        }
        .preview-box {
            background: #f0f0f0 !important;
            border: 1px solid #000 !important;
            -webkit-print-color-adjust: exact;
        }
        .preview-text {
            color: #000 !important;
            text-shadow: none !important;
        }
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
email_user = st.sidebar.text_input("E-mail de Acesso", placeholder="seu@email.com")
senha_mestre = st.sidebar.text_input("Chave de Ativação", type="password")

# Logins Prioritários
is_admin = (email_user.lower().strip() == "hugoadm" and senha_mestre == "1920")
acesso_liberado = is_admin or (verificar_acesso(email_user) and senha_mestre == "HUGO2026")

if acesso_liberado:
    st.sidebar.success("✅ Acesso Liberado")
    
    # --- PARÂMETROS DO PROJETO ---
    st.sidebar.header("📋 Dados do Orçamento")
    nome_cliente = st.sidebar.text_input("Nome do Cliente", "CLIENTE EXEMPLO")
    texto_letreiro = st.sidebar.text_input("Texto do Letreiro", "TEXTO").upper()
    
    base_regional = {
        "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "RJ - Light": [0.98, 1.02],
        "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98], "RS - Equatorial": [0.88, 1.03],
        "SC - Celesc": [0.76, 0.98], "PE - Neoenergia": [0.89, 1.08], "CE - Enel": [0.94, 1.10],
        "GO - Equatorial": [0.85, 1.02], "MT - Energisa": [0.96, 1.12], "AM - Amazonas": [1.02, 1.25],
        "PA - Equatorial": [1.05, 1.20], "DF - Neoenergia": [0.82, 1.05], "ES - EDP": [0.86, 1.01]
    }
    
    impressoras = {
        "Anycubic": [{"n": "Kobra 2 Max", "f": 1.0, "w": 500}, {"n": "Kobra 3 Max", "f": 0.95, "w": 550}],
        "Bambu Lab": [{"n": "X1-Carbon", "f": 0.85, "w": 350}, {"n": "P1S", "f": 0.88, "w": 350}],
        "Creality": [{"n": "K1 Max", "f": 0.9, "w": 1000}, {"n": "Ender 3 V3", "f": 1.1, "w": 350}]
    }

    with st.sidebar.expander("🛠️ Configuração Técnica"):
        estado = st.selectbox("Localização", options=list(base_regional.keys()))
        marca = st.selectbox("Marca da Máquina", options=list(impressoras.keys()))
        modelo = st.selectbox("Modelo", options=impressoras[marca], format_func=lambda x: x['n'])
        h = st.number_input("Altura (cm)", value=30)
        w = st.number_input("Largura (cm)", value=32)
        p = st.number_input("Profundidade (cm)", value=5)

    with st.sidebar.expander("🎨 Materiais"):
        led = st.selectbox("LED", [(0, "Sem LED"), (45, "Branco"), (75, "RGB")], format_func=lambda x: x[1])
        face = st.selectbox("Face", [(35, "Policarbonato 2mm"), (15, "Acrílico 2mm")], format_func=lambda x: x[1])
        cor_face = st.selectbox("Cor da Face", [(0, "Branca"), (20, "Colorida")], format_func=lambda x: x[1])
        fundo = st.selectbox("Fundo", [(15, "PVC 5mm"), (12, "3D Print")], format_func=lambda x: x[1])
        corpo = st.selectbox("Material Corpo", [(130, "PETG (Externo)"), (100, "PLA (Interno)")], format_func=lambda x: x[1])

    ajuste_perfil = st.sidebar.radio("Perfil", [0, -20], format_func=lambda x: "Final (100%)" if x==0 else "Terceirização (80%)")

    # 4. LÓGICA DE CÁLCULO
    qtd_letras = len(texto_letreiro.replace(" ", ""))
    kwh, mult_mat = base_regional[estado]
    
    custo_mat_base = corpo[0] * mult_mat
    preco_corpo = ((h * 2) + (w * 2)) * p * 0.17808 * modelo['f'] * (custo_mat_base / 130)
    energia = ((h + w) / 10) * modelo['f'] * (modelo['w'] / 1000) * kwh
    
    valor_unitario = (preco_corpo + (face[0] * mult_mat) + (fundo[0] * mult_mat) + led[0] + cor_face[0] + energia) * (1 + (ajuste_perfil / 100))
    total_geral = valor_unitario * qtd_letras

    # 5. ÁREA PRINCIPAL (PDF)
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    # Botão para salvar PDF (JavaScript)
    if st.sidebar.button("💾 SALVAR EM PDF / IMPRIMIR"):
        st.components.v1.html("<script>window.parent.focus(); window.parent.print();</script>", height=0)

    # Preview Visual
    estilo_neon = "led-rgb" if led[0] == 75 else ("led-on" if led[0] > 0 else "")
    st.markdown(f"""
        <div class="preview-box">
            <div class="preview-text {estilo_neon}">{texto_letreiro if texto_letreiro else "PREVIEW"}</div>
            <div style="color: #60a5fa; font-size: 12px; margin-top: 10px;">{led[1].upper()}</div>
        </div>
    """, unsafe_allow_html=True)

    col_fin, col_tec = st.columns(2)
    with col_fin:
        st.subheader("💰 Resumo Financeiro")
        st.metric("Total do Orçamento", f"R$ {total_geral:,.2f}")
        st.write(f"**Unitário:** R$ {valor_unitario:,.2f}")
        st.write(f"**Cliente:** {nome_cliente}")

    with col_tec:
        st.subheader("📋 Detalhes")
        st.write(f"• **Quantidade:** {qtd_letras} letras")
        st.write(f"• **Máquina:** {modelo['n']} | **Local:** {estado}")
        st.write(f"• **Material Corpo:** {corpo[1]}")

    st.warning("⚠️ Base orçamentária prévia. Valor final sujeito a análise técnica.")

else:
    st.title("🔒 SISTEMA RESTRITO")
    st.error("Faça login para acessar a calculadora.")
    st.sidebar.info("Acesso Administrativo: hugoadm / 1920")
