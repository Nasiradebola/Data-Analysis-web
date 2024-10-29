import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from analysis.data_analysis import display_data_analysis
from analysis.descriptive_analysis import display_descriptive_analysis
from analysis.diagnostic_analysis import display_diagnostic_analysis
from analysis.prescriptive_analysis import display_prescriptive_analysis

def loading():
    uploaded_file = st.file_uploader("upload your file", type=['csv','xls','xlsx','json','sql'])
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split('.')[-1]
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xls','xlsx']:
            df = pd.read_excel(uploaded_file)
        elif file_extension == 'json':
            df = pd.read_json(uploaded_file)
        elif file_extension == 'sql':
            df = pd.read_sql(uploaded_file)
        else:
            st.error("Unsupported file format")
            return None
        st.success(f"File  successfully loaded: {uploaded_file.name}")
        return df
    else:
        st.warning("warning upload a file to proceed.")
        return None


st.sidebar.title("Institution Interpreter Services Survey Analysis")

df = loading()

# Add options to choose the type of analysis using Streamlit's selectbox
analysis_type = st.sidebar.selectbox(
    "Choose the type of analysis:",
    ["Select", "Data Analysis", "Descriptive Analysis", "Diagnostic Analysis", "Prescriptive Analysis"]
)

# Based on the user selection, perform the analysis
if  analysis_type != "Select":
    st.write(f"### {analysis_type}")
    
    if analysis_type == "Data Analysis":
        display_data_analysis(df)
    elif analysis_type == "Descriptive Analysis":
        display_descriptive_analysis(df)
    elif analysis_type == "Diagnostic Analysis":
        display_diagnostic_analysis(df)
    elif analysis_type == "Prescriptive Analysis":
        display_prescriptive_analysis(df)
else:
    st.write("Please upload data and choose an analysis type.")