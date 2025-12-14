

#URL DO SITE https://meu-primeiro-app-phvs3006.streamlit.app/
#URL DO KAGGLE: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
# 1. Carregar dados (sem cache, direto)
teste3_filtered = pd.read_csv('teste3_filtered.csv')
#
Nordeste= ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN','SE']
Sudeste= ['ES', 'MG', 'RJ','SP']
Norte= ['AC' , 'AM', 'AP', 'PA','RO','RR','TO']
Centroeste= ['DF', 'GO', 'MS', 'MT']
Sul= ['PR','RS','SC']
#
# Traduzindo o genero pra colocar no Gráfico
regiãosemsigla = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AM': 'Amazonas',
    'AP': 'Amapá',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MG': 'Minas Gerais',
    'MS': 'Mato Grosso do Sul',
    'MT': 'Mato Grosso',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'PR': 'Paraná',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'RS': 'Rio Grande do Sul',
    'SC': 'Santa Catarina',
    'SE': 'Sergipe',
    'SP': 'São Paulo',
    'TO': 'Tocantins'
}

# Traduzindo os métodos de pagamento para português
payment_type_traducao = {
    'credit_card': 'Cartão de Crédito',
    'boleto': 'Boleto',
    'voucher': 'Voucher',
    'debit_card': 'Cartão de Débito'
}

# Criando uma cópia para evitar SettingWithCopyWarning
teste3_copy = teste3_filtered.copy()
teste3_copy['customer_state_full'] = teste3_copy['customer_state'].map(regiãosemsigla)
teste3_copy['payment_type_portugues'] = teste3_copy['payment_type'].map(payment_type_traducao)

# clientes com as siglas tranformadas em nome do estado
clientes_nordeste = teste3_copy[teste3_copy['customer_state'].isin(Nordeste)]
clientes_sudeste = teste3_copy[teste3_copy['customer_state'].isin(Sudeste)]
clientes_sul = teste3_copy[teste3_copy['customer_state'].isin(Sul)]
clientes_norte = teste3_copy[teste3_copy['customer_state'].isin(Norte)]
clientes_centroeste = teste3_copy[teste3_copy['customer_state'].isin(Centroeste)]

# 2. Criar o seletor (direto na página)
regiãoes= ''
região= ''
Estadoes= ''

Ropções = ['Nordeste', 'Sudeste', 'Norte', 'Centroeste', 'Sul']
regiãoes = st.selectbox('Selecione o estado:', Ropções)

#trocar nome em região
if regiãoes is "Nordeste":
    região = clientes_nordeste
elif regiãoes is  "Sudeste":
    região = clientes_sudeste
elif regiãoes is "Sul":
    região = clientes_sul
elif regiãoes is "Norte":
    região = clientes_norte
elif regiãoes is "Centro-Oeste":
    região = clientes_centroeste

# Define the region name based on the chosen DataFrame
# You can change this manually or implement a more dynamic mapping if needed
    nome_da_regiao = regiãoes
#nome do estado 
nome_completo_estado = regiãosemsigla.get(Estadoes, Estadoes)
# Filter teste3_copy for the chosen state
estado_filtrado = teste3_copy[teste3_copy['customer_state'] == Estadoes]
nome_completo_estado = regiãosemsigla.get(Estadoes, Estadoes)

#aaaa
payment_distribution_nordeste = clientes_nordeste.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
payment_distribution_sudeste = clientes_sudeste.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
payment_distribution_sul = clientes_sul.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
payment_distribution_norte = clientes_norte.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
payment_distribution_centroeste = clientes_centroeste.groupby(['customer_state_full', 'payment_type_portugues']).size().reset_index(name='count')
#aaaaaaaaaaaaa
regiãopag = 0
# Região vai ser o escolhida no filtro
if região is clientes_nordeste:
    regiãopag = payment_distribution_nordeste
elif região is clientes_sudeste:
    regiãopag = payment_distribution_sudeste
elif região is clientes_sul:
    regiãopag = payment_distribution_sul
elif região is clientes_norte:
    regiãopag = payment_distribution_norte
elif região is clientes_centroeste:
    regiãopag = payment_distribution_centroeste
# Define the region name based on the chosen DataFrame
# You can change this manually or implement a more dynamic mapping if needed


# Grafico de barras
   # fig, ax = plt.subplots(figsize=(7, 4))
   # sns.barplot(x='count', y='customer_state_full', hue='payment_type_portugues', data=regiãopag, orient='h', palette='viridis')
 #   ax.set_title(f'istribuição de Tipos de Pagamento por Estado (Região {nome_da_regiao})') # Um título mínimo
   # st.pyplot(fig)
# Cria a figura e o eixo explicitamente
fig, ax = plt.subplots(figsize=(12, 8))

# Desenha o gráfico no eixo 'ax' criado acima
sns.barplot(
    x='count', 
    y='customer_state_full', 
    hue='payment_type_portugues', 
    data=regiãopag, 
    orient='h', 
    palette='viridis',
    ax=ax # Importante: vincular ao eixo
)

# Configurações de texto
ax.set_title(f'Distribuição de Tipos de Pagamento por Estado (Região {nome_da_regiao})')
ax.set_xlabel('Número de Pagamentos')
ax.set_ylabel('Estado do Cliente')
ax.legend(title='Tipo de Pagamento', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()

# Em vez de plt.show(), usa-se st.pyplot()
st.pyplot(fig)


