import streamlit as st
st.set_page_config(
    page_title="GBBdata-lab"
)
st.markdown("""
    <script>
        window.location.replace("https://gbbinfo-jpn.onrender.com/");
    </script>
""", unsafe_allow_html=True)


st.title('GBBdata-lab')
st.write("当ページはサービスを終了しました。今後は[GBBINFO-JPN](https://gbbinfo-jpn.onrender.com/)をご利用ください。")

st.link_button("GBBINFO-JPN", "https://gbbinfo-jpn.onrender.com/")

st.markdown("made by [GBBINFO-JPN](https://gbbinfo-jpn.onrender.com/) owner NOT swissbeatbox")
