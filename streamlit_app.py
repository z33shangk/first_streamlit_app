
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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
#streamlit.write('The user entered ', fruit_choice)

#New section to display fruitvice api response
#streamlit.text(fruityvice_response.json()) #write the json data to screen as is
#take json response and normalize it
#out the screen as table
#Create the repeatable code block(called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
   back_from_function=get_fruityvice_data(fruit_choice)
   streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

#56my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#57my_data_row = my_cur.fetchone()
#59streamlit.text("Hello from Snowflake:")
#60streamlit.text(my_data_row)
#fetch secrets from streamlit variables

my_data_row = my_cur.fetchall()
streamlit.text("The fruit load list contains")
#Snowflake-related functions
def get_fruit_load_list():
  with my_cnx_cursor as my_cur:
    my_cur.execute("SELECT * from FRUIT_LOAD_LIST")
    return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_row = get_fruit_load_list()
  streamlit.dataframe(my_data_row)

#donot run anything until we troubleshoot
streamlit.stop()
#Allow the end user to add fruit to the list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding', add_my_fruit)
#insert picklist fruit to SF database
my_cur.execute("insert into fruit_load_list values('from streamlit')")



