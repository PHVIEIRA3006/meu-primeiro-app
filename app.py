#URL DO SITE https://meu-primeiro-app-phvs3006.streamlit.app/
#URL DO KAGGLE: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Configuração da página para usar largura total (opcional, mas ajuda no layout 2x2)
st.set_page_config(layout="wide") 

# --- 1. Carregar dados ---
teste3_filtered = pd.read_csv('teste3_filtered.csv')

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

# --- SELETORES (LAYOUT 2x1) ---
# Cria duas colunas para os filtros
col_filtro1, col_filtro2 = st.columns(2)

regiao_raw = pd.DataFrame() 
nome_da_regiao = ""

with col_filtro1:
    opcoes_regiao = ['Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']
    escolha_regiao = st.selectbox('Selecione a região:', opcoes_regiao)
    nome_da_regiao = escolha_regiao
    
    # Lógica de seleção do DF base
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

with col_filtro2:
    lista_estados = sorted(regiao_raw['customer_state_full'].unique())
    lista_estados.insert(0, 'Todos')
    estado_selecionado = st.selectbox("Selecione o Estado:", lista_estados)

# --- LÓGICA DO FILTRO MESTRE ---
dados_visuais = regiao_raw.copy()
titulo_contexto = f"Região {nome_da_regiao}"

if estado_selecionado != 'Todos':
    dados_visuais = dados_visuais[dados_visuais['customer_state_full'] == estado_selecionado]
    titulo_contexto = estado_selecionado

st.markdown("---")

# --- GRÁFICOS (LAYOUT 2x2) ---

# PRIMEIRA LINHA DE GRÁFICOS (Chart 1 e Chart 2)
row1_col1, row1_col2 = st.columns(2)

# --- GRÁFICO 1 ---
with row1_col1:
    st.subheader(f"1. Tipos de Pagamento")
    
    dados_agrupados_pagamento = dados_visuais.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')

    fig1, ax1 = plt.subplots(figsize=(10, 6)) # Ajustei figsize para caber melhor na coluna
    sns.barplot(
        x='count', 
        y='customer_state_full', 
        hue='payment_type_portugues', 
        data=dados_agrupados_pagamento, 
        orient='h', 
        palette='viridis',
        ax=ax1
    )
    ax1.set_title(f'Distribuição - {titulo_contexto}') # Título mais curto para não quebrar
    ax1.set_xlabel('Qtd. Pedidos')
    ax1.set_ylabel('Estado')
    ax1.legend(title='Pagamento', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot(fig1)

# --- GRÁFICO 2 ---
with row1_col2:
    st.subheader(f"2. Distribuição do Preço")

    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        x='customer_state_full',
        y='price', 
        data=dados_visuais, 
        orient='v', 
        palette='viridis',
        ax=ax2
    )
    ax2.set_title(f'Preço - {titulo_contexto}')
    ax2.set_xlabel('Estado')
    ax2.set_ylabel('Valor (R$)')

    if not dados_visuais.empty:
        ax2.set_ylim(0, dados_visuais['price'].quantile(0.95)) 
    st.pyplot(fig2)


st.markdown("---")


# SEGUNDA LINHA DE GRÁFICOS (Chart 3 e Chart 4)
row2_col1, row2_col2 = st.columns(2)

# --- GRÁFICO 3 ---
with row2_col1:
    st.subheader(f"3. Valor do Frete")

    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.boxplot(
        x='customer_state_full',
        y='freight_value', 
        data=dados_visuais, 
        orient='v',
        palette='crest',
        ax=ax3
    )
    ax3.set_title(f'Frete - {titulo_contexto}')
    ax3.set_xlabel('Estado')
    ax3.set_ylabel('Valor Frete')
    st.pyplot(fig3)

# --- GRÁFICO 4 ---
with row2_col2:
    st.subheader(f"4. Parcelas (Crédito)")

    dados_apenas_credito = dados_visuais[dados_visuais['payment_type'] == 'credit_card']

    fig4, ax4 = plt.subplots(figsize=(10, 6))

    if dados_apenas_credito.empty:
        st.warning(f"Sem dados de crédito.")
        max_parcelas = 1
    else:
        max_parcelas = dados_apenas_credito['payment_installments'].max()
        if pd.isna(max_parcelas): max_parcelas = 1
        max_parcelas = int(max_parcelas)

        bins = range(1, max_parcelas + 2)

        sns.histplot(
            data=dados_apenas_credito,
            x='payment_installments',
            bins=bins,
            discrete=True,
            color='skyblue',
            ax=ax4
        )

        ax4.set_title(f'Freq. Parcelas - {titulo_contexto}')
        ax4.set_xlabel('Nº Parcelas')
        ax4.set_ylabel('Frequência')
        ax4.set_xticks(range(1, max_parcelas + 1))
    
    st.pyplot(fig4)
