import streamlit as st
import joblib
import pandas as pd

st.set_page_config(page_title="Calculadora de Aluguel", page_icon="🏠")

try:
    modelo = joblib.load('modelo_aluguel.pkl')
    colunas_modelo = joblib.load('colunas_aluguel.pkl')
except FileNotFoundError:
    st.error("Erro: Arquivos .pkl não encontrados.")
    st.stop()

st.title("🏠 Quanto custa morar aqui?")
st.markdown("IA para estimar o **custo total mensal** (Aluguel + Condomínio) de um imóvel.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    cidade = st.selectbox("Cidade", ['São Paulo', 'Porto Alegre', 'Rio de Janeiro', 'Campinas', 'Belo Horizonte'])
    area = st.number_input("Área (m²)", min_value=10, max_value=1000, value=60)
    quartos = st.slider("Quartos", 1, 10, 2)
    banheiros = st.slider("Banheiros", 1, 10, 1)

with col2:
    vagas = st.slider("Vagas de Garagem", 0, 10, 1)
    condominio = st.number_input("Valor do Condomínio (R$)", min_value=0, value=500, help="Se for casa de rua, coloque 0.")
    mobilia = st.radio("Está mobiliado?", ["Não", "Sim"])

if st.button("Calcular Valor Estimado"):
    dados_input = {
        'Area': area,
        'Quartos': quartos,
        'Banheiros': banheiros,
        'Vagas': vagas,
        'Mobilia': 1 if mobilia == "Sim" else 0,
        'Condominio': condominio
    }
    
    df_input = pd.DataFrame([dados_input])
    cidades_possiveis = ['São Paulo', 'Porto Alegre', 'Rio de Janeiro', 'Campinas', 'Belo Horizonte']
    
    for c in cidades_possiveis:
        nome_coluna = f"Cidade_{c}"
        if nome_coluna in colunas_modelo:
            if c == cidade:
                df_input[nome_coluna] = 1
            else:
                df_input[nome_coluna] = 0
                
    df_final = df_input.reindex(columns=colunas_modelo, fill_value=0)
    previsao = modelo.predict(df_final)[0]
    
    st.divider()
    st.success(f"💰 Valor Total Estimado: R$ {previsao:,.2f} / mês")
    st.caption("Considerando aluguel + condomínio + taxas médias.")