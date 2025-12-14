

#URL DO SITE https://meu-primeiro-app-phvs3006.streamlit.app/
#URL DO KAGGLE: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
# 1. Carregar dados (sem cache, direto)
base = pd.read_csv('teste3_filtered.csv')
print(base)
