import streamlit as st
#URL DO SITE https://meu-primeiro-app-phvs3006.streamlit.app/
#URL DO KAGGLE: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# 1. Carregar dados 

# importando pacotes
import pandas as pd
import kagglehub
import os


caminho = kagglehub.dataset_download("olistbr/brazilian-ecommerce")

csv1 = "olist_customers_dataset.csv"




csv2 = "olist_order_items_dataset.csv"
full_csv2 = os.path.join(caminho, csv2)
dados2=  pd.read_csv(os.path.join(caminho, full_csv2))
dados2.head()


csv3 = "olist_order_payments_dataset.csv"
full_csv3 = os.path.join(caminho, csv3)
dados3=  pd.read_csv(os.path.join(caminho, full_csv3))
dados3.head()


csv4 = "olist_orders_dataset.csv"
full_csv4 = os.path.join(caminho, csv4)
dados4=  pd.read_csv(os.path.join(caminho, full_csv4))
dados4.head()


teste = pd.merge(dados4, dados2, on='order_id', how='inner')
teste.head()


teste2 = pd.merge(teste, dados3, on='order_id', how='inner')
teste2.head()



costu= pd.merge(dados4, dados1, on='customer_id', how='inner')
costu.head(10)


teste3= pd.merge(teste2, costu, on='order_id', how='inner')
teste3.head()




Nordeste= ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN','SE']
Sudeste= ['ES', 'MG', 'RJ','SP']
Norte= ['AC' , 'AM', 'AP', 'PA','RO','RR','TO']
Centroeste= ['DF', 'GO', 'MS', 'MT']
Sul= ['PR','RS','SC']

# Filtrando clientes da região Nordeste
clientes_nordeste = teste3[teste3['customer_state'].isin(Nordeste)]
print('Clientes da região Nordeste:')
display(clientes_nordeste.head())


# Filtrando clientes da região Sudeste
clientes_sudeste = teste3[teste3['customer_state'].isin(Sudeste)]
print('Clientes da região Sudeste:')
display(clientes_sudeste.head())


# Filtrando clientes da região Norte
clientes_norte = teste3[teste3['customer_state'].isin(Norte)]
print('Clientes da região Norte:')
display(clientes_norte.head())


# Filtrando clientes da região Centro-Oeste
clientes_centroeste = teste3[teste3['customer_state'].isin(Centroeste)]
print('Clientes da região Centro-Oeste:')
display(clientes_centroeste.head())


# Filtrando clientes da região Sul
clientes_sul = teste3[teste3['customer_state'].isin(Sul)]
print('Clientes da região Sul:')
display(clientes_sul.head())




# 2. Criar o seletor (direto na página)
options = ['Nordeste', 'Sudeste', 'Norte', 'Centroeste', 'Sul']
selected_var = st.selectbox('Selecione a variável de agrupamento:', options)

# 3. Calcular a taxa de sobrevivência
# Usamos .dropna() para garantir que o groupby funcione se houver NaNs na coluna selecionada
try:
    survival_rate = titanic.dropna(subset=[selected_var]) \
                           .groupby(selected_var)['survived'] \
                           .mean() \
                           .reset_index()

    # 4. Criar o gráfico
    # É necessário criar fig, ax para passar para st.pyplot()
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(
        x=selected_var,
        y='survived',
        data=survival_rate,
        ax=ax
    )
    ax.set_ylim(0, 1) # Define o limite do eixo Y
    ax.set_title(f'Taxa de Sobrevivência por {selected_var}') # Um título mínimo

    # 5. Exibir o gráfico
    st.pyplot(fig)

except Exception as e:
    st.error(f"Erro ao processar a coluna '{selected_var}': {e}")
