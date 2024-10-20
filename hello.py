import streamlit as st

# Text Elements
st.title("NasFoodies")
st.header("Welcome to FoodNas")
st.subheader("odgugefoeffh28t32ru2w23rwd33")
st.write("cghddxcy6esguirr6e")


# Display data
data = {
    'name': ['Nasir', 'Victor', 'Abubakar'],
    'age': [23,45,36]
}
st.dataframe(data)
st.table(data)

#Widget
age =