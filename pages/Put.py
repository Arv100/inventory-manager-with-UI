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
session_state = st.session_state

st.header("Update Collection")
st.divider()

st.text_input('Item Name',key='item_name')

if session_state['item_name'] != "":
    result = inventory.find_one({"item_name" : session_state['item_name']})
    if not result:
        st.error('Item not found')
    else:
        st.write(
            inventory.find_one({"item_name" : session_state['item_name']},{"_id" : 0})
        )
        col1, col2 = st.columns([.5,.5])
        with col2:
            st.text_input('Item Brand',key='item_brand')
            st.markdown('<br>',unsafe_allow_html=True)
            update = st.button('Update')
        with col1:
            st.number_input('Item Quantity',key='item_quantity',step=1)
            st.number_input('Item Price',key='item_price',step=1)

if update:
    if session_state['item_brand'] != "" and session_state['item_price'] != 0 and session_state['item_quantity'] != 0:
        inventory.update_one(
            {
                "item_name" : session_state['item_name'],
            },
            {"$set" : {
                "item_brand" : session_state['item_brand'],
                "item_price" : session_state['item_price'],
                "item_quantity" : session_state['item_quantity'],
                "inserted_timestamp" : session_state['timestamp']
            }}
        )
        st.success("Data Updated successfully")
        st.write(
            inventory.find_one({"item_name" : session_state['item_name']},{"_id" : 0})
        )
    else:
        if session_state['item_brand'] != "":
            inventory.update_one(
                {
                    "item_name" : session_state['item_name'],
                },
                {"$set" : {
                    "item_brand" : session_state['item_brand']
                }})
            st.success("Data Updated successfully")
            st.write(
                inventory.find_one({"item_name" : session_state['item_name']},{"_id" : 0})
            )
        if session_state['item_price'] != 0:
            inventory.update_one(
                {
                    "item_name" : session_state['item_name'],
                },
                {"$set" : {
                    "item_price" : session_state['item_price']
                }})
            st.success("Data Updated successfully")
            st.write(
                inventory.find_one({"item_name" : session_state['item_name']},{"_id" : 0})
            )
        if session_state['item_quantity'] != 0:
            inventory.update_one(
                {
                    "item_name" : session_state['item_name'],
                },
                {"$set" : {
                    "item_quantity" : session_state['item_quantity']
                }})
            st.success("Data Updated successfully")
            st.write(
                inventory.find_one({"item_name" : session_state['item_name']},{"_id" : 0})
            )
