import streamlit as st
import json

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="SPP - Precificação Pro",
    page_icon="🚀",
    layout="wide"
)

# --- CSS PARA SIMULAR O VISUAL DO HTML ORIGINAL ---
st.markdown("""
    <style>
    .main { background-color: #f3f4f6; }
    .stApp { color: #334155; }
    
    /* Container de Preview Estilo Letreiro */
    .preview-box {
        background: radial-gradient(circle, #1e293b 0%, #000000 100%);
        padding: 40px;
        border-radius: 12px;
        text-align: center;
        border: 3px solid #334155;
        margin-bottom: 20px;
    }
    
    .preview-text {
        font-size: 50px;
        font-weight: 900;
        text-transform: uppercase;
        color: white;
        text-shadow: 0 0 12px rgba(255,255,255,0.6);
    }
    
    .led-rgb {
        animation: rgbCycle 3s infinite linear;
    }

    @keyframes rgbCycle {
        0% { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
        33% { color: #00ff00; text-shadow: 0 0 15px #00ff00; }
        66% { color: #0000ff; text-shadow: 0 0 15px #0000ff; }
        100% { color: #ff0000; text-shadow: 0 0 15px #ff0000; }
    }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS DE REFERÊNCIA (TRANSFORMADOS DO JS)
base_regional = {
    "BA - Coelba": [0.92, 1.05], "SP - Enel": [0.84, 1.00], "RJ - Light": [0.98, 1.02],
    "MG - Cemig": [0.91, 1.00], "PR - Copel": [0.78, 0.98], "RS - Equatorial": [0.88, 1.03],
    "SC - Celesc": [0.76, 0.98], "PE - Neoenergia": [0.89, 1.08], "CE - Enel": [0.94, 1.10],
    "GO - Equatorial": [0.85, 1.02], "MT - Energisa": [0.96, 1.12], "AM - Amazonas": [1.02, 1.25],
    "PA - Equatorial": [1.05, 1.20], "DF - Neoenergia": [0.82, 1.05], "ES - EDP": [0.86, 1.01]
}

impressoras = {
    "Anycubic": [
        {"nome": "Kobra 2 Max", "fator": 1.0, "watts": 500},
        {"nome": "Kobra 3 Max", "fator": 0.95, "watts": 550},
        {"nome": "Kobra 2 Plus", "fator": 1.05, "watts": 450}
    ],
    "Bambu Lab": [
        {"nome": "X1-Carbon", "fator": 0.85, "watts": 350},
        {"nome": "P1S", "fator": 0.88, "watts": 350}
    ],
    "Creality": [
        {"nome": "K1 Max", "fator": 0.9, "watts": 1000},
        {"nome": "Ender 3 V3", "fator": 1.1, "watts": 350}
    ]
}

# 3. INTERFACE LATERAL (INPUTS)
st.sidebar.header("⚙️ CONFIGURAÇÕES")
nome_cliente = st.sidebar.text_input("NOME DO CLIENTE", "CLIENTE FINAL")

with st.sidebar.expander("📝 Detalhes do Letreiro", expanded=True):
    texto = st.text_input("Texto do Letreiro", "TEXTO").upper()
    qtd_letras = len(texto.replace(" ", ""))
    led_opcao = st.selectbox("Iluminação LED", 
                            options=[(0, "Sem Iluminação"), (45, "Branco Frio/Quente"), (75, "RGB Colorido")],
                            format_func=lambda x: x[1])
    
    h = st.number_input("Altura (cm)", value=30)
    w = st.number_input("Largura (cm)", value=32)
    p = st.number_input("Profundidade (cm)", value=5)

with st.sidebar.expander("🛠️ Materiais e Máquina"):
    estado = st.selectbox("Localização (Custo Regional)", options=list(base_regional.keys()))
    marca = st.selectbox("Marca da Impressora", options=list(impressoras.keys()))
    
    lista_modelos = impressoras[marca]
    modelo_selecionado = st.selectbox("Modelo da Máquina", 
                                    options=lista_modelos, 
                                    format_func=lambda x: x['nome'])
    
    face = st.selectbox("Material da Face", 
                        options=[(0, "Nenhum"), (15, "Acrílico 2mm"), (35, "Policarbonato 2mm")],
                        format_func=lambda x: x[1])
    
    fundo = st.selectbox("Material do Fundo", 
                         options=[(0, "Sem Fundo"), (15, "PVC Expandido 5mm"), (12, "Impressão 3D")],
                         format_func=lambda x: x[1])
    
    mat_corpo = st.selectbox("Material do Corpo", 
                             options=[(130, "Uso Externo (PETG)"), (100, "Uso Interno (PLA)")],
                             format_func=lambda x: x[1])

perfil = st.sidebar.radio("Perfil de Cliente", ["Cliente Final (100%)", "Terceirização (80%)", "Personalizado"])
if perfil == "Personalizado":
    ajuste = st.sidebar.number_input("Ajuste (%)", value=0)
else:
    ajuste = 0 if "Final" in perfil else -20

# 4. LÓGICA DE CÁLCULO (PYTHON)
kwh, mult_material = base_regional[estado]
mat_custo = mat_corpo[0] * mult_material
face_custo = face[0] * mult_material
fundo_custo = fundo[0] * mult_material

# Cálculo baseado na sua fórmula original JS
preco_corpo = ((h * 2) + (w * 2)) * p * 0.17808 * modelo_selecionado['fator'] * (mat_custo / 130)
energia = ((h + w) / 10) * modelo_selecionado['fator'] * (modelo_selecionado['watts'] / 1000) * kwh

valor_unitario = (preco_corpo + face_custo + fundo_custo + led_opcao[0] + energia) * (1 + (ajuste / 100))
total_geral = valor_unitario * qtd_letras

# 5. ÁREA PRINCIPAL (OUTPUT)
st.title("SPP - SISTEMA DE PRECIFICAÇÃO PRO")
st.caption(f"Orçamento para: **{nome_cliente}**")

# Preview Visual
estilo_led = "led-rgb" if led_opcao[0] == 75 else "preview-text"
st.markdown(f"""
    <div class="preview-box">
        <div class="{estilo_led}">{texto if texto else "PREVIEW"}</div>
        <div style="color: #60a5fa; font-size: 12px; margin-top: 10px; font-weight: bold;">
            {led_opcao[1].upper()}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Painel de Resultados
col_res1, col_res2 = st.columns([1, 1])

with col_res1:
    st.subheader("💰 Resumo Financeiro")
    st.metric("Total do Orçamento", f"R$ {total_geral:,.2f}")
    st.write(f"**Valor Unitário:** R$ {valor_unitario:,.2f} / por letra")
    st.info("💡 Corpo interno sempre em branco para melhor reflexão.")

with col_res2:
    st.subheader("📋 Detalhamento Técnico")
    st.write(f"**Nº de Letras:** {qtd_letras}")
    st.write(f"**Dimensões:** {h}cm (H) x {w}cm (L) x {p}cm (P)")
    st.write(f"**Máquina:** {modelo_selecionado['nome']} ({marca})")
    st.write(f"**Local:** {estado}")

st.warning("⚠️ **Nota:** Estes valores servem como uma base orçamentária prévia. O valor final será confirmado após análise do arquivo técnico.")

# Botão de Impressão (Simulado)
if st.button("🖨️ Gerar Orçamento (Imprimir)"):
    st.write("Dica: Use Ctrl+P para salvar esta página como PDF.")
