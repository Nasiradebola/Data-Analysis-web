import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def data_visualization_barchart(subheader, column, content, df):
    # Store DataFrame in session state
    st.session_state.df = df

    # Display subheader and content
    st.subheader(subheader)
    st.write(content)

    # Calculate value counts and percentages
    counts = df[column].value_counts()
    percentages = (counts / counts.sum()) * 100

    # Create the bar chart
    fig, ax = plt.subplots(figsize=(12, 10))
    percentages.plot(kind='bar', ax=ax, color='skyblue')

    # Set chart title and labels
    ax.set_title(subheader)
    ax.set_xlabel(column)
    ax.set_ylabel('Percentage (%)')

    # Add percentage labels on the bars
    for bar in ax.patches:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}%', 
                    (bar.get_x() + bar.get_width() / 2, height),
                    ha='center', va='bottom')

    # Display the chart in Streamlit
    st.pyplot(fig)


def data_visualization_barcharth(subheader, column, content, df):
    # Store DataFrame in session state
    st.session_state.df = df

    # Display subheader and content
    st.subheader(subheader)
    st.write(content)

    # Calculate value counts and percentages
    counts = df[column].value_counts()
    percentages = (counts / counts.sum()) * 100

    # Create a horizontal bar chart
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.barh(percentages.index, percentages.values, color='skyblue')

    # Set chart title and labels
    ax.set_title(subheader)
    ax.set_xlabel('Percentage (%)')
    ax.set_ylabel(column)

    # Add percentage labels on the bars
    for index, value in enumerate(percentages.values):
        ax.annotate(f'{value:.1f}%', 
                    (value, index), 
                    ha='left', va='center')

    # Display the chart in Streamlit
    st.pyplot(fig)


def data_visualization_piechart(subheader,column,content,df):
    st.session_state.df = df
    st.subheader(subheader)
    df_column = st.session_state.df[column].value_counts().sort_index()
    st.write(content)
    fig, ax = plt.subplots()
    ax.pie(df_column, labels=df_column.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

def data_visualization_doughnut_chart(subheader, column, content, df):
    st.session_state.df = df
    st.subheader(subheader)
    df_column = df[column].value_counts().sort_index()
    st.write(content)
    fig, ax = plt.subplots()
    ax.pie(
        df_column, labels=df_column.index,  autopct='%1.1f%%', startangle=90,
        wedgeprops={'width': 0.5}
    )
    ax.axis('equal')
    st.pyplot(fig)

def plot_bar_chart(df, group_cols, title, xlabel, ylabel):
    """
    Plots a bar chart based on grouping columns and displays it in Streamlit.

    Parameters:
    - df: DataFrame containing the data.
    - group_cols: List of columns to group by.
    - title: Title of the chart.
    - xlabel: Label for the x-axis.
    - ylabel: Label for the y-axis.
    """

    # Group the data and handle missing values
    grouped_data = df.groupby(group_cols)['Responders'].count().unstack(fill_value=0)

    # Display the grouped data
    st.subheader(title)
    st.write(grouped_data)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(13, 6))
    grouped_data.plot(kind='bar', ax=ax, width=0.8)

    # Set chart title and axis labels
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # Add percentage labels to bars
    total = grouped_data.values.sum()
    for bar in ax.patches:
        height = bar.get_height()
        if height > 0:
            percentage = (height / total) * 100
            ax.annotate(f'{percentage:.1f}%', 
                        (bar.get_x() + bar.get_width() / 2, height),
                        ha='center', va='bottom')

    # Adjust layout and display in Streamlit
    plt.tight_layout()
    st.pyplot(fig)