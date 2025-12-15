#URL DO SITE https://meu-primeiro-app-phvs3006.streamlit.app/
#URL DO KAGGLE: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# --- 1. Carregar dados ---
# Dica: Em produção, use @st.cache_data para não recarregar toda vez
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

# Agrupamentos para o Gráfico de Barras (pre-calculado)
pag_dist_nordeste = clientes_nordeste.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
pag_dist_sudeste = clientes_sudeste.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
pag_dist_sul = clientes_sul.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
pag_dist_norte = clientes_norte.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
pag_dist_centroeste = clientes_centroeste.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')


# --- 2. Interface Streamlit ---

st.title("Análise de Vendas por Região")

# Seletor
opcoes_regiao = ['Centro-Oeste', 'Nordeste', 'Norte', 'Sudeste', 'Sul']
escolha_regiao = st.selectbox('Selecione a região:', opcoes_regiao)

# Lógica de Seleção (Define qual DF usar baseado na escolha)
região = pd.DataFrame() # Inicializa vazio
regiãopag = pd.DataFrame() # Inicializa vazio

if escolha_regiao == "Nordeste":
    região = clientes_nordeste
    regiãopag = pag_dist_nordeste
elif escolha_regiao == "Sudeste":
    região = clientes_sudeste
    regiãopag = pag_dist_sudeste
elif escolha_regiao == "Sul":
    região = clientes_sul
    regiãopag = pag_dist_sul
elif escolha_regiao == "Norte":
    região = clientes_norte
    regiãopag = pag_dist_norte
elif escolha_regiao == "Centro-Oeste":
    região = clientes_centroeste
    regiãopag = pag_dist_centroeste

nome_da_regiao = escolha_regiao

#seletor de estaos
lista_estados = sorted(região['customer_state'].unique())
estado_selecionado = st.selectbox("Selecione o Estado para visualizar o histograma:", ['Todos', lista_estados])




# --- GRÁFICO 1: Barras (Tipos de Pagamento) ---
st.subheader(f"1. Tipos de Pagamento ({nome_da_regiao})")

fig1, ax1 = plt.subplots(figsize=(12, 8))
sns.barplot(
    x='count', 
    y='customer_state_full', 
    hue='payment_type_portugues', 
    data=regiãopag, 
    orient='h', 
    palette='viridis',
    ax=ax1
)
ax1.set_title(f'Distribuição de Tipos de Pagamento por Estado (Região {nome_da_regiao})')
ax1.set_xlabel('Número de Pagamentos')
ax1.set_ylabel('Estado do Cliente')
ax1.legend(title='Tipo de Pagamento', bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig1)

st.markdown("---")

# --- GRÁFICO 2: Boxplot (Valor Pago) ---
st.subheader(f"2. Distribuição do Preço na região ({nome_da_regiao})")
fig2, ax2 = plt.subplots(figsize=(12, 8))
sns.boxplot(
    x='customer_state_full',
    y='price', 
    data=região, 
    orient='v', 
    palette='viridis',
    ax=ax2
    )
ax2.set_title(f'Distribuição do preço por Estado ({nome_da_regiao})')
ax2.set_xlabel('Estado')
ax2.set_ylabel('Valor (R$)')
# Ajuste opcional para visualizar melhor (remove outliers extremos visuais)
ax2.set_ylim(0, região['price'].quantile(0.95)) 
st.pyplot(fig2)

st.markdown("---")

# --- GRÁFICO 3: Boxplot (Valor do Frete) ---
st.subheader(f"3. Distribuição do Valor do Frete ({nome_da_regiao})")

fig3, ax3 = plt.subplots(figsize=(12, 8))
sns.boxplot(
    x='customer_state_full',
    y='freight_value', 
    data=região, 
    orient='v',
    palette='crest',
    ax=ax3
)
ax3.set_title(f'Distribuição do Valor do Frete por Estado (Região {nome_da_regiao})')
ax3.set_xlabel('Estado do Cliente')
ax3.set_ylabel('Valor do Frete')
st.pyplot(fig3)

st.markdown("---")

# --- GRÁFICO 4: Histograma (Parcelas - Apenas Cartão de Crédito) ---
st.subheader(f"4. Frequência de Parcelas - Cartão de Crédito ({nome_da_regiao})")

# *** NOVO FILTRO AQUI ***
# Filtra o dataframe 'região' para pegar apenas linhas onde o pagamento é cartão de crédito
regiao_apenas_credito = região[região['payment_type'] == 'credit_card']

fig4, ax4 = plt.subplots(figsize=(12, 8))

# Cálculo seguro dos bins (usando o dataframe filtrado)
max_parcelas = regiao_apenas_credito['payment_installments'].max()

if pd.isna(max_parcelas):
    max_parcelas = 1 # Evita erro se não houver vendas no cartão
else:
    max_parcelas = int(max_parcelas)

bins = range(1, max_parcelas + 2)

# Desenha o histograma usando o dataframe filtrado (regiao_apenas_credito)
sns.histplot(
    data=regiao_apenas_credito,
    x='payment_installments',
    bins=bins,
    discrete=True,
    color='skyblue',
    ax=ax4
)

ax4.set_title(f'Frequência de Parcelas (Cartão de Crédito) - Região {nome_da_regiao}')
ax4.set_xlabel('Número de Parcelas')
ax4.set_ylabel('Frequência')
ax4.set_xticks(range(1, max_parcelas + 1))
st.pyplot(fig4)
