import streamlit as st
from pymongo import MongoClient

st.set_page_config(
    page_icon='🏡',
    page_title='Inventory management',
    layout='wide',
    initial_sidebar_state="expanded"
)

@st.cache_resource
def get_collection():
    client = MongoClient(st.secrets["mongo"]['host'])
    db = client['inventory_manager']        
    return db['inventory']

inventory = get_collection()

st.header('Delete Collection')
st.divider()

item_name = st.text_input("Item Name",key='item_name')

if item_name:
    result = inventory.find_one({"item_name" : item_name})
    if not result:
        st.error('Item not found')
    else:
        st.write(result)
        st.divider()
        delete = st.button('Delete',type='primary',key='delete')
        if st.session_state['delete']:
            inventory.delete_one({"item_name" : item_name})
            st.success(f'Item {item_name} : deleted')
            