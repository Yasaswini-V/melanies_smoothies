# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want to in your custom smoothie
    """)

cnx=st.connection("snowflake")
session = cnx.session()

name_on_order=st.text_input("Name on Smoothies: ")
st.write("The name of your Smoothies will be:",name_on_order)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(my_dataframe,use_container_width=True)
# st.stop()
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredient_list=st.multiselect("Choose up to 5 ingredients:",my_dataframe,max_selections=5)
if ingredient_list:
    ingredients_string=''
    for fruit in ingredient_list:
        ingredients_string+=fruit+' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        st.subheader(fruit+' Nutrition Infromation')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit)
        fv_df=st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+ name_on_order +"""')"""
    
    # st.write(my_insert_stmt)
    time_to_submit=st.button("Submit Order")
    if time_to_submit:
        session.sql(my_insert_stmt).collect()
        st.success(f'Your Smoothie is ordered,{name_on_order}!', icon="✅")

