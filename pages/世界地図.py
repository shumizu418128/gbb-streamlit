import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

import available

# Set up Streamlit
st.set_page_config(page_title="GBB出場者 世界地図", layout="wide")
st.title('GBB出場者 世界地図')

# 年度を選択
years = available.years

# Option to filter by year
selected_year = st.selectbox('GBB開催年', options=years)

# Load data from CSV files
beatboxers_df = pd.read_csv(f'gbb{selected_year}_participants.csv')
countries_df = pd.read_csv('countries.csv')

# nanを空白に変換
beatboxers_df = beatboxers_df.fillna("")

# beatboxers_dfから、名前に[cancelled]がついている人を削除
beatboxers_df = beatboxers_df[~beatboxers_df["name"].str.contains(
    r"\[cancelled\]", case=False)]

# Initialize a folium map centered around the average latitude and longitude
map_center = [20, 0]
beatboxer_map = folium.Map(location=map_center, zoom_start=3)

# Merge data to include country coordinates in beatboxers_df
beatboxers_df = beatboxers_df.merge(
    countries_df[['iso_code', 'lat', 'lon', 'name']],
    on='iso_code',
    how='left',
    suffixes=('', '_country')
)

# 国ごとに参加者をグループ化
coord_participants = beatboxers_df.groupby(['lat', 'lon'])

# Add markers to the map
# 国ごとにまとめてマーカーを追加
for (lat, lon), group in coord_participants:

    names = group["name"].values
    categories = group["category"].values
    members = group["members"].values

    country_name = group["name_country"].values[0]
    iso_code = group["iso_code"].values[0]

    # 国名を日本語に変換
    # countries_dfからiso_codeが一致する行を取得
    country_data = countries_df[countries_df["iso_code"] == iso_code]
    country_name_ja = country_data["name_ja"].values[0]

    location = (group["lat"].values[0], group["lon"].values[0])

    popup_content = '<div style="font-family: Noto sans JP; font-size: 14px;">'
    popup_content += f'<h3 style="margin: 0; color: #F0632F;">{country_name}</h3>'
    popup_content += f'<h4 style="margin: 0; color: #F0632F;">{country_name_ja}</h4>'

    for name, category, members in zip(names, categories, members):
        if members != "":
            popup_content += f'''
            <p style="margin: 5px 0;">
                <strong style="color: #000000">{name}</strong> ({category})<span style="font-size: 0.7em; color=#222222"><br>【{members}】</span>
            </p>
            '''
        else:
            popup_content += f'''
            <p style="margin: 5px 0;">
                <strong style="color: #000000">{name}</strong> ({category})
            </p>
            '''

    popup_content += '</div>'

    # 画像に合わせてアイコンのサイズを変更
    # 丸画像になっている国のリスト
    country_exception = [
        "Taiwan",
        "Hong Kong",
        "Saudi Arabia",
        "Iran"
    ]

    # アイコン素材がある国の場合
    if country_name not in country_exception:
        icon_size = (56, 42)
        icon_anchor = (0, 40)

    # アイコン素材がない国の場合
    else:
        icon_size = (56, 38)
        icon_anchor = (28, 5)
        popup_content += '<br><p style="margin: 5px 0;">※国旗素材の都合で、<br>他国とは違う画像です</p>'

    popup = folium.Popup(popup_content, max_width=1000)

    flag_icon = folium.CustomIcon(
        icon_image=r"./flags/" + country_name + ".webp",  # アイコン画像のパス
        icon_size=icon_size,  # アイコンのサイズ（幅、高さ）
        icon_anchor=icon_anchor  # アイコンのアンカー位置
    )

    folium.Marker(
        location=location,
        popup=popup,
        icon=flag_icon
    ).add_to(beatboxer_map)

# Display the map
st.write("国旗をクリックすると、その国の出場者を確認できます。")
st.markdown("""
    <style>
    iframe {
        width: 100%;
        min-height: 400px;
        height: 100%:
    }
    </style>
    """,
            unsafe_allow_html=True
            )
folium_static(beatboxer_map)

st.markdown("---")

st.link_button("GBBdata-lab トップページ", "Home",
               type="primary", use_container_width=True)
st.link_button("GBBINFO-JPN トップページ", "https://gbbinfo-jpn.jimdofree.com/")
