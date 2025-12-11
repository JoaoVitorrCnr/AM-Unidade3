import streamlit as st
import joblib
import numpy as np


st.set_page_config(page_title="Auto Market Segmenter", page_icon="🚗")

try:
    modelo = joblib.load('modelo_carros.pkl')
    scaler = joblib.load('scaler_carros.pkl')
except FileNotFoundError:
    st.error("Erro: Arquivos .pkl não encontrados. Baixe do Colab e coloque na mesma pasta.")
    st.stop()

st.title("🚗 Classificador de Nicho Automotivo")
st.markdown("Defina as especificações técnicas do protótipo para identificar seu **Segmento de Mercado**.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Motor e Performance")
    hp = st.slider("Potência (Cavalos/HP)", 40, 250, 100)
    acc = st.slider("Aceleração (0-100 km/h em seg)", 8.0, 25.0, 15.0, help="Tempo em segundos. Menor = Mais rápido.")

with col2:
    st.subheader("Estrutura e Eficiência")
    weight = st.number_input("Peso do Veículo (lbs)", min_value=1500, max_value=5500, value=3000, step=100)
    mpg = st.slider("Consumo (Milhas por Galão)", 10.0, 50.0, 25.0, help="Quanto maior, mais econômico.")

if st.button("Analisar Prototipo"):
    dados = np.array([[mpg, hp, weight, acc]])
    dados_escalados = scaler.transform(dados)
    cluster = modelo.predict(dados_escalados)[0]
    segmento = ""
    detalhes = ""
    icone = ""
    
 
    if mpg > 28 and weight < 2500:
        segmento = "CARRO ECONÔMICO / COMPACTO"
        detalhes = "Focado em eficiência e uso urbano. Baixo custo operacional."
        icone = "🍃"
        cor = "success" 
    elif hp > 130 and acc < 14:
        segmento = "ESPORTIVO / MUSCLE CAR"
        detalhes = "Alta performance, motor potente, mas alto consumo."
        icone = "🏎️"
        cor = "error"
    else:
        segmento = "SEDAN PESADO / UTILITÁRIO"
        detalhes = "Veículo robusto, pesado e com motorização padrão. Equilíbrio entre força e consumo."
        icone = "🚙"
        cor = "warning" 
    st.divider()
    st.header(f"{icone} {segmento}")
    
    if cor == "success":
        st.success(detalhes)
    elif cor == "error":
        st.error(detalhes)
    else:
        st.warning(detalhes)
        
    st.caption(f"Cluster Técnico: {cluster}")