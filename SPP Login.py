import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SPP - Sistema de Precificação Pro",
    page_icon="🚀",
    layout="wide"  # Mantemos wide para controlar a largura via CSS
)

# --- ESTILO CSS PARA CENTRALIZAR TUDO ---
st.markdown("""
    <style>
    /* Fundo e Centralização do Bloco Principal */
    .stApp { 
        background-color: #0e1117; 
    }
    
    /* Limita a largura do conteúdo e centraliza no meio da tela */
    .block-container {
        max-width: 900px !important;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
    }

    /* Estilo dos Blocos (Cards) */
    .css-1r6slb0, .stVerticalBlock {
        background-color: #161b22;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #30363d;
        margin-bottom: 20px;
    }

    /* Preview Neon */
    .preview-box {
        background: radial-gradient(circle, #1e293b 0%, #000000 100%);
        padding: 50px 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #30363d;
        margin-bottom: 25px;
    }
    .preview-text { font-size: 60px; font-weight: 900; color: white; text-transform: uppercase; }
    .led-on { text-shadow: 0 0 15px #fff, 0 0 25px #60a5fa; color: #fff; }
    .led-rgb { animation: rgbCycle 3s infinite linear; }
    
    @keyframes rgbCycle {
        0% { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
        33% { color: #00ff00; text-shadow: 0 0 15px #00ff00; }
        66% { color: #0000ff; text-shadow: 0 0 15px #0000ff; }
        100% { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
    }

    /* REGRAS DE IMPRESSÃO */
    @media print {
        section[data-testid="stSidebar"], .stButton, header, footer, [data-testid="stToolbar"] {
            display: none !important;
        }
        .block-container { max-width: 100% !important; margin: 0 !important; }
        .preview-box { background: white !important; border: 1px solid #000 !important; -webkit-print-color-adjust: exact; }
        .preview-text { color: black !important; text-shadow: none !important; }
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

# 3. BARRA LATERAL (CONTROLADORES)
st.sidebar.image("https://spp.uniplenotech.com.br/wp-content/uploads/2024/02/logo-spp.png", width=150)
email_user = st.sidebar.text_input("E-mail", placeholder="seu@email.com")
senha_mestre = st.sidebar.text_input("Chave", type="password")

is_admin = (email_user.lower().strip() == "hugoadm" and senha_mestre == "1920")
acesso = is_admin or (verificar_acesso(email_user) and senha_mestre == "HUGO2026")

if acesso:
    st.sidebar.success("✅ Acesso Liberado")
    
    # Inputs na Sidebar para não poluir o meio da tela
    nome_cliente = st.sidebar.text_input("Cliente", "HUGO LETRA CAIXA PRO")
    texto_letreiro = st.sidebar.text_input("Texto", "TEXTO").upper()
    
    with st.sidebar.expander("🛠️ Técnica"):
        h = st.number_input("Altura (cm)", value=30)
        w = st.number_input("Largura (cm)", value=32)
        p = st.number_input("Profundidade (cm)", value=5)
        led_val = st.selectbox("LED", [(0, "Sem LED"), (45, "Branco"), (75, "RGB")], format_func=lambda x: x[1])
        corpo_val = st.selectbox("Material", [(130, "PETG"), (100, "PLA")], format_func=lambda x: x[1])

    if st.sidebar.button("💾 GERAR PDF / IMPRIMIR"):
        st.components.v1.html("<script>window.parent.focus(); window.parent.print();</script>", height=0)

    # 4. CONTEÚDO CENTRALIZADO (ESTRUTURA EM BLOCOS)
    st.markdown(f"<h1 style='text-align: center; color: white;'>🚀 SPP - PRECIFICAÇÃO PRO</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #94a3b8;'>Orçamento para: <b>{nome_cliente}</b></p>", unsafe_allow_html=True)

    # Bloco 1: Preview
    estilo = "led-rgb" if led_val[0] == 75 else ("led-on" if led_val[0] > 0 else "")
    st.markdown(f"""
        <div class="preview-box">
            <div class="preview-text {estilo}">{texto_letreiro if texto_letreiro else "PREVIEW"}</div>
        </div>
    """, unsafe_allow_html=True)

    # Bloco 2: Resultados em Colunas
    col1, col2 = st.columns(2)
    
    # Cálculos Simples (Baseados na sua lógica)
    qtd = len(texto_letreiro.replace(" ", ""))
    valor_unit = ( ( (h*2)+(w*2) ) * p * 0.17808 ) + led_val[0] + corpo_val[0]
    total = valor_unit * qtd

    with col1:
        st.markdown("### 💰 Financeiro")
        st.metric("Total Geral", f"R$ {total:,.2f}")
        st.write(f"**Unitário:** R$ {valor_unit:,.2f}")

    with col2:
        st.markdown("### 📋 Resumo")
        st.write(f"• **Letras:** {qtd}")
        st.write(f"• **Medidas:** {h}x{w}x{p} cm")
        st.write(f"• **Material:** {corpo_val[1]}")

    st.markdown("---")
    st.warning("⚠️ Valor sujeito a alteração após análise do arquivo vetorial.")

else:
    st.markdown("<h1 style='text-align: center;'>🔒 ACESSO RESTRITO</h1>", unsafe_allow_html=True)
    st.info("Insira as suas credenciais na barra lateral para aceder ao sistema.")
