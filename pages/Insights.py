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
st.set_page_config(page_title="Insights", page_icon="📊", layout="wide")
st.header("Insights Extraídos 📊")

# Layout do aplicativo
tab0, tab1, tab2 = st.tabs(
    ["Linha do Tempo", "Indicadores Econômicos", "Análise dos dias da Semana"]
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
        title="Distribuição do valor do petróleo Brent ao longo dos anos",
        title_font=dict(size=24),
        width=2000,
        height=500,
        template="plotly_dark",
    )

    fig.update_xaxes(title="Anos", title_font=dict(size=18))

    fig.update_yaxes(title="Valor", title_font=dict(size=18))

    idx = st.session_state.df_data.groupby(
        st.session_state.df_data[mask]["date"].dt.year
    )["oil_value_usd"].idxmax()

    # Adicione um ponto ao gráfico em cada um desses índices
    fig.add_trace(
        px.scatter(st.session_state.df_data.loc[idx], x="date", y="oil_value_usd").data[
            0
        ]
    )
    fig.update_traces(marker=dict(color="red", size=10))

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        """
        Nossa seção "Linha do Tempo" oferece uma jornada visual através da história dos preços do petróleo Brent, destacando como eventos globais e tendências econômicas se refletiram no mercado energético. Esta linha do tempo é mais do que uma simples trilha de números; ela é um mapa que revela como conflitos geopolíticos, avanços tecnológicos, crises financeiras e mudanças na política ambiental têm influenciado os preços ao longo das décadas.

        Cada pico e vale em nosso gráfico conta uma história: o choque dos preços na virada do milênio, a volatilidade durante a crise financeira de 2008, as implicações da revolução do xisto nos EUA e a recente instabilidade trazida pela pandemia COVID-19. Ao explorar esses pontos de dados, você pode observar padrões e extrair lições valiosas que informam não apenas sobre o estado atual do mercado, mas também sobre possíveis futuros cenários
        """
    )


with tab1:
    correlation_matrix = st.session_state.df_data.corr().round(2)
    correlation_matrix.columns = ['Ano', 'Mês', 'Dia', 'Valor Brent (USD)', 'Valor Euro (USD)', 'Valor Dolar (BRL)', 'IPC Percent (a.m)', 'Valor Nasdaq'] 
    fig = ff.create_annotated_heatmap(
        z=correlation_matrix.to_numpy(),
        y=correlation_matrix.columns.to_list(),
        x=correlation_matrix.columns.to_list(),
        textfont_color="white",
        zmax=1,
        zmin=-1,
        showscale=True,
        hoverongaps=True,
        colorscale="ice",
    )
    fig.update_layout(
        title="Matriz de Correlação", title_font=dict(size=24), width=500, height=500
    )
    fig.update_xaxes(
        ticktext=["Nova Coluna 1", "Nova Coluna 2", "Nova Coluna 3", 'a', 'a', 'a', 'a']
        )
    fig.update_yaxes(
        ticktext=["Nova Coluna 1", "Nova Coluna 2", "Nova Coluna 3", 'a', 'a', 'a', 'a']
        )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        No coração do setor energético, o preço do petróleo Brent é influenciado por uma complexa rede de fatores econômicos. A seção "Indicadores Econômicos" mergulha na interdependência dos indicadores econômicos globais e seu impacto nos preços do petróleo. Utilizando uma matriz de correlação avançada, revelamos como variáveis como índices de bolsas de valores, taxas de câmbio e outros indicadores macroeconômicos se movem em conjunto com os preços do petróleo.
        
        Esta análise não apenas destaca correlações diretas, mas também aponta para influências menos óbvias que podem não ser imediatamente aparentes. Por exemplo, uma correlação positiva forte entre o preço do petróleo e um determinado índice de mercado pode sinalizar a sensibilidade do setor energético a mudanças na confiança dos investidores. Alternativamente, uma correlação negativa com uma moeda pode indicar a influência das políticas monetárias e das taxas de juros.
        Entender essas dinâmicas é crucial para qualquer estratégia de gestão de risco e investimento, pois fornece uma visão mais holística e fundamentada do mercado. Através desta lente analítica, você pode antecipar melhor as reações do mercado a eventos futuros e posicionar-se de forma proativa.
        """
    )


with tab2:
    col1, col2 = st.columns(2)
    with col1:
        ## DATAVIZ COUNT PLOT
        fig = px.histogram(
            st.session_state.df_data,
            y="week_date",
            text_auto=True,
            color="week_date",
            color_discrete_sequence=px.colors.qualitative.Safe,
        )

        fig.update_layout(
            title="Contagem de valores nos dias da semana",
            title_font=dict(size=24),
            width=500,
            height=500,
            template="plotly_dark",
            showlegend=False,
        )
        fig.update_yaxes(title="Dia da semana", title_font=dict(size=18))

        fig.update_xaxes(title="Contagem", title_font=dict(size=18))
        # Atualize as barras
        fig.update_traces(
            textposition="outside",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write(
            "Neste gráfico, observamos a contagem de valores registrados para o petróleo Brent durante cada dia da semana. A distribuição reflete o pulso do comércio global de petróleo, com a atividade do mercado seguindo o calendário comercial tradicional. Durante os finais de semana, vemos uma queda notável, um reflexo direto do fechamento dos mercados globais. Essa tendência ressalta a importância do tempo na indústria do petróleo, onde cada dia da semana carrega seu próprio perfil de atividade e potencial de negociação."
        )

    fig = px.scatter(
        st.session_state.df_data,
        x="oil_value_usd",
        y="year",
        color="week_date",
        title="Relation Between Oil Price and Year based on the Week Day",
        color_discrete_sequence=px.colors.qualitative.Safe,
    )
    fig.update_layout(
        title="Distribuição do valor do Petróleo Brent em cada ano por dia da semana",
        title_font=dict(size=24),
        width=500,
        height=750,
        template="plotly_dark",
        showlegend=False,
    )
    fig.update_yaxes(title="Ano", title_font=dict(size=18))
    fig.update_xaxes(title="Valor do Petróleo Brent", title_font=dict(size=18))

    st.plotly_chart(fig, use_container_width=True)
    st.write(
        "Aqui, traçamos a distribuição dos preços do petróleo Brent ao longo dos anos, discriminada por dias da semana. Esse gráfico revela se existem padrões de preços consistentes ou anomalias que emergem em dias específicos ao longo do tempo. Pode-se notar, por exemplo, se os picos de preço tendem a ocorrer mais em um dia da semana do que em outros, o que poderia sugerir a influência de relatórios de mercado ou atualizações políticas regulares. Essa perspectiva temporal oferece aos analistas um detalhe granular, possibilitando uma análise direcionada que pode capturar nuances ocultas nas tendências de preços."
    )
