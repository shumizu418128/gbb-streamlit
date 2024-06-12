import streamlit as st
import pandas as pd

import available

st.set_page_config(
    page_title="GBB結果一覧"
)

# 年度を選択
years = available.years

# Option to filter by year
selected_year = st.selectbox('GBB開催年', options=years)

# Load data from CSV files
try:
    results_df = pd.read_csv(f'gbb{selected_year}_result.csv')

except pd.errors.EmptyDataError:
    st.error('データが見つかりませんでした。更新をお待ちください。')

else:
    st.subheader(f'GBB{selected_year} 結果一覧')
    st.dataframe(results_df)
    st.write("上記入賞者は、全員次回のGBB出場権を獲得しています。")

# 各種リンク
st.markdown('---')

st.link_button("GBBdata-lab トップページ", "Home",
               type="primary", use_container_width=True)

st.link_button('GBBINFO-JPN', 'https://gbbinfo-jpn.jimdofree.com/')
