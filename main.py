import streamlit as st
import pandas as pd

st.title('GBB全出場者一覧')

# 年度を選択
years = [2024, 2023]

# Option to filter by year
selected_year = st.selectbox('GBB開催年', options=years)

# Load data from CSV files
beatboxers_df = pd.read_csv(f'gbb{selected_year}_participants.csv')
countries_df = pd.read_csv('countries.csv')

# Merge data to include country names in beatboxers_df
beatboxers_df = beatboxers_df.merge(countries_df[['iso_code', 'name', "name_ja"]], on='iso_code', how='left', suffixes=('', '_country'))

# 出場カテゴリーを取得
# beatboxers_dfの2列目の内容をすべて取得
categories = list(beatboxers_df["category"].unique())

# すべてのカテゴリーを選択肢に追加
categories.insert(0, "すべて")

# カテゴリーを選択
selected_category = st.selectbox('カテゴリー', options=categories)

# 出場区分
ticket_class = ["すべて", "Wildcard", "シード権"]

# 出場区分を選択
selected_ticket_class = st.selectbox('出場区分', options=ticket_class)

# 国ごとに検索するための選択肢を作成
country_options = countries_df['name_ja'].unique()

# 国名を五十音順に並べ替え
country_options = sorted(country_options)

# "日本"をリストから削除
country_options.remove("日本")

# "日本"をリストの先頭に挿入
country_options.insert(0, "日本")

# すべての国を選択肢に追加
country_options.insert(0, "すべて")

# 国を選択
selected_country = st.selectbox('国', options=country_options)

######################
# フィルター処理
######################

if all([selected_category, selected_ticket_class, selected_country]):

    # Filter data based on selected_ticket_class
    if selected_ticket_class != "すべて":

        # Wildcardを選択した場合
        if selected_ticket_class == "Wildcard":
            beatboxers_df = beatboxers_df[beatboxers_df['ticket_class'].str.startswith('Wildcard')]

        # シード権を選択した場合
        if selected_ticket_class == "シード権":
            beatboxers_df = beatboxers_df[~beatboxers_df['ticket_class'].str.startswith('Wildcard')]

    # Filter data based on selected_category
    if selected_category != "すべて":
        beatboxers_df = beatboxers_df[beatboxers_df["category"] == selected_category]

    # Filter data based on selected_country
    if selected_country != "すべて":
        beatboxers_df = beatboxers_df[beatboxers_df['name_ja'] == selected_country]

    # nameにcancelledが含まれる行を削除
    beatboxers_df = beatboxers_df[~beatboxers_df['name'].str.startswith('[cancelled]')]

    # delete unnecessary columns
    beatboxers_df = beatboxers_df.drop(['iso_code', "name_country"], axis=1)

    # Display filtered data
    if beatboxers_df.empty:
        st.write("該当するデータはありません。")

    else:
        st.write(beatboxers_df)
