# Libs
import pandas as pd
import streamlit as st
from project.get_data import GetIPEAData

# Dataviz
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

# Configurações da página
st.set_page_config(page_title="Insigths", page_icon="🛢️", layout="wide")
st.header("Insights Extraídos")

# Layout do aplicativo
tab0, tab1, tab2 = st.tabs(
    [
        "Linha do Tempo",
        "Análise_2",
        "Análise dos dias da Semana"
    ]
)

if "df_data" not in st.session_state:
    # Dados
    ipea = GetIPEAData(database_path="source\db_main.csv")
    st.session_state.df_data = ipea.db_main


with tab0:
    # Crie um widget date_input para o usuário selecionar um intervalo de datas
    col1, col2 = st.columns(2)
    with col1:
        start_date = pd.to_datetime(
            st.date_input(
                "Selecione a data de início", st.session_state.df_data["date"].min()
            )
        )
    with col2:
        end_date = pd.to_datetime(
            st.date_input(
                "Selecione a data de término", st.session_state.df_data["date"].max()
            )
        )

    # Gráfico de linha com filtros
    fig = px.line(st.session_state.df_data, x="date", y="oil_value_usd")
    mask = (st.session_state.df_data["date"] >= start_date) & (
        st.session_state.df_data["date"] <= end_date
    )
    fig.update_traces(x=st.session_state.df_data[mask]["date"])

    # Design & layout
    fig.update_layout(
        title='Distribuição do valor do petróleo Brent ao longo dos anos',
        title_x=0.5,
        title_font=dict(size=24),
        width=2000, 
        height=500,
        template='plotly_dark'
        )

    fig.update_xaxes(
        title='Anos',
        title_font=dict(size=18)
        )

    fig.update_yaxes(
        title='Valor',
        title_font=dict(size=18)
        )

    idx = st.session_state.df_data.groupby(st.session_state.df_data[mask]["date"].dt.year)["oil_value_usd"].idxmax()

    # Adicione um ponto ao gráfico em cada um desses índices
    fig.add_trace(px.scatter(st.session_state.df_data.loc[idx], x="date", y="oil_value_usd").data[0])
    fig.update_traces(
        marker=dict(
            color='red',
            size=10
            )
        )

    st.plotly_chart(fig, use_container_width=True)
    st.write('Pontos vermelhos são os maiores picos em cada ano')


with tab1:
    correlation_matrix = st.session_state.df_data.corr().round(2)
    fig = ff.create_annotated_heatmap(
        z=correlation_matrix.to_numpy(),
        y=correlation_matrix.columns.to_list(),
        x=correlation_matrix.columns.to_list(),
        textfont_color='white',
        zmax=1,
        zmin=-1,
        showscale=True,
        hoverongaps=True,
        colorscale='ice'
        )
    fig.update_layout(
            title='Contagem de valores nos dias da semana',
            title_font=dict(size=24),
            width=500, 
            height=500
            )
    fig.update_layout(
        title='Matriz de Correlação',
        xaxis_nticks=36)
    st.plotly_chart(fig, use_container_width=True)


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