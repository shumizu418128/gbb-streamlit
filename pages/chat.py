import streamlit as st

import available

st.set_page_config(page_title="GBBINFO-AI")

st.header("準備中")

st.markdown("---")

st.link_button("GBBdata-lab トップページ", "Home", type="primary", use_container_width=True)
st.link_button("GBBINFO-JPN トップページ", "https://gbbinfo-jpn.jimdofree.com/")

# 最終更新日を表示
last_updated = available.get_last_updated()
st.write(f"最終更新日: {last_updated}")
