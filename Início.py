# Libs
import streamlit as st
import pandas as pd
from project.get_data import GetIPEAData

# Dataviz libs
import plotly.express as px
import plotly.graph_objects as go


# Configurações da página
st.set_page_config(page_title="Início", page_icon="🛢️", layout="wide")

st.write("# Petrolytics: Explorando os dados do IPEA 🛢️")

st.markdown(
    """
Boas vindas ao Petrolytics, sua plataforma analítica para o mundo dinâmico do petróleo Brent. Em um mercado que oscila com os ventos da política global, crises econômicas e demandas energéticas em constante mudança, a capacidade de entender e antecipar as tendências dos preços do petróleo é mais valiosa do que nunca. Petrolytics é uma ferramenta dedicada a desvendar os mistérios por trás das flutuações dos preços, equipando analistas, traders e decisores com insights cruciais para navegar no mercado energético com confiança.

Nossa aplicação web construída com Streamlit combina análises detalhadas e visualizações interativas para transformar dados complexos em compreensões claras e acionáveis. Com Petrolytics, você pode mergulhar nos dados históricos e emergentes do preço do petróleo Brent, explorar padrões sazonais e identificar as tendências que moldam o futuro da energia.

Explore, analise e extraia o máximo dos dados disponíveis. Cada gráfico conta uma parte da história, cada análise revela nuances do mercado, e cada insight oferecido pode ser a chave para sua próxima decisão estratégica.
"""
)

if "df_data" not in st.session_state:
    # Dados
    # st.session_state.df_data = pd.read_csv("source\ipea_brent_oil.csv", sep=",")
    # st.session_state.df_data = st.session_state.df_data['date'] = pd.to_datetime(st.session_state.df_data['date'], format='%Y-%m-%d')
    ipea = GetIPEAData(database_path="source\db_main.csv")
    st.session_state.df_data = ipea.db_main

st.session_state.db_war_contry = pd.read_csv('war_data\countries-in-conflict-data-all.csv', sep=",")
st.session_state.db_war_type = pd.read_csv('war_data\countries-in-conflict-data-by-type.csv', sep=",")


# Análisar em que página fica
st.divider()

with st.expander("Fluxograma do processo de atualização e predição dos dados"):
    col1, col2, col3 = st.columns(3)

    with col1:
        pass

    with col2:
        st.write(
            """
            Pontos a serem considerados:
            - Para visualizar o processo de transformação dos dados consulte o código no github;  
            - API de atualização foi criada utilizando a biblioteca: "ipeadatapy";
            - Base de dados no momento da criação do tech challenge é um arquivo em csv que é atualizado de forma incremental;
            - Modelo de machine learning utilizado é o da SeasonalWindowAverage biblioteca statsforecast.
            """
        )
        st.image("pages/petrolytics_flowchart.png")

    with col3:
        pass


# # Layout do aplicativo
# tab0, tab1 = st.tabs(["Ferramentas Utilizadas", "Colunas Selecionadas"])


# with tab0:
#     st.markdown(
#         """
#     ## Ferramentas Utilizadas Durante o Desevolvimento
#     """
#     )

#     st.image("Images/tools.png")

#     st.markdown(
#         """
#     ### Base de Dados &  Transformação
#     Os dados foram ingeridos dentro do sistema de DBFS (Sistema de Arquivos do Databricks).
#     Com o pyspark dentro do databricks foi possível criar a tabela final para o streamlit consumir os dados, fazendo diversos tratamentos e utilizando as bases do PNAN Covid referentes aos meses de setembro, outubro e novembro de 2020.
#     Acesse o link para visualizar o notebook.
#     [Databricks Notebook ↗](https://databricks-prod-cloudfront.cloud.databricks.com/public/4027ec902e239c93eaaa8714f173bcfc/5375801336056031/59063656447375/8314753084412668/latest.html)
#     #
#     """
#     )

#     st.markdown(
#         """
#     ### Conexão com os Dados
#     Por uma limitação do databricks community não é possível criar um "personal access token" para a consulta da tabela pelo streamlit, portanto utilizaremos a exportação dessa tabela para o streamlit ingerir os dados, caso contrário seria possível conectar ao databricks pelo código na imagem abaixo.
#     """
#     )
#     with st.expander("Clique para ver o código de conexão"):
#         st.image("Images/databricks_connection.png")


# with tab1:
#     df_chosen_cols = pd.read_csv("chosen_cols.csv", sep="	")
#     st.markdown(
#         """
#         ## Colunas Selecionadas
#         Foi realizado uma análise dentre aproximadamente 150 colunas disponíveis dentro da base do PNAD Covid, e foram selecionadas as descritas na tabela a seguir.
#         As colunas que estão numeradas em "Coluna Escolhida" são as que entram na contagem do limite de 20 colunas possíveis.
#         """
#     )
#     st.dataframe(df_chosen_cols)


# if "df_data" not in st.session_state:
#     df1 = pd.read_csv("pnad_covid_1.csv", sep=",")
#     df2 = pd.read_csv("pnad_covid_2.csv", sep=",")
#     st.session_state.df_data = pd.concat([df1, df2], axis=0, ignore_index=True)
