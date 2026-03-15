import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SPP - Sistema de Precificação Pro",
    page_icon="🚀",
    layout="wide"
)

# --- ESTILO CSS PARA LAYOUT MODERNO ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background: linear-gradient(45deg, #22c55e, #16a34a);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 24px;
        color: #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. CONFIGURAÇÕES DE DADOS
# Para gerar: Arquivo > Compartilhar > Publicar na Web > Valores separados por vírgula (.csv)
URL_PLANILHA = "SUA_URL_DA_PLANILHA_CSV_AQUI"

def verificar_acesso(email_digitado):
    if not email_digitado:
        return False
    try:
        df = pd.read_csv(URL_PLANILHA)
        # Ajuste o nome da coluna para bater com a sua planilha (ex: 'email')
        lista_autorizada = df['email'].str.lower().str.strip().tolist()
        return email_digitado.lower().strip() in lista_autorizada
    except:
        return False

# 3. BARRA LATERAL (LOGIN)
st.sidebar.image("https://spp.uniplenotech.com.br/wp-content/uploads/2024/02/logo-spp.png", width=150)
st.sidebar.title("🔐 ÁREA DO ASSINANTE")

email_user = st.sidebar.text_input("E-mail", placeholder="seu@email.com")
senha_mestre = st.sidebar.text_input("Chave de Ativação", type="password")

# --- LÓGICA DE VALIDAÇÃO ---
# Verifica se é o Administrador OU se está na planilha
is_admin = (email_user.lower().strip() == "hugoadm" and senha_mestre == "1920")
acesso_permitido = is_admin or (verificar_acesso(email_user) and senha_mestre == "HUGO2026")

if acesso_permitido:
    st.sidebar.success(f"✅ Acesso Liberado!")
    if is_admin:
        st.sidebar.info("Modo Administrador Ativo")

    # ---------------------------------------------------------
    # INTERFACE PRINCIPAL DO SISTEMA (APÓS LOGIN)
    # ---------------------------------------------------------
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    # Exemplo de organização por Tabs (Abas)
    tab1, tab2, tab3 = st.tabs(["📊 Calculadora", "💡 Visualização", "📁 Histórico"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Configurações do Projeto")
            texto_letreiro = st.text_input("Texto do Letreiro", "HUGO LETRA CAIXA").upper()
            material = st.selectbox("Tipo de Material", ["Acrílico", "PVC Expandido", "Chapa Galvanizada"])
            
        with col2:
            st.subheader("Custos e Margens")
            custo_energia = st.number_input("Custo Energia (kWh)", value=0.85)
            margem_lucro = st.slider("Margem de Lucro (%)", 0, 300, 100)

        # Exemplo de métricas de resultado
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Custo Estimado", "R$ 450,00")
        m2.metric("Preço Sugerido", f"R$ {450 * (1 + margem_lucro/100):.2f}")
        m3.metric("Tempo de Produção", "4h 30min")

    with tab2:
        st.subheader("Preview do Design")
        st.info("Aqui entrará o código do seu preview animado/Neon.")

else:
    # ---------------------------------------------------------
    # TELA DE BLOQUEIO (SITE DE VENDA)
    # ---------------------------------------------------------
    st.title("🔒 SISTEMA RESTRITO")
    
    col_venda, col_img = st.columns([2, 1])
    
    with col_venda:
        st.warning("### ⚠️ Assinatura não identificada ou expirada.")
        st.write("""
            Para utilizar o **SPP - Sistema de Precificação Pro**, você precisa de uma assinatura ativa. 
            Com ela, você terá acesso total às ferramentas de:
            - **Cálculo de Custos Realista** (Energia, Mão de Obra e Insumos).
            - **Preview de Letreiros** para apresentação ao cliente.
            - **Exportação de Orçamentos** em PDF profissional.
        """)
        
        # Botão de Venda com estilo CSS
        st.markdown("""
            <a href="https://spp.uniplenotech.com.br/" target="_blank">
                <button style="
                    background-color: #22c55e; 
                    color: white; 
                    padding: 18px 30px; 
                    border: none; 
                    border-radius: 12px; 
                    font-size: 20px; 
                    font-weight: bold; 
                    cursor: pointer;
                    width: 100%;
                    box-shadow: 0 4px 15px rgba(34, 197, 94, 0.4);">
                    🚀 LIBERAR MEU ACESSO AGORA
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        st.caption("Já é assinante? Insira os seus dados na barra lateral à esquerda.")

    st.sidebar.info("Dúvidas? Suporte via WhatsApp Unipleno.")
