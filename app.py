import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    url = 'owid-covid-data.csv'
    df = pd.read_csv(url, parse_dates=['date'])
    return df

df = load_data()

st.title("COVID-19 Global Data Tracker — Streamlit")

countries = sorted(df['location'].unique())
sel_countries = st.sidebar.multiselect("Select countries", countries, default=['Kenya','United States'])
start_date = st.sidebar.date_input("Start date", value=df['date'].min().date())
end_date = st.sidebar.date_input("End date", value=df['date'].max().date())

mask = (df['location'].isin(sel_countries)) & (df['date'].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))
df_vis = df.loc[mask]

if not df_vis.empty:
    fig = px.line(df_vis, x='date', y='total_cases', color='location', title='Total Cases Over Time')
    st.plotly_chart(fig, use_container_width=True)

    df_vis['new_cases_7d'] = df_vis.groupby('location')['new_cases'].transform(lambda s: s.rolling(7, min_periods=1).mean())
    fig2 = px.line(df_vis, x='date', y='new_cases_7d', color='location', title='Daily New Cases (7-day MA)')
    st.plotly_chart(fig2, use_container_width=True)

    if 'people_vaccinated' in df_vis.columns and 'population' in df_vis.columns:
        df_vis['pct_vaccinated'] = df_vis['people_vaccinated'] / df_vis['population'] * 100
        fig3 = px.line(df_vis, x='date', y='pct_vaccinated', color='location', title='% Population Vaccinated')
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.write("No data for selected filters.")
