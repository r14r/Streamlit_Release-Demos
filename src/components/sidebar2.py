import streamlit as st
import os


def show_sidebar(root:str = '.', handler = None):
    st.header("Sidebar")
    folders = [f for f in os.listdir(root) 
               if os.path.isdir(os.path.join(root, f)) and f[0].isdigit()]

    print(folders)
    selected = st.selectbox('Select folder:', folders)

    if handler:
        handler(selected)