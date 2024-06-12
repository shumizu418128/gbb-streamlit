import pandas as pd
import streamlit as st

import available

st.set_page_config(page_title="GBB 全出場者一覧")

st.title('GBB全出場者一覧')

# 年度を選択
years = available.years

# Option to filter by year
selected_year = st.selectbox('GBB開催年', options=years)

# Load data from CSV files
beatboxers_df = pd.read_csv(f'gbb{selected_year}_participants.csv')
countries_df = pd.read_csv('countries.csv')

# Merge data to include country names in beatboxers_df
beatboxers_df = beatboxers_df.merge(countries_df[[
                                    'iso_code', 'name', "name_ja"]], on='iso_code', how='left', suffixes=('', '_country'))

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

# 出身国ごとに検索するための選択肢を作成
country_options = countries_df['name_ja'].unique()

# 出身国名を五十音順に並べ替え
country_options = sorted(country_options)

# "日本"をリストから削除
country_options.remove("日本")

# "日本"をリストの先頭に挿入
country_options.insert(0, "日本")

# すべての出身国を選択肢に追加
country_options.insert(0, "すべて")

# 出身国を選択
selected_country = st.selectbox('出身国', options=country_options)

######################
# フィルター処理
######################

if all([selected_category, selected_ticket_class, selected_country]):

    # Filter data based on selected_ticket_class
    if selected_ticket_class != "すべて":

        # Wildcardを選択した場合
        if selected_ticket_class == "Wildcard":
            beatboxers_df = beatboxers_df[beatboxers_df['ticket_class'].str.startswith(
                'Wildcard')]

        # シード権を選択した場合
        if selected_ticket_class == "シード権":
            beatboxers_df = beatboxers_df[~beatboxers_df['ticket_class'].str.startswith(
                'Wildcard')]

    # Filter data based on selected_category
    if selected_category != "すべて":
        beatboxers_df = beatboxers_df[beatboxers_df["category"]
                                      == selected_category]

    # Filter data based on selected_country
    if selected_country != "すべて":
        beatboxers_df = beatboxers_df[beatboxers_df['name_ja']
                                      == selected_country]

    # nameにcancelledが含まれる行を削除
    beatboxers_df = beatboxers_df[~beatboxers_df['name'].str.startswith(
        '[cancelled]')]

    # delete unnecessary columns
    beatboxers_df = beatboxers_df.drop(['iso_code', "name_country"], axis=1)

    # beatboxers_dfのmembers列がすべて無い場合、members列を削除
    if beatboxers_df['members'].isnull().all():
        beatboxers_df = beatboxers_df.drop(['members'], axis=1)

    # カテゴリーが指定されている場合、カテゴリー列を削除
    if selected_category != "すべて" and not beatboxers_df.empty:
        st.markdown('---')
        beatboxers_df = beatboxers_df.drop(['category'], axis=1)
        st.text(f'【選択中のカテゴリー】{selected_category}')

    # Display filtered data
    if beatboxers_df.empty:
        st.subheader('😭該当するデータがありません')

        # 条件が「すべて」になっていない条件を調べる
        if selected_country != "すべて":
            st.write('ヒント：出身国を「すべて」に設定してみて！')
        elif selected_ticket_class != "すべて":
            st.write('ヒント：出場区分を「すべて」に設定してみて！')
        elif selected_category != "すべて":
            st.write('ヒント：カテゴリーを「すべて」に設定してみて！')

        st.text(
            f'【選択中の条件】 出場区分: {selected_ticket_class}、カテゴリー: {selected_category}、出身国: {selected_country}')

    else:
        st.write(beatboxers_df)

# 各種リンク
st.markdown('---')

st.link_button("GBBdata-lab トップページ", "Home",
               type="primary", use_container_width=True)

st.link_button('GBBINFO-JPN', 'https://gbbinfo-jpn.jimdofree.com/')
