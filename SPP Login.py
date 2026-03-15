import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SPP - Sistema de Precificação Pro",
    page_icon="🚀",
    layout="wide"
)

# --- ESTILO CSS (VISUAL DO SEU HTML ORIGINAL) ---
st.markdown("""
    <style>
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

# 3. BARRA LATERAL (LOGIN E PARÂMETROS)
st.sidebar.image("https://spp.uniplenotech.com.br/wp-content/uploads/2024/02/logo-spp.png", width=150)
email_user = st.sidebar.text_input("E-mail de Acesso", placeholder="seu@email.com")
senha_mestre = st.sidebar.text_input("Chave de Ativação", type="password")

# Logins Prioritários
is_admin = (email_user.lower().strip() == "hugoadm" and senha_mestre == "1920")
acesso_liberado = is_admin or (verificar_acesso(email_user) and senha_mestre == "HUGO2026")

if acesso_liberado:
    st.sidebar.success("✅ Acesso Liberado")
    
    st.sidebar.header("📋 Parâmetros do Projeto")
    nome_cliente = st.sidebar.text_input("Nome do Cliente", "CLIENTE EXEMPLO")
    texto_letreiro = st.sidebar.text_input("Texto do Letreiro", "TEXTO").upper()
    
    # Dados Regionais (Igual ao seu JS)
    base_regional = {
        "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "RJ - Light": [0.98, 1.02],
        "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98], "RS - Equatorial": [0.88, 1.03],
        "SC - Celesc": [0.76, 0.98], "PE - Neoenergia": [0.89, 1.08], "CE - Enel": [0.94, 1.10],
        "GO - Equatorial": [0.85, 1.02], "MT - Energisa": [0.96, 1.12], "AM - Amazonas": [1.02, 1.25],
        "PA - Equatorial": [1.05, 1.20], "DF - Neoenergia": [0.82, 1.05], "ES - EDP": [0.86, 1.01]
    }
    
    # Impressoras (Igual ao seu JS)
    impressoras = {
        "Anycubic": [{"n": "Kobra 2 Max", "f": 1.0, "w": 500}, {"n": "Kobra 3 Max", "f": 0.95, "w": 550}],
        "Bambu Lab": [{"n": "X1-Carbon", "f": 0.85, "w": 350}, {"n": "P1S", "f": 0.88, "w": 350}],
        "Creality": [{"n": "K1 Max", "f": 0.9, "w": 1000}, {"n": "Ender 3 V3", "f": 1.1, "w": 350}]
    }

    with st.sidebar.expander("🛠️ Configuração Técnica"):
        estado = st.selectbox("Localização (Custo Regional)", options=list(base_regional.keys()))
        marca = st.selectbox("Marca da Impressora", options=list(impressoras.keys()))
        modelo = st.selectbox("Modelo da Máquina", options=impressoras[marca], format_func=lambda x: x['n'])
        
        h = st.number_input("Altura (cm)", value=30)
        w = st.number_input("Largura (cm)", value=32)
        p = st.number_input("Profundidade (cm)", value=5)

    with st.sidebar.expander("🎨 Materiais e Acabamento"):
        led = st.selectbox("Iluminação LED", [(0, "Sem LED"), (45, "Branco Frio/Quente"), (75, "RGB Colorido")], format_func=lambda x: x[1])
        face = st.selectbox("Material da Face", [(35, "Policarbonato 2mm"), (15, "Acrílico 2mm"), (0, "Nenhum")], format_func=lambda x: x[1])
        cor_face = st.selectbox("Cor da Face", [(0, "Branca (Padrão)"), (20, "Colorida (+ R$ 20,00)")], format_func=lambda x: x[1])
        fundo = st.selectbox("Material do Fundo", [(15, "PVC 5mm"), (12, "3D Print"), (0, "Vazado")], format_func=lambda x: x[1])
        corpo = st.selectbox("Material do Corpo", [(130, "PETG (Externo)"), (100, "PLA (Interno)")], format_func=lambda x: x[1])

    perfil = st.sidebar.radio("Perfil de Venda", ["Cliente Final (100%)", "Terceirização (80%)"])
    ajuste_perfil = 0 if "Final" in perfil else -20

    # 4. LÓGICA DE CÁLCULO REVISADA
    qtd_letras = len(texto_letreiro.replace(" ", ""))
    kwh_local, mult_mat = base_regional[estado]
    
    # Cálculos matemáticos extraídos da sua fórmula original
    custo_mat_base = corpo[0] * mult_mat
    preco_corpo = ((h * 2) + (w * 2)) * p * 0.17808 * modelo['f'] * (custo_mat_base / 130)
    energia = ((h + w) / 10) * modelo['f'] * (modelo['w'] / 1000) * kwh_local
    
    valor_unitario = (preco_corpo + (face[0] * mult_mat) + (fundo[0] * mult_mat) + led[0] + cor_face[0] + energia) * (1 + (ajuste_perfil / 100))
    total_geral = valor_unitario * qtd_letras

    # 5. ÁREA PRINCIPAL
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    # Preview Visual
    estilo_neon = "led-rgb" if led[0] == 75 else ("led-on" if led[0] > 0 else "")
    st.markdown(f"""
        <div class="preview-box">
            <div class="preview-text {estilo_neon}">{texto_letreiro if texto_letreiro else "PREVIEW"}</div>
            <div style="color: #60a5fa; font-size: 12px; margin-top: 10px;">{led[1].upper()}</div>
        </div>
    """, unsafe_allow_html=True)

    # Painel de Resultados
    col_fin, col_tec = st.columns(2)
    
    with col_fin:
        st.subheader("💰 Resumo Financeiro")
        st.metric("Total do Orçamento", f"R$ {total_geral:,.2f}")
        st.write(f"**Valor por Letra:** R$ {valor_unitario:,.2f}")
        st.write(f"**Orçamento para:** {nome_cliente}")
        st.info("💡 Corpo interno em branco para máxima reflexão.")

    with col_tec:
        st.subheader("📋 Detalhamento")
        st.write(f"• **Quantidade:** {qtd_letras} letras")
        st.write(f"• **Dimensões:** {h}cm x {w}cm x {p}cm")
        st.write(f"• **Região:** {estado}")
        st.write(f"• **Máquina:** {modelo['n']}")

    st.warning("⚠️ Nota: Base orçamentária prévia. Valor final após análise do arquivo técnico.")

else:
    # TELA DE BLOQUEIO
    st.title("🔒 SISTEMA RESTRITO")
    st.error("Acesso não autorizado. Verifique seu e-mail e chave de ativação.")
    st.write("---")
    st.markdown("### Não tem uma conta? [Assine o SPP PRO](https://spp.uniplenotech.com.br/)")
    st.sidebar.info("Dúvidas? Entre em contato com o suporte.")
