# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom smoothie!"
)

name_on_order = st.text_input("Name On Smoothie")
st.write("Name on your smoothie will be ", name_on_order)

session = get_active_session();
fruit_option_df = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data = fruit_option_df, use_container_width = True) 

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients:",
    fruit_option_df, max_selections = 5
)

if ingredients_list:
    #st.write(ingredients_list)
    ingredients_string=""
    for i in ingredients_list:
        ingredients_string += i + ' '
    #st.write(ingredients_string)

    my_insert_statement = """insert into smoothies.public.orders (ingredients, name_on_order) values('"""+ingredients_string+"""','"""+name_on_order+"""');"""
    #st.write(my_insert_statement)
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_statement).collect()
        st.success('Your Smoothie is ordered! '+name_on_order, icon="✅")


