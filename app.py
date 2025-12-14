

#URL DO SITE https://meu-primeiro-app-phvs3006.streamlit.app/
#URL DO KAGGLE: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(layout="wide") 

# 1. Carregar dados
# Certifique-se que o arquivo está na mesma pasta
try:
    teste3_filtered = pd.read_csv('teste3_filtered.csv')
except FileNotFoundError:
    st.error("Arquivo 'teste3_filtered.csv' não encontrado.")
    st.stop()

# --- DEFINIÇÕES DE DADOS ---
# Dicionário de Regiões para facilitar a filtragem (Substitui os ifs manuais)
mapa_regioes = {
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Norte': ['AC', 'AM', 'AP', 'PA', 'RO', 'RR', 'TO'],
    'Centro-Oeste': ['DF', 'GO', 'MS', 'MT'], # Corrigido para bater com o selectbox
    'Sul': ['PR', 'RS', 'SC']
}

regiãosemsigla = {
    'AC': 'Acre', 'AL': 'Alagoas', 'AM': 'Amazonas', 'AP': 'Amapá', 'BA': 'Bahia',
    'CE': 'Ceará', 'DF': 'Distrito Federal', 'ES': 'Espírito Santo', 'GO': 'Goiás',
    'MA': 'Maranhão', 'MG': 'Minas Gerais', 'MS': 'Mato Grosso do Sul', 'MT': 'Mato Grosso',
    'PA': 'Pará', 'PB': 'Paraíba', 'PE': 'Pernambuco', 'PI': 'Piauí', 'PR': 'Paraná',
    'RJ': 'Rio de Janeiro', 'RN': 'Rio Grande do Norte', 'RO': 'Rondônia', 'RR': 'Roraima',
    'RS': 'Rio Grande do Sul', 'SC': 'Santa Catarina', 'SE': 'Sergipe', 'SP': 'São Paulo', 'TO': 'Tocantins'
}

payment_type_traducao = {
    'credit_card': 'Cartão de Crédito',
    'boleto': 'Boleto',
    'voucher': 'Voucher',
    'debit_card': 'Cartão de Débito'
}

# Tratamento inicial dos dados
df = teste3_filtered.copy()
df['customer_state_full'] = df['customer_state'].map(regiãosemsigla)
df['payment_type_portugues'] = df['payment_type'].map(payment_type_traducao)

# --- INTERFACE E FILTROS ---
st.title("Análise de Pagamentos por Região")

# Seletor de Região
# Nota: Usei as chaves do dicionário para garantir que os nomes sejam iguais
regiao_selecionada = st.selectbox('Selecione a Região:', list(mapa_regioes.keys()))

# --- LÓGICA DE FILTRAGEM ---
# 1. Pega a lista de estados da região selecionada
estados_da_regiao = mapa_regioes[regiao_selecionada]

# 2. Filtra o DataFrame principal apenas para essa região
df_regiao_filtrada = df[df['customer_state'].isin(estados_da_regiao)]

# 3. Faz o agrupamento (Groupby) apenas para os dados filtrados
regiãopag = df_regiao_filtrada.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')

# --- GRÁFICO ---
if not regiãopag.empty:
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.barplot(
        x='count', 
        y='customer_state_full', 
        hue='payment_type_portugues', 
        data=regiãopag, 
        orient='h', 
        palette='viridis',
        ax=ax
    )

    ax.set_title(f'Distribuição de Tipos de Pagamento - Região {regiao_selecionada}')
    ax.set_xlabel('Número de Pagamentos')
    ax.set_ylabel('Estado')
    ax.legend(title='Tipo de Pagamento')

    st.pyplot(fig)
else:
    st.warning("Não há dados para a região selecionada.")
