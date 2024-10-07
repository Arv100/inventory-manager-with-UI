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
    return client

client = get_collection()
db = client['inventory_manager'] 
inventory = db['inventory']

st.header('Fetch Collection')
st.divider()

col1, col2, col3 = st.columns([2,2,2])

with col1:
    st.text_input('Item Name',key='item_name')

with col2:
    st.text_input('Item Brand',key='item_brand')
    
with col3:
    st.markdown("<br>",unsafe_allow_html=True)
    st.button('Fetch',use_container_width=True,type='primary',key='fetch')

session_state = st.session_state

if session_state['fetch']:
    if session_state['item_name'] == "" and session_state['item_brand'] == "":
        result = list(inventory.find({},{'_id' : 0}))
        st.write(result)
    else:
        if session_state['item_name'] != "":
            result = list(inventory.find({"item_name" : session_state['item_name']},{'_id' : 0}))
            if len(result) > 0:
                st.write(result)
            else:
                st.warning('Incorrect item name')
        if session_state['item_brand'] != "":
            result = list(inventory.find({"item_brand" : session_state['item_brand']},{'_id' : 0}))
            if len(result) > 0:
                st.write(result)
            else:
                st.warning('Incorrect item name')