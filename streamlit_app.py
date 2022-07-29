
import streamlit
import pandas

streamlit.title('My parents new healthy dinner')
streamlit.header('Breakfast menu')
streamlit.text('🍞 Oatmeal')
streamlit.text('🥑 Smootie')
streamlit.text('🐔 Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show=my_fruit_list.loc[fruits_selected]
# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
#New section to display fruitvice api response
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")
#streamlit.text(fruityvice_response.json()) #write the json data to screen as is
#take json response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#out the screen as table
streamlit.dataframe(fruityvice_normalized)



