import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA E ESTILO
st.set_page_config(page_title="SPP - Precificação Pro", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .preview-box {
        background: radial-gradient(circle, #1e293b 0%, #000000 100%);
        padding: 40px; border-radius: 15px; text-align: center;
        border: 3px solid #334155; margin-bottom: 20px;
    }
    .preview-text { font-size: 50px; font-weight: 900; color: white; text-transform: uppercase; }
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

# 2. BANCO DE DADOS E VALIDAÇÃO (LOGIN)
URL_PLANILHA = "SUA_URL_DA_PLANILHA_CSV_AQUI"

def verificar_acesso(email):
    if not email: return False
    try:
        df = pd.read_csv(URL_PLANILHA)
        return email.lower().strip() in df['email'].str.lower().str.strip().tolist()
    except: return False

# 3. BARRA LATERAL (LOGIN E INPUTS)
st.sidebar.image("https://spp.uniplenotech.com.br/wp-content/uploads/2024/02/logo-spp.png", width=150)
email_user = st.sidebar.text_input("E-mail", placeholder="seu@email.com")
senha_mestre = st.sidebar.text_input("Chave", type="password")

# Login de Admin fixo e Verificação de Assinante
is_admin = (email_user.lower().strip() == "hugoadm" and senha_mestre == "1920")
acesso = is_admin or (verificar_acesso(email_user) and senha_mestre == "HUGO2026")

if acesso:
    st.sidebar.success("✅ Acesso Liberado")
    
    # --- INPUTS TÉCNICOS ---
    st.sidebar.header("📋 Dados do Projeto")
    nome_cliente = st.sidebar.text_input("Cliente/Empresa", "HUGO LETRA CAIXA PRO")
    texto = st.sidebar.text_input("Texto do Letreiro", "TEXTO").upper()
    
    with st.sidebar.expander("📏 Dimensões e LED"):
        h = st.number_input("Altura (cm)", value=30)
        w = st.number_input("Largura (cm)", value=32)
        p = st.number_input("Profundidade (cm)", value=5)
        led_tipo = st.selectbox("Iluminação", [(0, "Sem LED"), (45, "Branco"), (75, "RGB")], format_func=lambda x: x[1])

    with st.sidebar.expander("🏗️ Materiais e Regional"):
        estado = st.selectbox("Sua Região", ["BA - Coelba", "SP - Enel", "RJ - Light", "MG - Cemig"])
        # Lógica de custos regionais simplificada
        custos_regiao = {"BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00]}
        kwh, mult_mat = custos_regiao.get(estado, [0.90, 1.00])
        
        face = st.selectbox("Face", [(35, "Policarbonato 2mm"), (15, "Acrílico 2mm")], format_func=lambda x: x[1])
        cor_face = st.selectbox("Cor da Face", [(0, "Branca (Padrão)"), (20, "Colorida (+R$20)")], format_func=lambda x: x[1])
        fundo = st.selectbox("Fundo", [(15, "PVC 5mm"), (12, "3D Print")], format_func=lambda x: x[1])
        corpo = st.selectbox("Corpo", [(130, "PETG (Externo)"), (100, "PLA (Interno)")], format_func=lambda x: x[1])

    # 4. CÁLCULOS (Lógica traduzida do seu HTML)
    qtd_letras = len(texto.replace(" ", ""))
    fator_maquina = 1.0 # Ex: Kobra 2 Max
    watts_maquina = 500
    
    custo_mat = corpo[0] * mult_mat
    preco_corpo = ((h * 2) + (w * 2)) * p * 0.17808 * fator_maquina * (custo_mat / 130)
    energia = ((h + w) / 10) * fator_maquina * (watts_maquina / 1000) * kwh
    
    # Preço Unitário
    valor_unit = (preco_corpo + (face[0] * mult_mat) + (fundo[0] * mult_mat) + led_tipo[0] + cor_face[0] + energia)
    total_orcamento = valor_unit * qtd_letras

    # 5. ÁREA PRINCIPAL
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    # Preview Neon
    estilo = "led-rgb" if led_tipo[0] == 75 else ("led-on" if led_tipo[0] > 0 else "")
    st.markdown(f'<div class="preview-box"><div class="preview-text {estilo}">{texto if texto else "PREVIEW"}</div></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💰 Resumo Financeiro")
        st.metric("Total Orçamento", f"R$ {total_orcamento:,.2f}")
        st.write(f"**Unitário:** R$ {valor_unit:,.2f}")
        st.write(f"**Cliente:** {nome_cliente}")
    
    with col2:
        st.subheader("📝 Detalhes Técnicos")
        st.write(f"• Letras: {qtd_letras} | Altura: {h}cm")
        st.write(f"• Região: {estado} (KWh: R$ {kwh})")
        st.write(f"• Face: {face[1]} | Fundo: {fundo[1]}")

else:
    # TELA DE BLOQUEIO (Vendas)
    st.title("🔒 ACESSO RESTRITO")
    st.warning("Assinatura não encontrada ou dados de login incorretos.")
    st.info("Acesse hugoadm / 1920 para o modo administrador.")
    st.markdown("[🚀 Clique aqui para assinar o SPP](https://spp.uniplenotech.com.br/)")
