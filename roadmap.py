import streamlit as st
from prompts import ai_roadmap_prompt
from groq import Groq
from fpdf import FPDF
from datetime import datetime
from dotenv import load_dotenv
import os
import re

# Load environment variables (API key)
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load Galaxy theme
with open("galaxy_theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Streamlit page config
st.set_page_config(page_title="raha.ai", layout='wide')
st.title("💫 raha.ai")
st.caption("You start. We guide.")

# Session state
if "response_text" not in st.session_state:
    st.session_state.response_text = ""

if "unlocked_weeks" not in st.session_state:
    st.session_state.unlocked_weeks = 1

if "task_checkboxes" not in st.session_state:
    st.session_state.task_checkboxes = {}

if "reflection_submitted" not in st.session_state:
    st.session_state.reflection_submitted = {}

if "streak" not in st.session_state:
    st.session_state.streak = 0

# Input box
user_input = st.text_input("🔍 Kis raha par chalna chahte hain? ")

# Generate roadmap
if st.button("Raha Dikhaiye"):
    if user_input.strip():
        with st.spinner("Generating roadmap..."):
            prompt = ai_roadmap_prompt.format(topic=user_input)
            chat_completion = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful AI roadmap generator."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.session_state.response_text = chat_completion.choices[0].message.content
            st.session_state.unlocked_weeks = 1
            st.session_state.task_checkboxes = {}
            st.session_state.reflection_submitted = {}
            st.session_state.streak = 0

# Extract weeks from text
def extract_weeks(text):
    pattern = r"(Week \d+[\s\S]*?)(?=(Week \d+)|$)"
    matches = re.findall(pattern, text)
    return [match[0].strip() for match in matches]

# Save roadmap as PDF
def save_roadmap_as_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    lines = text.strip().split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, txt=line)
    filename = f"raha_roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = os.path.join(os.getcwd(), filename)
    pdf.output(path)
    return path, filename

# Show current streak
if st.session_state.response_text:
    st.markdown("---")
    st.markdown(f"🔥 **Your Streak:** {st.session_state.streak} week(s) completed!")

# Show interactive roadmap
if st.session_state.response_text:
    weeks = extract_weeks(st.session_state.response_text)
    st.markdown("---")
    st.subheader("🚶 Chalna shuru kijiye:")

    full_content = ""

    for i, week_text in enumerate(weeks):
        week_num = i + 1
        header = week_text.splitlines()[0]
        content_lines = week_text.splitlines()[1:]

        full_content += f"\n\n## {week_text}"

        if week_num <= st.session_state.unlocked_weeks:
            with st.expander(f"✅ {header}"):
                tasks = [line.strip() for line in content_lines if line.strip()]
                for j, task in enumerate(tasks):
                    key = f"week{week_num}_task{j}"
                    if key not in st.session_state.task_checkboxes:
                        st.session_state.task_checkboxes[key] = False
                    st.session_state.task_checkboxes[key] = st.checkbox(task, value=st.session_state.task_checkboxes[key], key=key)

                st.markdown("**📝 Reflection Time**")
                reflection_key = f"reflection_week_{week_num}"
                if reflection_key not in st.session_state.reflection_submitted:
                    reflection = st.text_area("What did you learn this week?", key=f"reflection_input_{week_num}")
                    if st.button("Submit Reflection", key=f"submit_reflect_{week_num}"):
                        if reflection.strip():
                            st.session_state.reflection_submitted[reflection_key] = True
                            st.success("Reflection submitted!")
                            st.session_state.streak += 1
                            if week_num == st.session_state.unlocked_weeks and week_num < len(weeks):
                                st.session_state.unlocked_weeks += 1
                        else:
                            st.error("Please write something before submitting.")
                else:
                    st.success("✅ Reflection submitted for this week.")
        else:
            st.markdown(f"🔒 Week {week_num} is locked. Complete the previous week and submit your reflection to unlock.", unsafe_allow_html=True)

    # Save as PDF option
    st.markdown("---")
    if st.button("💾 Save as PDF"):
        pdf_path, filename = save_roadmap_as_pdf(full_content)
        with open(pdf_path, "rb") as file:
            st.download_button("📥 Download PDF", data=file, file_name=filename, mime="application/pdf")


