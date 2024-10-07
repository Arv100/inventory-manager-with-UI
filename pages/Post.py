import streamlit as st
from pymongo import MongoClient
from datetime import datetime

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

session_state = st.session_state
session_state['timestamp'] = datetime.now()

st.header("Insert Collection")
st.divider()

col1, col2 = st.columns([.5,.5])

with col1:
    st.text_input('Item Name',key='item_name')
    st.text_input('Item Brand',key='item_brand')

with col2:
    st.number_input('Item Quantity',key='item_quantity',step=1)
    st.number_input('Item Price',key='item_price',step=1)

if session_state['item_name'] != "" and session_state['item_brand'] != "" and session_state['item_price'] != 0 and session_state['item_quantity'] != 0:
    st.markdown("<br>",unsafe_allow_html=True)
    st.button('Insert',type='primary',key='insert',use_container_width=True)
    if session_state['insert']:
        inventory.insert_one(
            {
                "item_name" : session_state['item_name'],
                "item_brand" : session_state['item_brand'],
                "item_price" : session_state['item_price'],
                "item_quantity" : session_state['item_quantity'],
                "inserted_timestamp" : session_state['timestamp']
            }
        )
        st.success("Data inserted successfully")
        st.write(
            inventory.find_one({"item_name" : session_state['item_name']},{"_id" : 0})
        )
else:
    st.warning("Provide all the values")

