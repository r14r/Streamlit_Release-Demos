import os
import streamlit as st

from src.components import sidebar


st.set_page_config(
    page_title="About background colors",
    page_icon="🎨",
)

st.title("🎨 Background colors for text")

sidebar.show_sidebar(os.path.dirname(__file__))

with st.echo():
    tabA, tabB = st.tabs(
        [
            "Background color is :orange-background[supported on tab A]",
            ":red-background[And is supported on tab B]",
        ]
    )
with tabA:
    st.markdown("""It also :blue-background[works perfectly inside of them!]""")

with tabB:
    st.write("""It also :blue-background[works perfectly inside of them!]""")
