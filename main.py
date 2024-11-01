import streamlit as st
import openai
import PyPDF2

import streamlit as st
import openai

# Initialize OpenAI with your API key
secret_key = st.secrets["openapi"]["openapi_key"]
openai.api_key = secret_key
model_input="gpt-4o" # "gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"

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

# Function to modify essay using OpenAI ChatCompletion API
def get_modified_essay(essay, mission, vision):
    try:
        client = openai.Client(api_key=secret_key)
        response = client.chat.completions.create(
          model= model_input,
          messages=[
                {"role": "system", "content": "You are an assistant that helps revise college essays to better align with college missions and visions."},
                {"role": "user", "content": f"Here is a college essay written by a student:\n\nEssay: {essay}\n\nThe mission of the college is: {mission}\nThe vision of the college is: {vision}\n\nPlease revise the essay to align with the mission and vision of the college. Make it more compelling for the admissions committee."}
          ],
          temperature=1,
          max_tokens=1000,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0,
        )
        msg = response.choices[0].message.content
        return msg
        #if 'choices' in response and response['choices']:
        #    return response['choices'][0]['message']['content'].strip()
        #else:
        #    return "Error: The response from OpenAI was empty or in an unexpected format."
    except Exception as e:
        return f"Error: {str(e)}"
# Streamlit app layout
st.title("College Essay Revision Tool with OpenAI")

sample_essay = """I witnessed how powerful Python coding language is. I learned it and created a small project.
I want to take advanced computer science and use technology to solve real-world problems.
Using new technologies, we can tackle issues in education, farming, and other areas.

I participated in my computer science club at my school, where we learned collaboratively.
We also talked to many tech professionals to understand what they are currently working on.

I once participated in a hackathon where the theme was how we can make use of solar energy. I joined a team and built a prototype. It was so much fun."""


# Input text area for essay paragraph
essay = st.text_area("Enter your essay paragraph here:",height=300,value=sample_essay)

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
    st.text_area(f"Revised Essay for {college1}", revised_essay_college1, height=600, disabled=True, key="revised_essay1")
    st.markdown(
        f"""
        <button onclick="navigator.clipboard.writeText(`{revised_essay_college1}`)" style="margin-top: 10px;">Copy Text</button>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.subheader(f"Revised Essay for {college2}")
    st.text_area(f"Revised Essay for {college2}", revised_essay_college2, height=600, disabled=True, key="revised_essay2")
    st.markdown(
        f"""
        <button onclick="navigator.clipboard.writeText(`{revised_essay_college2}`)" style="margin-top: 10px;">Copy Text</button>
        """,
        unsafe_allow_html=True
    )