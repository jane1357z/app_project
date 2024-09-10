import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('airbib')


@st.cache_data
def get_data():
    df_amsterdam = pd.read_csv("amsterdam_weekends.csv",sep=',')
    df_amsterdam.drop(df_amsterdam.columns[0], axis=1, inplace=True)
    df_amsterdam = df_amsterdam.sample(n=100, replace=False)
    return df_amsterdam


# st.write(df_amsterdam)
data_load_state = st.text('Loading data...')
df_amsterdam = get_data()
data_load_state.text("Done! (using st.cache_data)")

st.subheader('Raw data')
st.write(df_amsterdam)

if st.checkbox('scatter'):
    fig = px.scatter(df_amsterdam, x="rest_index_norm", y="attr_index_norm")
else:
    fig = px.histogram(df_amsterdam, x='room_type')

st.plotly_chart(fig, use_container_width=True)