# Libs
import pandas as pd
import streamlit as st
from project.get_data import GetIPEAData

# Dataviz
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configurações da página
st.set_page_config(page_title="Insigths", page_icon="🛢️", layout="wide")
st.header("Insights Extraídos")

# Layout do aplicativo
tab0, tab1, tab2 = st.tabs(
    [
        "Análise_1",
        "Análise_2",
        "Análise dos dias da Semana"
    ]
)

if "df_data" not in st.session_state:
    # Dados
    ipea = GetIPEAData(database_path="source\db_main.csv")
    st.session_state.df_data = ipea.db_main


with tab2:

    col1, col2 = st.columns(2)    
    with col1:
    
        ## DATAVIZ COUNT PLOT
        fig = px.histogram(
            st.session_state.df_data, 
            y='week_date', 
            text_auto=True,
            color='week_date',
            color_discrete_sequence=px.colors.qualitative.Safe
            )
        
        fig.update_layout(
            title='Contagem de valores nos dias da semana',
            title_font=dict(size=24),
            width=500, 
            height=500,
            template='plotly_dark',
            showlegend=False
            )
        fig.update_yaxes(
            title='Dia da semana',
            title_font=dict(size=18)
            )

        fig.update_xaxes(
            title='Contagem',
            title_font=dict(size=18)
            )
        # Atualize as barras
        fig.update_traces(
            textposition='outside', 
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write('Texto aqui')


    fig = px.scatter(
        st.session_state.df_data, 
        x='oil_value_usd', 
        y='year', 
        color='week_date',
        title='Relation Between Oil Price and Year based on the Week Day',
        color_discrete_sequence=px.colors.qualitative.Safe
        )
    fig.update_layout(
            title='Distribuição do valor do Petróleo Brent em cada ano por dia da semana',
            title_x=0.5,
            title_font=dict(size=24),
            width=500, 
            height=750,
            template='plotly_dark',
            showlegend=False
            )
    fig.update_yaxes(
            title='Ano',
            title_font=dict(size=18)
            )
    fig.update_xaxes(
        title='Valor do Petróleo Brent',
        title_font=dict(size=18)
        )

    st.plotly_chart(fig, use_container_width=True)
    st.write('Texto aqui também')