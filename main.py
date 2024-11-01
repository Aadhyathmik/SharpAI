import streamlit as st
import openai
import PyPDF2


# Initialize OpenAI with your API key
secret_key = st.secrets["openapi"]["openapi_key"]
openai.api_key = secret_key
model_input = "gpt-4"  # Adjust to "gpt-4", "gpt-3.5-turbo" as needed

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
def get_modified_essay(essay, mission, vision, user_prompt):
    try:
        client = openai.Client(api_key=secret_key)
        response = client.chat.completions.create(
            model=model_input,
            messages=[
                {"role": "system", "content": "You are an assistant that helps revise college essays to better align with college missions, visions, and user-provided prompts."},
                {"role": "user", "content": f"Here is a college essay written by a student:\n\nEssay: {essay}\n\nThe mission of the college is: {mission}\nThe vision of the college is: {vision}\n\nUser-Provided Prompt: {user_prompt}\n\nPlease revise the essay to align with the mission, vision, and user provided prompt, making it more compelling for the admissions committee."}
            ],
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        msg = response.choices[0].message.content
        return msg
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

sample_prompt="Why do you want to study your chosen major and why do you want to study your major in this university"

# Input text area for custom prompt
user_prompt = st.text_area("Enter the Essay Prompt:", value=sample_prompt)

# Input text area for essay paragraph
essay = st.text_area("Enter your essay paragraph here:", height=300, value=sample_essay)



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

    # Call OpenAI API to revise essay for each college with custom prompt
    revised_essay_college1 = get_modified_essay(essay, mission1, vision1, user_prompt)
    revised_essay_college2 = get_modified_essay(essay, mission2, vision2, user_prompt)
else:
    # Initial placeholder text
    revised_essay_college1 = "Your revised essay will appear here."
    revised_essay_college2 = "Your revised essay will appear here."

# Display the output text boxes in two side-by-side columns with unique keys
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Revised Essay for {college1}")
    st.text_area(f"Revised Essay for {college1}", revised_essay_college1, height=600, disabled=True, key="revised_essay1")
    
with col2:
    st.subheader(f"Revised Essay for {college2}")
    st.text_area(f"Revised Essay for {college2}", revised_essay_college2, height=600, disabled=True, key="revised_essay2")
