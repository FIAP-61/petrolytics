# contexto_brent.py

# Importações necessárias
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Contexto", page_icon="⛽")

# Título da página
st.title("Contexto do Petróleo Brent ⛽")

# Introdução ao contexto do Petróleo Brent
st.write(
    """
Antes de começarmos a trabalhar com os dados do Petróleo Brent, precisamos entender um pouco do contexto dessa variável e onde ela está inserida.

O local de extração do Petróleo Brent diz muito sobre as variações de preço que ele sofre. A localização faz parte de uma das características econômicas do bem porque envolve características de transporte e comercialização desse bem.

O Petróleo Brent é extraído do Mar do Norte, que é parte do Oceano Atlântico.
"""
)


st.write(
    "O local de extração divide fronteira com os países do Reino Unido, Noruega, França, Dinamarca, Holanda, Alemanha e Bélgica."
)

# Adicionar imagem do mapa
st.image("source/mapa.png", caption="Mar do Norte e países adjacentes.")

st.markdown(
    "Fonte: [North Sea Brent Crude](https://corporatefinanceinstitute.com/resources/commodities/north-sea-brent-crude/)"
)
