import streamlit as st
import openai
import PyPDF2

import streamlit as st
import openai

# Initialize OpenAI with your API key
secret_key = st.secrets["openapi"]["openapi_key"]
openai.api_key = secret_key

# Sample list of colleges with mission and vision statements
college_data = {
    "Harvard": {
        "mission": "To educate the citizens and citizen-leaders for our society.",
        "vision": "Harvard’s mission is to advance new ideas and promote discovery in an ever-changing world."
    },
    "Stanford": {
        "mission": "To promote the public welfare by exercising an influence in behalf of humanity and civilization.",
        "vision": "Stanford prepares students to think critically and contribute to society."
    },
    "MIT": {
        "mission": "To advance knowledge and educate students in science, technology, and other areas.",
        "vision": "MIT’s mission is to serve the nation and the world by advancing knowledge."
    }
    # Add more colleges as needed
}

# Function to modify essay using OpenAI API
def get_modified_essay(essay, mission, vision):
    prompt = f"""
    Here is a college essay written by a student:

    Essay: {essay}

    The mission of the college is: {mission}
    The vision of the college is: {vision}

    Please revise the essay to align with the mission and vision of the college. Make it more compelling for the admissions committee.
    """

    response = openai.Completion.create(
        engine="text-davinci-003",  # Use "gpt-3.5-turbo" or other available models
        prompt=prompt,
        max_tokens=250,
        temperature=0.7
    )

    return response.choices[0].text.strip()

# Streamlit app layout
st.title("College Essay Revision Tool with OpenAI")

# Input text area for essay paragraph
essay = st.text_area("Enter your essay paragraph here:")

# Dropdown for college selection
college1 = st.selectbox("Select the first college:", list(college_data.keys()))
college2 = st.selectbox("Select the second college:", list(college_data.keys()))

# Button to generate revised essays
if st.button("Revise Essay for Selected Colleges"):
    # Get the mission and vision for each selected college
    mission1 = college_data[college1]["mission"]
    vision1 = college_data[college1]["vision"]

    mission2 = college_data[college2]["mission"]
    vision2 = college_data[college2]["vision"]

    # Call OpenAI API to revise essay for each college
    revised_essay_college1 = get_modified_essay(essay, mission1, vision1)
    revised_essay_college2 = get_modified_essay(essay, mission2, vision2)
else:
    # Initial placeholder text
    revised_essay_college1 = "Your revised essay will appear here."
    revised_essay_college2 = "Your revised essay will appear here."

# Display the output text boxes in two side-by-side columns with unique keys
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Revised Essay for {college1}")
    st.text_area(f"Revised Essay for {college1}", revised_essay_college1, height=150, disabled=True, key="revised_essay1")
    
with col2:
    st.subheader(f"Revised Essay for {college2}")
    st.text_area(f"Revised Essay for {college2}", revised_essay_college2, height=150, disabled=True, key="revised_essay2")
