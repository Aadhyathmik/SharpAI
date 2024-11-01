import streamlit as st
import openai
import PyPDF2 
from PIL import Image

def count_words(text):
    if text:
        return len(text.split())
    return 0

def add_space(n=1):
  for _ in range(n):
    st.sidebar.text(" ")

# Initialize OpenAI with your API key
secret_key = st.secrets["openapi"]["openapi_key"]
openai.api_key = secret_key
model_input = "gpt-4o-mini" #"gpt-4"  # Adjust to "gpt-4", "gpt-3.5-turbo" as needed

##Initialize
st.sidebar.image("Essbot3.jpg", use_column_width=True)
st.sidebar.divider()
lnkd_profile_url="https://www.linkedin.com/in/rajvarahagiri/"
st.sidebar.markdown("[Rajkumar Varahagiri](%s)" % lnkd_profile_url)  
st.sidebar.title("Welcome")
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.header("This is a restricted version of Essay Bot AI. Can't be used or reproduced without the author's permission.")
st.sidebar.text(" ")
st.sidebar.text(" ")
add_space(5)
tos="https://graderbotai.com/terms-and-conditions/"
pp="https://graderbotai.com/privacy-policy/"

st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.markdown("[Terms of Service](%s)" % tos)  
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.markdown("[Privacy Policy](%s)" % pp)  

image_path="Essbot3.jpg"
image = Image.open(image_path)
#st.image(image_file, width=300)
#link_url="https://graderbotai.com/"

st.markdown(
    """
    <style>
    .centered-image {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#st.image(image_file, use_column_width=False, width=300)  # Adjust width as needed
#st.markdown('</div>', unsafe_allow_html=True)


st.title("ESSBOT College Essay Companion")
st.divider()

sample_essay = """I witnessed how powerful Python coding language is. I learned it and created a small project.
    I want to take advanced computer science and use technology to solve real-world problems.
    Using new technologies, we can tackle issues in education, farming, and other areas.

    I participated in my computer science club at my school, where we learned collaboratively.
    We also talked to many tech professionals to understand what they are currently working on.

    I once participated in a hackathon where the theme was how we can make use of solar energy. I joined a team and built a prototype. It was so much fun."""

sample_prompt="Why do you want to study your chosen major and why do you want to study your major in this university"

sample_words = 300


# Input text area for custom prompt
st.markdown("**Enter the Essay Prompt:**")
#st.markdown("<h4 style='margin-bottom: 0;'>**Enter the Essay Prompt:**</h4>", unsafe_allow_html=True)
user_prompt = st.text_area("", value=sample_prompt)

# Input text area for custom prompt
#essay_words = st.text_area("Max Essay Word Count:", value=sample_words)

essay_words_min_value = 0
essay_words_max_value = 1000
essay_words_initial_value = 300

col1, col2,col3 = st.columns(3)
with col1:
    st.markdown("**Max Essay Word Count:**")
    essay_words = st.number_input("", min_value=essay_words_min_value, max_value=essay_words_max_value, value=essay_words_initial_value)

# Create a slider
#slider_value = st.slider("Max Essay Word Count:", min_value=essay_words_min_value, max_value=essay_words_max_value, value=essay_words_initial_value)

# Create a number input, initialized to the slider's value
#essay_words = st.number_input("Max Essay Word Count:", min_value=essay_words_min_value, max_value=essay_words_max_value, value=slider_value)

# Optional: Update the number input value when the slider changes
#if slider_value != essay_words:
#    essay_words = slider_value

# Update the slider value based on the number input
#if essay_words != st.session_state.slider_value:
#    st.session_state.slider_value = essay_words

# Input text area for essay paragraph
st.markdown("**Enter your essay paragraph here:**")
essay = st.text_area("", height=300, value=sample_essay)


# Step 1: Initialize the button state in session state if not already present
if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False  # Button starts as enabled



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
    },
    "UCLA": {
        "mission": "To create, disseminate, preserve, and apply knowledge for the betterment of our global society.",
        "vision": "UCLA strives to be a public research university committed to excellence, inclusivity, and service."
    },
    "UCSD": {
        "mission": "To transform California and a diverse global society by educating, generating, and disseminating knowledge and creative works.",
        "vision": "UCSD aspires to be a student-centered, research-focused, service-oriented public university."
    },
    "UC Berkeley": {
        "mission": "To generate, disseminate, preserve, and apply knowledge to advance the human condition globally.",
        "vision": "UC Berkeley’s vision is to be a premier research institution that impacts society positively through knowledge and discovery."
    },
    "UCSB": {
        "mission": "To promote knowledge through research, teaching, and creativity, serving California, the nation, and the world.",
        "vision": "UCSB aspires to foster academic excellence and social responsibility as a leading research university."
    },
    "UIUC": {
        "mission": "To enhance the lives of citizens in Illinois, across the nation, and around the world through leadership in learning, discovery, engagement, and economic development.",
        "vision": "UIUC aims to be a preeminent public research university with a transformative societal impact."
    },
    "UT Austin": {
        "mission": "To achieve excellence in the interrelated areas of undergraduate education, graduate education, research, and public service.",
        "vision": "UT Austin’s vision is to be a world-class university that educates leaders and generates knowledge for societal benefit."
    },
    "Carnegie Mellon": {
        "mission": "To create a transformative educational experience that develops leaders and innovators to solve global challenges.",
        "vision": "Carnegie Mellon envisions a world where knowledge is at the service of society and advances the human condition."
    },
    "Purdue": {
        "mission": "To provide an education that combines rigorous academic study and the excitement of discovery with the support and intellectual stimulation of a diverse campus community.",
        "vision": "Purdue strives to be a global leader in engineering, technology, and sciences, driving impactful research and learning."
    }
}


# Set a default index for the selectbox
default_index1 = list(college_data.keys()).index("MIT")  # Default to "MIT"

# Set a default index for the selectbox
default_index2 = list(college_data.keys()).index("Harvard")  # Default to "Harvard"

m = st.markdown("""
<style>
    /* Normal button style */
    div.stButton > button:first-child {
        background-color: #333333; /* Dark Gray */
        color: #FFFFFF;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 20px;
    }
    /* Hover effect */
    div.stButton > button:hover {
        background-color: #555555; /* Lighter Dark Gray on hover */
        color: #FFFFFF;
    }
    /* Disabled button style */
    div.stButton > button:disabled {
        background-color: #A9A9A9; /* Medium Gray for disabled */
        color: #D3D3D3; /* Light Gray text for disabled */
    }
    </style>
    """, unsafe_allow_html=True)

# Dropdown for college selection
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Choose a college:**")
    college1 = st.selectbox("Select college:", list(college_data.keys()), index=default_index1)

    if college1:
        st.subheader(f"{college1} Mission")
        st.write(college_data[college1]["mission"])
        st.subheader(f"{college1} Vision")
        st.write(college_data[college1]["vision"])

with col2:
    st.markdown("**Choose a college:**")
    college2 = st.selectbox("", list(college_data.keys()), index=default_index2)

    if college2:
        st.subheader(f"{college2} Mission")
        st.write(college_data[college2]["mission"])
        st.subheader(f"{college2} Vision")
        st.write(college_data[college2]["vision"])

col1.write("")  # Blank line to push content down if needed
col2.write("")


col3, col4, col5 = st.columns(3)
with col4 :
    submit_button = st.button('Revise Essay',use_container_width=True)
    

# Dropdown for college selection
#college1 = st.selectbox("Select the first college:", list(college_data.keys()), index=default_index1)
#college2 = st.selectbox("Select the second college:", list(college_data.keys()), index=default_index2)



# Function to modify essay using OpenAI ChatCompletion API
def get_modified_essay(essay, mission, vision, user_prompt):
    try:
        client = openai.Client(api_key=secret_key)
        response = client.chat.completions.create(
            model=model_input,
            messages=[
                {"role": "system", "content": "You are an assistant that helps revise college essays to better align with college missions, visions, and user-provided prompts."},
                {"role": "user", "content": f"Here is a college essay written by a student:\n\nEssay: {essay}\n\nThe mission of the college is: {mission}\nThe vision of the college is: {vision}\n\nUser-Provided Prompt: {user_prompt}\n\nPlease revise the essay to align with the mission, vision, and user provided prompt, making it more compelling for the admissions committee. Please restrict the length of the essay to strictly {essay_words} words."}
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

    
    
def main():
    """ The main function that handles the Streamlit app logic.  """

   
    # Button to generate revised essays
    #if st.button("Revise Essay for Selected Colleges"):
    if submit_button:
        progress_placeholder = st.empty()
        progress_placeholder.text("Putting in the Oven...")
        with st.spinner("Making the Recipe..."):
            st.session_state.button_disabled = True
            # Get the mission and vision for each selected college
            mission1 = college_data[college1]["mission"]
            vision1 = college_data[college1]["vision"]

            mission2 = college_data[college2]["mission"]
            vision2 = college_data[college2]["vision"]

            # Call OpenAI API to revise essay for each college with custom prompt
            message_placeholder = "Finetuning for College " + college1 + "..."
            progress_placeholder.text(message_placeholder)
            revised_essay_college1 = get_modified_essay(essay, mission1, vision1, user_prompt)
            message_placeholder = "Finetuning for College " + college2 + "..."
            progress_placeholder.text(message_placeholder)
            #progress_placeholder.text("Preparing for ...")
            revised_essay_college2 = get_modified_essay(essay, mission2, vision2, user_prompt)
            progress_placeholder.text("")
            message = (
            f"🎓✨ Congratulations! Your essay has been successfully revised for "
            f"**{college1} and {college2} **! 🎉\n\n"
            "Your hard work is about to pay off, and we can't wait to see you shine! "
            "Take a moment to review the changes, make edits as necessary and prepare to submit your masterpiece! 🚀"
            )
            st.success(message)
    else:
        # Initial placeholder text
        revised_essay_college1 = "Your revised essay will appear here."
        revised_essay_college2 = "Your revised essay will appear here."

    
    # Display the output text boxes in two side-by-side columns with unique keys
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Revised Essay for \n {college1}")
        st.text_area(f"", revised_essay_college1, height=600, disabled=True, key="revised_essay1")
        
    with col2:
        st.subheader(f"Revised Essay for \n{college2}")
        st.text_area(f"", revised_essay_college2, height=600, disabled=True, key="revised_essay2")

    st.session_state.button_disabled = False

# Runs program
if __name__ == "__main__":
  main()
