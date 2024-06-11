import streamlit as st

st.set_page_config(
    page_title="GBBdata-lab"
)

st.title('GBBdata-lab')
st.subheader('ようこそ')
st.write('各種データ ページへのリンク')

st.page_link(
    "pages/世界地図.py",
    label="GBB出場者 世界地図",
    icon="🗺️",
    help="GBB出場者の名前を世界地図上に表示します。",
    use_container_width=True
)
st.page_link(
    "pages/出場者.py",
    label="GBB 全出場者一覧",
    icon="🎤",
    help="GBB出場者の一覧です。カテゴリー、国で絞り込みができます。",
    use_container_width=True
)
st.page_link(
    "pages/辞退者.py",
    label="GBB出場者 キャンセル一覧",
    icon="😭",
    help="GBB出場をキャンセルした方の一覧です。",
    use_container_width=True
)
st.page_link(
    "pages/chat.py",
    label="GBBINFO-AI (準備中)",
    icon="🤖",
    help="GBBINFO-AIとチャットできます。",
    use_container_width=True,
    disabled=True
)

st.markdown('---')

st.link_button("GBBINFO-JPN", "https://gbbinfo-jpn.jimdofree.com/")

st.markdown("made by [GBBINFO-JPN](https://gbbinfo-jpn.jimdofree.com/) owner NOT swissbeatbox")
