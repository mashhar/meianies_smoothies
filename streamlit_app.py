# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothies :cup_with_straw:")
st.write(
  """Choose the Fruits you want in your customize Smoothies!
  """
)


title = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", title)

cnx=st.connection("snowflake", type="snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#conver the snowpark dataframe to the Panda dataframe so we can use the LOC function
pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()

ingredient_list = st.multiselect(
    'Chose upto 5 ingredients:'
    , my_dataframe
    , max_selections=5
)

if ingredient_list:
    #st.write(ingredient_list)
    #st.text(ingredient_list)
    ingredients_string=''
    for fruit_chosen in ingredient_list:
        ingredients_string+=fruit_chosen +' '
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')  
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+title+ """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(f"Your Smoothie is ordered {title}!", icon="✅")





