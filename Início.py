import streamlit as st
import pandas as pd
from project.get_data import GetIPEAData


# Configurações da página
st.set_page_config(page_title="Início", page_icon="🛢️", layout="wide")

st.write("# Petrolytics: Explorando os dados do IPEA 🛢️")

st.markdown(
    """
Bem-vindo ao Petrolytics, sua bússola analítica na era pós-pandêmica. Enquanto o mundo continua a navegar pelas consequências da COVID-19, a capacidade de entender e prever as tendências de saúde pública nunca foi tão crucial. Hospitalytics é uma plataforma dedicada a decifrar o comportamento da pandemia usando dados do PNAD-COVID-19 do IBGE, equipando profissionais de saúde com insights essenciais para antecipar e combater ondas futuras de infecções. Mergulhe conosco na jornada através dos dados, onde cada gráfico revela uma história, cada número fala sobre vidas e cada insight pode ser a chave para salvar mais amanhãs. Nossa aplicação web, construída com Streamlit, reúne informações abrangentes e visualizações intuitivas para facilitar a compreensão e a tomada de decisões estratégicas.

Explore os dados coletados e navegue pelos diferentes painéis para descobrir tendências, identificar as principais variações e compreender o impacto em diversas demografias e aspectos socioeconômicos. Nosso objetivo é fornecer uma experiência intuitiva e rica em informações para que você possa explorar, analisar e extrair insights valiosos dos dados disponíveis.
"""
)

# Dados
ipea = GetIPEAData(
            ipea_table="EIA366_PBRENT366",
            database_path="source\ipea_brent_oil.csv"
        )
if "df_data" not in st.session_state:
    # st.session_state.df_data = pd.read_csv("source\ipea_brent_oil.csv", sep=",")
    # st.session_state.df_data = st.session_state.df_data['date'] = pd.to_datetime(st.session_state.df_data['date'], format='%Y-%m-%d')
    st.session_state.df_data = ipea.df_brent_oil

st.line_chart(st.session_state.df_data, x='date', y='value', use_container_width=True)

st.write(f'Pandas: {pd.__version__}')
st.write(f'Streamlit: {st.__version__}')
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
