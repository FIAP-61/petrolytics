# Libs
import streamlit as st
import joblib
from datetime import datetime, timedelta

# Dataviz libs
import plotly.graph_objects as go
import plotly.express as px

# Functions
from project.get_data import GetIPEAData


# Configurações da página
st.set_page_config(page_title="Início", page_icon="🔮", layout="wide")

st.write("# Predizendo os dados do Petróleo Brent 🔮")

if "df_data" not in st.session_state:
    # Dados
    # st.session_state.df_data = pd.read_csv("source\ipea_brent_oil.csv", sep=",")
    # st.session_state.df_data = st.session_state.df_data['date'] = pd.to_datetime(st.session_state.df_data['date'], format='%Y-%m-%d')
    ipea = GetIPEAData(
                ipea_table="EIA366_PBRENT366",
                database_path="source\ipea_brent_oil.csv"
            )
    st.session_state.df_data = ipea.df_brent_oil

model_swa = joblib.load('swa.joblib')
df_pred = model_swa.predict(h=90, level=[95])


# Dados preditos
df_pred = df_pred[(df_pred['ds'] > datetime.today()) & (df_pred['ds'] < datetime.today() + timedelta(8))]

fig = px.line(df_pred, x='ds', y='SeasWA', hover_data=['SeasWA'])

for i in range(0, df_pred.shape[0]):
    fig.add_trace(
        go.Scatter(
            x=[df_pred['ds'].iloc[-i]],
            y=[df_pred['SeasWA'].iloc[-i]],
            text=[df_pred['SeasWA'].iloc[-i]],
            mode='markers+text',
            marker=dict(color='white', size=10),
            textfont=dict(color='white', size=15),
            textposition='top right',
            showlegend=False
        )
    )

fig.update_layout(
    title='Predição de valores da semana seguinte',
    title_x=0.5,
    title_font=dict(size=24),
    width=2000, 
    height=500,
    template='plotly_dark'
    )

fig.update_xaxes(
    title='Valor Predito',
    title_font=dict(size=18)
    )

fig.update_yaxes(
    title='Data',
    title_font=dict(size=18)
    )

st.plotly_chart(fig, use_container_width=True)
