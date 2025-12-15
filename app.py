#URL DO SITE https://meu-primeiro-app-phvs3006.streamlit.app/
#URL DO KAGGLE: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(layout="wide") 

# --- 1. Carregar dados ---
@st.cache_data
def carregar_dados():
    return pd.read_csv('teste3_filtered.csv')

try:
    teste3_filtered = carregar_dados()
except FileNotFoundError:
    st.error("Arquivo 'teste3_filtered.csv' não encontrado. Usando dados fictícios.")
    dados_dict = {
        'customer_state': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'RS'], 100),
        'payment_type': np.random.choice(['credit_card', 'boleto', 'voucher'], 100),
        'price': np.random.uniform(10, 1000, 100),
        'freight_value': np.random.uniform(5, 50, 100),
        'payment_installments': np.random.randint(1, 12, 100)
    }
    teste3_filtered = pd.DataFrame(dados_dict)

# Definição das Regiões
Nordeste = ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE']
Sudeste = ['ES', 'MG', 'RJ', 'SP']
Norte = ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO']
Centroeste = ['DF', 'GO', 'MS', 'MT']
Sul = ['PR', 'RS', 'SC']

# Dicionários de Tradução
regiãosemsigla = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AM': 'Amazonas', 'AP': 'Amapá',
    'BA': 'Bahia', 'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo',
    'GO': 'Goiás', 'MA': 'Maranhão', 'MG': 'Minas Gerais', 'MS': 'Mato Grosso do Sul',
    'MT': 'Mato Grosso', 'PA': 'Pará', 'PB': 'Paraíba', 'PE': 'Pernambuco',
    'PI': 'Piauí', 'PR': 'Paraná', 'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte',
    'RO': 'Rondônia', 'RR': 'Roraima', 'RS': 'Rio Grande do Sul', 'SC': 'Santa Catarina',
    'SE': 'Sergipe', 'SP': 'São Paulo', 'TO': 'Tocantins'
}

payment_type_traducao = {
    'credit_card': 'Cartão de Crédito',
    'boleto': 'Boleto',
    'voucher': 'Voucher',
    'debit_card': 'Cartão de Débito'
}

# Tratamento do DataFrame
teste3_copy = teste3_filtered.copy()
teste3_copy['customer_state_full'] = teste3_copy['customer_state'].map(regiãosemsigla)
teste3_copy['payment_type_portugues'] = teste3_copy['payment_type'].map(payment_type_traducao)

# Filtros prévios por região
clientes_nordeste = teste3_copy[teste3_copy['customer_state'].isin(Nordeste)]
clientes_sudeste = teste3_copy[teste3_copy['customer_state'].isin(Sudeste)]
clientes_sul = teste3_copy[teste3_copy['customer_state'].isin(Sul)]
clientes_norte = teste3_copy[teste3_copy['customer_state'].isin(Norte)]
clientes_centroeste = teste3_copy[teste3_copy['customer_state'].isin(Centroeste)]

# --- 2. Interface Streamlit ---

st.title("Análise de Vendas por Região e Estado")

# --- SELETORES (LAYOUT 3x1) ---
col_filtro1, col_filtro2, col_filtro3 = st.columns(3)

regiao_raw = pd.DataFrame() 
nome_da_regiao = ""

# Coluna 1: Região
with col_filtro1:
    opcoes_regiao = ['Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']
    escolha_regiao = st.selectbox('Selecione a região:', opcoes_regiao)
    nome_da_regiao = escolha_regiao
    
    if escolha_regiao == "Nordeste":
        regiao_raw = clientes_nordeste
    elif escolha_regiao == "Sudeste":
        regiao_raw = clientes_sudeste
    elif escolha_regiao == "Sul":
        regiao_raw = clientes_sul
    elif escolha_regiao == "Norte":
        regiao_raw = clientes_norte
    elif escolha_regiao == "Centro-Oeste":
        regiao_raw = clientes_centroeste

# Coluna 2: Estado
with col_filtro2:
    lista_estados = sorted(regiao_raw['customer_state_full'].unique())
    lista_estados.insert(0, 'Todos')
    estado_selecionado = st.selectbox("Selecione o Estado:", lista_estados)

# Coluna 3: Outliers
with col_filtro3:
    st.write("Configuração Visual:")
    mostrar_outliers = st.checkbox("Mostrar Outliers nos Gráficos", value=True)

# --- LÓGICA DO FILTRO MESTRE E AGRUPAMENTO ---
dados_visuais = regiao_raw.copy()
titulo_contexto = f"Região {nome_da_regiao}"

# Cria coluna 'Local' unificada
if estado_selecionado == 'Todos':
    dados_visuais['Local'] = nome_da_regiao
else:
    dados_visuais = dados_visuais[dados_visuais['customer_state_full'] == estado_selecionado]
    dados_visuais['Local'] = dados_visuais['customer_state_full']
    titulo_contexto = estado_selecionado

st.markdown("---")

# --- NOVO: SEÇÃO DE KPI / MÉTRICAS ---
st.subheader(f"📊 Resumo Estatístico - {titulo_contexto}")

# Cálculo das métricas
total_vendas = len(dados_visuais)

if total_vendas > 0:
    preco_medio = dados_visuais['price'].mean()
    frete_medio = dados_visuais['freight_value'].mean()
    parcelas_media = dados_visuais['payment_installments'].mean()
else:
    preco_medio = 0
    frete_medio = 0
    parcelas_media = 0

# Exibição em 4 colunas
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("📦 Total de Pedidos", f"{total_vendas}")
kpi2.metric("💰 Preço Médio", f"R$ {preco_medio:.2f}")
kpi3.metric("🚚 Frete Médio", f"R$ {frete_medio:.2f}")
kpi4.metric("💳 Média de Parcelas", f"{parcelas_media:.1f}x")

st.markdown("---")

# --- GRÁFICOS LINHA 1 ---
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.subheader(f"1. Tipos de Pagamento ({titulo_contexto})")
    dados_agrupados_pagamento = dados_visuais.groupby(['Local', 'payment_type_portugues']).size().reset_index(name='count')
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Local',y='count',hue='payment_type_portugues',data=dados_agrupados_pagamento, orient='v',palette='viridis',ax=ax1)
    ax1.set_title('') 
    ax1.set_xlabel('Local')
    ax1.set_ylabel('Qtd. Pedidos')
    ax1.tick_params(axis='x', rotation=45) 
    ax1.legend(title='Pagamento', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig1)

with row1_col2:
    st.subheader(f"2. Distribuição do Preço ({titulo_contexto})")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Local', y='price', data=dados_visuais, orient='v', palette='viridis', showfliers=mostrar_outliers, ax=ax2)
    ax2.set_title(f'')
    ax2.set_xlabel('Local')
    ax2.set_ylabel('Valor (R$)')
    st.pyplot(fig2)

st.markdown("---")

# --- GRÁFICOS LINHA 2 ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.subheader(f"3. Valor do Frete ({titulo_contexto})")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='Local', y='freight_value', data=dados_visuais, orient='v', palette='crest', showfliers=mostrar_outliers, ax=ax3)
    ax3.set_title(f'Frete - {titulo_contexto}')
    ax3.set_xlabel('Local')
    ax3.set_ylabel('Valor Frete')
    st.pyplot(fig3)

with row2_col2:
    st.subheader(f"4. Numero de parcelas ({titulo_contexto})")
    dados_apenas_credito = dados_visuais[dados_visuais['payment_type'] == 'credit_card']
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    if dados_apenas_credito.empty:
        st.warning(f"Sem dados de crédito.")
        max_parcelas = 1
    else:
        max_parcelas = dados_apenas_credito['payment_installments'].max()
        if pd.isna(max_parcelas): max_parcelas = 1
        max_parcelas = int(max_parcelas)
        bins = range(1, max_parcel
