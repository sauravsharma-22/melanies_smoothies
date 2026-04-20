# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests  
import pandas

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom smoothie!"
)

name_on_order = st.text_input("Name On Smoothie")
st.write("Name on your smoothie will be ", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()

fruit_option_df = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'),col('SEARCH_ON'))


pd_df = fruit_option_df.to_pandas()
#st.dataframe(pd_df) 
#st.stop()

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    fruit_option_df, max_selections = 5
)

if ingredients_list:
    
    ingredients_string=""
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      
        st.subheader(fruit_chosen + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)  
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

       

    my_insert_statement = """insert into smoothies.public.orders (ingredients, name_on_order) values('"""+ingredients_string+"""','"""+name_on_order+"""');"""
    #st.write(my_insert_statement)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_statement).collect()
        st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")



