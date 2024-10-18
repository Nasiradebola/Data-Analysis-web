import pandas as pd
import streamlit as st
from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from analysis.data_visualization import data_visualization_barchart,data_visualization_piechart

def display_data_analysis(df):
   # st.header("Data Analysis")
    st.session_state.df = pd.DataFrame(df)
    
    # Sidebar selection for analysis type
    data_type = st.sidebar.selectbox(
        "Choose the type of analysis:",
        ["Select", "Data Inspection and Exploration", "Data Cleaning", "Analysing the Data", "Data Visualization"]
    )
    
    if data_type != "Select":
            st.write(f" {data_type}")

               # 1. Data Inspection and Exploration
            if data_type == "Data Inspection and Exploration":
                st.subheader("1. Basic Information:")
                buffer = StringIO()
                st.session_state.df.info(buf=buffer)
                info_str = buffer.getvalue()
                st.text(info_str)

                st.subheader("2. First Five Rows of the DataFrame:")
                st.dataframe(st.session_state.df.head())

                st.subheader("3. Last Five Rows of the DataFrame:")
                st.dataframe(st.session_state.df.tail())

                st.subheader("4. Checking for missing values:")
                missing_values = st.session_state.df.isnull().sum()
                missing_values = missing_values[missing_values > 0]
                if not missing_values.empty:
                    st.write("Columns with Missing Values:")
                    st.table(missing_values)
                else:
                    st.success("No missing values found in the DataFrame.")

                st.subheader("5. Handling Duplicate Rows")
                # Identify duplicates
                duplicates = st.session_state.df[st.session_state.df.duplicated(keep=False)]
                # Display message based on the presence of duplicates
                if not duplicates.empty:
                    st.warning(f"Duplicate rows found: {len(duplicates)}")
                else:
                    st.success("No duplicate rows found.")

             # 2. Data Cleaning
# Assume df is already loaded into session_state (or loaded earlier in your app)
    if 'df' not in st.session_state:
    # Load your DataFrame initially (replace with actual data loading)
        st.session_state.df = pd.DataFrame()  # Replace with real data

    elif data_type == "Data Cleaning":
            cleaning_type = st.selectbox(
                "Choose the type of data cleaning:",
                ["Select", "Empty Cells", "Wrong Data", "Remove Duplicates"]
            )

            if cleaning_type != "Select":
                st.write(f"### {cleaning_type}")

                # Empty Cells Handling
                if cleaning_type == "Empty Cells":
                    st.write("### Current Table")
                    st.dataframe(st.session_state.df)

                    handling_options = [
                        "Select", "Fill with a specific value", 
                        "Drop rows"]

                    handling_missing = st.selectbox("Select a method:", handling_options)

                    if handling_missing != "Select":
                        specific_value = None
                        if handling_missing == "Fill with a specific value":
                            specific_value = st.text_input("Enter the value to fill missing data with:")

                        if st.button("Apply Missing Value Handling"):
                            if handling_missing == "Drop rows":
                                initial_count = st.session_state.df.shape[0]
                                st.session_state.df.dropna(inplace=True)
                                removed_rows = initial_count - st.session_state.df.shape[0]
                                st.success(f"Dropped {removed_rows} rows with missing values.")

                            # elif handling_missing == "Fill with mean":
                            #     numeric_cols = st.session_state.df.select_dtypes(include=['float64', 'int64']).columns
                            #     st.session_state.df[numeric_cols] = st.session_state.df[numeric_cols].fillna(st.session_state.df[numeric_cols].mean())
                            #     st.success("Filled missing values with the mean.")

                            # elif handling_missing == "Fill with median":
                            #     numeric_cols = st.session_state.df.select_dtypes(include=['float64', 'int64']).columns
                            #     st.session_state.df[numeric_cols] = st.session_state.df[numeric_cols].fillna(st.session_state.df[numeric_cols].median())
                            #     st.success("Filled missing values with the median.")

                            # elif handling_missing == "Fill with mode":
                            #     mode_values = st.session_state.df.mode().iloc[0]
                            #     st.session_state.df = st.session_state.df.fillna(mode_values)
                            #     st.success("Filled missing values with the mode.")

                            elif handling_missing == "Fill with a specific value":
                                if specific_value:
                                    try:
                                        value = float(specific_value)
                                        if value.is_integer():
                                            value = int(value)
                                    except ValueError:
                                        value = specific_value

                                    st.session_state.df.fillna(value, inplace=True)
                                    st.success(f"Filled missing values with `{value}`.")
                                else:
                                    st.error("Please enter a value to fill missing data.")

                        # Display the updated DataFrame
                        st.write("### Updated DataFrame")
                        st.dataframe(st.session_state.df)

               # Handling Wrong Data
                elif cleaning_type == "Wrong Data":
                    st.write("### Current DataFrame")
                    st.dataframe(st.session_state.df)

                    # Allow the user to select the column with potential wrong data
                    column = st.selectbox("Select the column with wrong data:", st.session_state.df.columns)

                    # List unique values for user review and correction
                    st.write(f"Unique values in the '{column}' column:")
                    unique_values = st.session_state.df[column].unique()
                    st.write(unique_values)

                    # Option to replace wrong values interactively
                    wrong_value = st.text_input("Enter the wrong value to replace:")
                    correct_value = st.text_input("Enter the correct value:")

                    if st.button("Apply Value Replacement"):
                        if wrong_value and correct_value:
                            st.session_state.df[column] = st.session_state.df[column].replace(wrong_value, correct_value)
                            st.success(f"Replaced '{wrong_value}' with '{correct_value}'.")

                        else:
                            st.error("Please enter both the wrong and correct values.")

                    # Option to remove specific unwanted values
                    remove_value = st.text_input("Enter a value to remove from the column:")

                    if st.button("Remove Value"):
                        if remove_value:
                            initial_count = st.session_state.df.shape[0]
                            st.session_state.df = st.session_state.df[st.session_state.df[column] != remove_value]
                            removed_count = initial_count - st.session_state.df.shape[0]
                            st.success(f"Removed {removed_count} rows containing '{remove_value}' in the '{column}' column.")
                        else:
                            st.error("Please enter a value to remove.")


                # Remove Duplicates
                elif cleaning_type == "Remove Duplicates":
                    st.subheader("Handling Duplicates: Drop Duplicate Rows")
                    st.write("### Current DataFrame")
                    st.dataframe(st.session_state.df)

                    if st.button("Drop Duplicates"):
                        initial_count = st.session_state.df.shape[0]
                        st.session_state.df.drop_duplicates(inplace=True)
                        removed_duplicates = initial_count - st.session_state.df.shape[0]
                        st.success(f"Dropped {removed_duplicates} duplicate rows.")

                    st.write("### Updated DataFrame with Duplicates Removed")
                    st.dataframe(st.session_state.df)

            # 3. Analyzing the Data
    elif data_type == "Analysing the Data":
                st.subheader("1. Total Number of Responses")
                total_number_responses = st.session_state.df['Responders'].count()
                st.write("Total number of responses:", total_number_responses)

                st.subheader("2. Age Distribution")
                age_distribution = st.session_state.df['Age'].value_counts().sort_index()
                st.write(age_distribution)

                st.subheader("3. Gender Distribution")
                gender_distribution = st.session_state.df['Gender'].value_counts()
                st.write(gender_distribution)

                st.subheader("4. Year of Study Distribution")
                year_of_study_distribution = st.session_state.df['Current year of study'].value_counts().sort_index()
                st.write(year_of_study_distribution)

                st.subheader("5. Course of Study Distribution")
                course_distribution = st.session_state.df['Course'].value_counts()
                st.write(course_distribution)

                st.subheader("6. Communication Methods Distribution")
                communication_methods = st.session_state.df['Communication methods'].value_counts()
                st.write(communication_methods)

                st.subheader("7. Accommodation and Year of Study Distribution")
                accommodation_and_year = st.session_state.df.groupby('Accommodation for your studies')['Responders'].count()
                st.write(accommodation_and_year)

                st.subheader("8. Location and Year of Study Distribution")
                location_and_year = st.session_state.df.groupby(['Location', 'Current year of study'])['Responders'].count()
                st.write("Total number of users by location and year of study:")
                st.write(location_and_year)

                st.subheader("9. Interpreter Availability for Classes")
                interpreter_availability = st.session_state.df.groupby(['Accessibility of Interpreters', 
                                                            'Current year of study'])['Responders'].count()
                st.write("Total number of users by interpreter availability for classes:")
                st.write(interpreter_availability)

                st.subheader("10. Understanding Lectures with Interpreters")
                lecture_understanding = st.session_state.df.groupby(['Understanding Lectures with Interpreters', 
                                                            'Current year of study'])['Responders'].count()
                st.write("Total number of users by interpreter effectiveness:")
                st.write(lecture_understanding)

                st.subheader("11. Interpreter Understanding of Sign Language")
                sign_language_understanding = st.session_state.df.groupby(['Interpreter Understanding of Sign Language', 
                                                                'Current year of study'])['Responders'].count()
                st.write("Total number of users by interpreter sign language understanding:")
                st.write(sign_language_understanding)

                st.subheader("12. Consistency of Interpreters in Classes")
                interpreter_consistency = st.session_state.df.groupby(['Consistency of Interpreters in classes', 
                                                            'Current year of study'])['Responders'].count()
                st.write("Total number of users by interpreter consistency:")
                st.write(interpreter_consistency)

                st.subheader("13. Interpreters for Understanding Course Material")
                course_material_help = st.session_state.df.groupby(['Interpreters for understanding the course material', 
                                                        'Current year of study'])['Responders'].count()
                st.write("Total number of users by course material assistance:")
                st.write(course_material_help)

                st.subheader("14. Interpreters for Academic Activities Outside Class")
                academic_activities_help = st.session_state.df.groupby(['Interpreters for Academic Activies Outsides Class', 
                                                            'Current year of study'])['Responders'].count()
                st.write("Total number of users by academic activities assistance:")
                st.write(academic_activities_help)

                st.subheader("15. Interpreters support outside class")
                assignments_help = st.session_state.df.groupby(['Interpreters support outside class', 
                                                    'Current year of study'])['Responders'].count()
                st.write("Total number of users by assistance with assignments:")
                st.write(assignments_help)

                st.subheader("16. Rating the Quality of the Sign Language Interpreters")
                interpreter_quality = st.session_state.df.groupby(['Rating the Quality of the Sign Language Interpreters', 
                                                        'Current year of study'])['Responders'].count()
                st.write("Total number of users by interpreter quality rating:")
                st.write(interpreter_quality)

                st.subheader("17. Satisfaction with Interpreter Services")
                satisfaction = st.session_state.df.groupby(['Satisfaction with Interpreter services', 
                                                'Current year of study'])['Responders'].count()
                st.write("Total number of users by satisfaction with interpreter services:")
                st.write(satisfaction)




            # 4. Data Visualization
    elif data_type == "Data Visualization":
                st.write("Using the latest cleaned dataset for visualization.")

                # 1. Age Distribution (Pie Chart)
                data_visualization_piechart(
                    "1. Age Distribution", 
                    'Age', 
                    "Total number of users by age:", 
                    st.session_state.df
                )

                # 2. Gender Distribution (Pie Chart)
                data_visualization_piechart(
                    "2. Gender Distribution", 
                    'Gender', 
                    "Total number of users by gender:", 
                    st.session_state.df
                )

                # 3. Year of Study Distribution (Pie Chart)
                data_visualization_piechart(
                    "3. Year of Study Distribution", 
                    'Current year of study?', 
                    "Total number of users by year of study:", 
                    st.session_state.df
                )

                # 4. Course of Study Distribution (Bar Chart)
                data_visualization_barchart(
                    "4. Course of Study Distribution", 
                    "Course", 
                    "Total number of users by course of study:", 
                    st.session_state.df
                )

                # 5. Communication Methods Distribution (Bar Chart)
                data_visualization_barchart(
                    "5. Communication Methods Distribution", 
                    'Communication methods', 
                    "Total number of users by communication methods:", 
                    st.session_state.df
                )

                # 6. Accommodation and Year of Study Distribution (Bar Chart)
                data_visualization_barchart(
                    "6. Accommodation and Year of Study Distribution", 
                    'Accommodation for your studies', 
                    "Total number of users by accommodation type:", 
                    st.session_state.df
                )
