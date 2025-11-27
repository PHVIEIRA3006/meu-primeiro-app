import streamlit as st
#URL DO SITE https://meu-primeiro-app-phvs3006.streamlit.app/
st.title('Meu primeiro App🎶')
st.header('Vamos fazer algo com intertividade')
n = st.number_input('Entre com um numero')
st.write(f'O numero que você escolheu ao quadrado é {n**2}')
