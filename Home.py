import streamlit as st
from pymongo import MongoClient

st.set_page_config(
    page_icon='🏡',
    page_title='Inventory management',
    layout='wide',
    initial_sidebar_state="expanded"
)

st.header("Inventory Manager")
st.divider()

@st.cache_resource
def get_collection():
    client = MongoClient(st.secrets["mongo"]['host'])
    db = client['inventory_manager']        
    return db['inventory']

inventory = get_collection()
result = inventory.find({},{"_id" : 0})

st.dataframe(
    result,
    use_container_width=True
)