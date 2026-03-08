import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# 2. CONEXÃO COM A PLANILHA (Substitua pelo link da sua planilha em formato CSV)
# Dica: No Google Sheets, vá em Arquivo > Compartilhar > Publicar na Web > Valores separados por vírgula (.csv)
URL_PLANILHA = "SUA_URL_DA_PLANILHA_EM_CSV_AQUI"

def verificar_assinante(email_digitado):
    try:
        df = pd.read_csv(URL_PLANILHA)
        # Transforma tudo em minúsculo para evitar erro de digitação
        lista_emails = df['email'].str.lower().str.strip().tolist()
        return email_digitado.lower().strip() in lista_emails
    except:
        return False

# 3. LOGIN NA BARRA LATERAL
st.sidebar.title("🔐 PORTAL UNIPLENO TECH")
email_user = st.sidebar.text_input("E-mail de Cadastro")
senha_mestre = st.sidebar.text_input("Chave do Sistema", type="password")

if verificar_assinante(email_user) and senha_mestre == "HUGO2026":
    
    st.sidebar.success(f"Assinatura Ativa: {email_user}")
    
    # --- INÍCIO DO SISTEMA (TUDO O QUE VOCÊ JÁ TINHA) ---
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    # Preview Animado
    texto_preview = st.text_input("Texto do Letreiro", value="TEXTO LETREIRO").upper()
    
    # (Inserir aqui todo o resto do código de CSS, cálculos e seletores)
    st.markdown("""<style> /* Seu CSS de Neon aqui */ </style>""", unsafe_allow_html=True)
    
    # Exemplo de Seletor que já começa como você pediu
    led_dict = {"Sem Iluminação": 0, "LED Branco": 45, "LED RGB": 75}
    led_sel = st.selectbox("Iluminação LED", list(led_dict.keys()), index=0)

    # ... RESTANTE DO CÓDIGO TÉCNICO ...

else:
    if email_user:
        st.sidebar.error("❌ Acesso Negado. Verifique seu pagamento em spp.uniplenotech.com.br")
    st.warning("🔒 Área restrita. Por favor, faça login para calcular seus orçamentos.")