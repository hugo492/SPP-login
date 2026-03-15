import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DO SISTEMA
st.set_page_config(page_title="SPP - SISTEMA DE PRECIFICAÇÃO PRO", layout="wide")

# Substitua pela sua URL real do Google Sheets (exportada como CSV)
URL_PLANILHA = "SUA_URL_DA_PLANILHA_CSV_AQUI"

def verificar_acesso(email_digitado):
    if not email_digitado:
        return False
    try:
        # Tenta ler a planilha
        df = pd.read_csv(URL_PLANILHA)
        lista_autorizada = df['email'].str.lower().str.strip().tolist()
        return email_digitado.lower().strip() in lista_autorizada
    except Exception as e:
        # Se a planilha não for encontrada ou a coluna 'email' não existir
        return False

# 2. INTERFACE DE LOGIN (BARRA LATERAL)
# Use uma logo válida ou remova a linha abaixo se não tiver a imagem
st.sidebar.image("https://spp.uniplenotech.com.br/wp-content/uploads/2024/02/logo-spp.png", width=150)
st.sidebar.title("🔐 ÁREA DO ASSINANTE")

email_user = st.sidebar.text_input("E-mail de Compra", placeholder="exemplo@email.com")
senha_mestre = st.sidebar.text_input("Chave de Ativação", type="password")

# --- VALIDAÇÃO DE ACESSO ---
if verificar_acesso(email_user) and senha_mestre == "HUGO2026":
    
    st.sidebar.success("✅ Acesso Liberado!")
    
    st.title("🚀 SPP - SISTEMA DE PRECIFICAÇÃO PRO")
    
    # Exemplo do início do seu sistema
    texto_preview = st.text_input("Texto do Letreiro", value="TEXTO LETREIRO").upper()
    st.write(f"Visualização: {texto_preview}")
    
    # O RESTANTE DO SEU CÓDIGO DA CALCULADORA ENTRA AQUI

else:
    # --- TELA DE BLOQUEIO E DIRECIONAMENTO PARA PAGAMENTO ---
    st.title("🔒 SISTEMA RESTRITO")
    
    col_venda, _ = st.columns([2, 1])
    
    with col_venda:
        st.warning("### ⚠️ Assinatura não identificada ou pendente.")
        st.write("""
            Para utilizar o **SPP - Sistema de Precificação Pro**, você precisa de uma assinatura ativa. 
            Com ela, você terá acesso a:
            - ✅ Cálculo exato de custo de energia e materiais por região.
            - ✅ Preview animado com efeito Neon/RGB.
            - ✅ Gerador de orçamentos profissionais em PDF.
        """)
        
        # BOTÃO DE DIRECIONAMENTO
        st.markdown(f"""
            <a href="https://spp.uniplenotech.com.br/" target="_blank">
                <button style="
                    background-color: #22c55e; 
                    color: white; 
                    padding: 15px 30px; 
                    border: none; 
                    border-radius: 8px; 
                    font-size: 18px; 
                    font-weight: bold; 
                    cursor: pointer;
                    width: 100%;">
                    🚀 QUERO ASSINAR AGORA E LIBERAR MEU ACESSO
                </button>
            </a>
        """, unsafe_allow_html=True)
        
        st.info("Já é assinante? Insira seu e-mail e chave na barra lateral à esquerda.")

    st.sidebar.info("Dúvidas? Entre em contato com o suporte Unipleno.")
    st.sidebar.warning("🔒 Área restrita. Faça login para continuar.")
