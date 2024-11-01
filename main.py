import streamlit as st
import openai
import PyPDF2

import streamlit as st

# Sample list of colleges
college_list = ["Harvard", "Stanford", "MIT", "UC Berkeley", "University of Chicago"]

# Function to revise essay based on college
def revise_essay_for_college(essay, college):
    # Sample revision logic based on college
    if college == "Harvard":
        return essay + " This paragraph highlights the student's passion for Harvard's unique liberal arts approach."
    elif college == "Stanford":
        return essay + " This paragraph emphasizes the student's alignment with Stanford's entrepreneurial culture."
    elif college == "MIT":
        return essay + " The student underscores their interest in MIT's technological innovation."
    elif college == "UC Berkeley":
        return essay + " This essay aligns with Berkeley’s focus on social impact and research."
    elif college == "University of Chicago":
        return essay + " Here, the student showcases an appreciation for Chicago's interdisciplinary studies."
    else:
        return essay + " No specific college revision available."

# Streamlit app layout
st.title("College Essay Revision Tool")

# Input text area for essay paragraph
essay = st.text_area("Enter your essay paragraph here:")

# Dropdown for college selection
college1 = st.selectbox("Select the first college:", college_list)
college2 = st.selectbox("Select the second college:", college_list)

# Button to generate revised essays
if st.button("Revise Essay for Selected Colleges"):
    # Display revised essays in two side-by-side read-only text boxes
    revised_essay_college1 = revise_essay_for_college(essay, college1)
    revised_essay_college2 = revise_essay_for_college(essay, college2)

    # Set up side-by-side columns for the output text boxes
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Revised Essay for {college1}")
        st.text_area(f"Revised Essay for {college1}", revised_essay_college1, height=150, disabled=True)
    
    with col2:
        st.subheader(f"Revised Essay for {college2}")
        st.text_area(f"Revised Essay for {college2}", revised_essay_college2, height=150, disabled=True)
