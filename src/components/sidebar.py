import os
import streamlit as st

def show_sidebar(root):
    with st.sidebar:
        folders = [f for f in os.listdir(root) 
               if os.path.isdir(os.path.join(root, f)) and f[0].isdigit()]

        sorted_folders = sorted(folders, reverse=True)

        if sorted_folders:
            folder_selected = st.selectbox('Select a folder:', sorted_folders)

            additional_entries(folder_selected, root)
        else:
            st.write("No folders starting with a number were found.")



def additional_entries(selected_folder, directory):
    folder_path = os.path.join(directory, selected_folder)
    
    files = [f for f in os.listdir(f"{folder_path}/pages") if f.endswith(".py")]

    if files:
        st.write(f"Files in {selected_folder}:")
        for file in files:
            st.write(file)
    else:
        st.write("This folder is empty.")

    if st.button(f'Create a new file in {selected_folder}'):
        open(os.path.join(folder_path, 'new_file.txt'), 'w').close()
        st.success("New file created successfully in the selected folder.")
