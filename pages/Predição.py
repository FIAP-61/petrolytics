# Libs
import joblib
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Dataviz libs
import plotly.graph_objects as go
import plotly.express as px

# Functions
from project.get_data import GetIPEAData


def highlight_min(s):
    """Função para destacar o menor valor de cada linha, exceto a primeira coluna de um dataframe"""
    return "background-color: #0057B8"


# Configurações da página
st.set_page_config(page_title="Predição", page_icon="🔮", layout="wide")
st.write("# Predizendo os dados do Petróleo Brent 🔮")


# Criação das guias
tab1, tab2 = st.tabs(["Predição", "Modelos"])

with tab1:
    # Texto da Sugestão do Modelo
    st.header("Seasonal Window Average")
    st.write(
        "O modelo escolhido para prever os valores diários do Petróleo Brent foi o Seasonal Window Average, devido a ser o modelo com os melhores resultados nas métricas de avaliação (consulte a aba de Modelos para ver os resultados)."
    )
    st.write(
        "O modelo faz uma previsão diária dos próximos 7 dias de acordo com o dia atual."
    )

    model_swa = joblib.load("swa.joblib")
    df_pred = model_swa.predict(h=90, level=[95])

    # Dados preditos
    df_pred = df_pred[
        (df_pred["ds"] > datetime.today())
        & (df_pred["ds"] < datetime.today() + timedelta(8))
    ]

    fig = px.line(df_pred, x="ds", y="SeasWA", hover_data=["SeasWA"])

    for i in range(0, df_pred.shape[0]):
        fig.add_trace(
            go.Scatter(
                x=[df_pred["ds"].iloc[-i]],
                y=[df_pred["SeasWA"].iloc[-i]],
                text=[df_pred["SeasWA"].iloc[-i]],
                mode="markers+text",
                marker=dict(color="white", size=10),
                textfont=dict(color="white", size=15),
                textposition="top right",
                showlegend=False,
            )
        )

    fig.update_layout(
        title="Predição de valores dos próximos 7 dias",
        title_x=0.5,
        title_font=dict(size=24),
        width=2000,
        height=500,
        template="plotly_dark",
    )

    fig.update_xaxes(title="Valor Predito", title_font=dict(size=18))

    fig.update_yaxes(title="Data", title_font=dict(size=18))

    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        O gráfico "Predição de valores dos próximos 7 dias" é o resultado direto de nossa análise preditiva, oferecendo uma janela para o futuro imediato do mercado de petróleo Brent. Com base no modelo Seasonal Window Average, esta visualização é uma representação gráfica das expectativas de preço no curto prazo, permitindo aos usuários um planejamento antecipado com base em dados modelados.

        Cada ponto na linha representa o preço previsto para o petróleo Brent em um dia específico, proporcionando uma visão contínua da tendência esperada de preços. Essa informação é vital para traders e analistas que buscam ajustar rapidamente suas estratégias às mudanças do mercado. É importante notar que, apesar da sofisticação do modelo, as previsões são hipotéticas e sujeitas a incertezas inerentes ao comportamento do mercado.

        Ao utilizar essas previsões, encorajamos uma abordagem equilibrada que leve em conta tanto os dados históricos quanto a perspectiva do cenário econômico global. Essas previsões são uma ferramenta poderosa, mas devem ser usadas como parte de uma estratégia de análise mais ampla e diversificada.
    """
    )


with tab2:
    # Texto da Sugestão do Modelo
    st.header("Comentários")
    st.write(
        "De acordo com os resultados apresentados pelos diversos testes em modelos diferentes de machine learning para séries temporais, elaboramos um resumo com um quadro comparativo para cada uma das análises qual seria a nossa recomendação quanto ao modelo preditivo mais aderente para prever os valores diários do Petróleo Brent."
    )
    st.write(
        "O quadro-resumo é composto com as principais métricas de desempenho para avaliar e comparar os modelos de forecasting de séries temporais."
    )

    # Métricas de avaliação dos modelos (Treino dos dados 2018-2023)
    st.header("Métricas de Avaliação dos Modelos")
    df_metrics = pd.read_csv(r"source/model_metrics.csv", sep="|")

    # Estilo de formatação condicional ao DataFrame
    styled_df = df_metrics.style.applymap(
        highlight_min,
        subset=pd.IndexSlice[:, ["Seasonal Naive", "Seasonal Window Average"]],
    )
    st.dataframe(styled_df)

    # Legenda
    st.divider()
    st.markdown(
        """
        ### Legenda das Siglas de Métricas
        **MAE (Mean Absolute Error)**: Este é o erro médio absoluto entre as previsões e os valores reais. Um MAE mais baixo é geralmente melhor.

        **MSE (Mean Squared Error)**: É a média dos erros ao quadrado. Dá mais peso a erros grandes e é mais sensível a variações.

        **RMSE (Root Mean Squared Error)**: É a raiz quadrada do MSE e fornece uma medida da magnitude dos erros de previsão.

        **MAPE (Mean Absolute Percentage Error)**: Este é o erro médio absoluto expresso como uma porcentagem. É útil para comparar erros entre diferentes escalas.

        **WMAPE (Weighted Mean Absolute Percentage Error)**: Similar ao MAPE, mas pondera os erros com base na magnitude dos valores reais, oferecendo uma métrica mais balanceada.
        """
    )
