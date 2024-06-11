import pandas as pd
import streamlit as st

# Set up Streamlit
st.title('辞退者一覧')

# 年度を選択
years = [2024]

# Option to filter by year
selected_year = st.selectbox('GBB開催年', options=years)

# Load data from CSV files
beatboxers_df = pd.read_csv(f'gbb{selected_year}_participants.csv')
countries_df = pd.read_csv('countries.csv')

# Merge data to include country names in beatboxers_df
beatboxers_df = beatboxers_df.merge(
    countries_df[['iso_code', 'name']], on='iso_code', how='left', suffixes=('', '_country'))

# Filter beatboxers whose names start with "[cancelled]"
cancelled_beatboxers_df = beatboxers_df[beatboxers_df['name'].str.startswith(
    '[cancelled]')]

# nameから"[cancelled]"を削除
cancelled_beatboxers_df.loc[:, 'name'] = cancelled_beatboxers_df['name'].str.replace('[cancelled]', '')

# delete unnecessary columns
cancelled_beatboxers_df = cancelled_beatboxers_df.drop(['iso_code', "name_country"], axis=1)

# cancelled_beatboxers_dfのmembers列がすべて無い場合、members列を削除
if cancelled_beatboxers_df['members'].isnull().all():
    cancelled_beatboxers_df = cancelled_beatboxers_df.drop(['members'], axis=1)

# Display the cancelled beatboxers data
st.dataframe(cancelled_beatboxers_df)

# Display the countries data
st.markdown("---")

st.link_button("GBBdata-lab トップページ", "Home", type="primary", use_container_width=True)
st.link_button("GBBINFO-JPN トップページ", "https://gbbinfo-jpn.jimdofree.com/")
