import streamlit as st
import matplotlib.pyplot as plt

def data_visualization_barchart(subheader,column,content,df):
    st.session_state.df = df
    st.subheader(subheader)
    df_column = st.session_state.df[column].value_counts()
    st.write(content)
    st.bar_chart(df_column)


def data_visualization_piechart(subheader,column,content,df):
    st.session_state.df = df
    st.subheader(subheader)
    df_column = st.session_state.df[column].value_counts().sort_index()
    st.write(content)
    fig, ax = plt.subplots()
    ax.pie(df_column, labels=df_column.index, autopct='%1.1f%%', startangle=90)
    # ax.legend()
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle
    st.pyplot(fig)
