import streamlit as st
from prompts import ai_roadmap_prompt
from groq import Groq
import os
import re
from fpdf import FPDF
from datetime import datetime

# Load galaxy theme
with open("galaxy_theme.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Use Streamlit Secrets for Groq API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Page config
st.set_page_config(page_title="raha.ai", layout='wide')
st.title(" raha.ai")
st.caption("You start. We guide.")

# Session state init
if "response_text" not in st.session_state:
    st.session_state.response_text = ""

if "unlocked_weeks" not in st.session_state:
    st.session_state.unlocked_weeks = 1

if "task_checkboxes" not in st.session_state:
    st.session_state.task_checkboxes = {}

# User input
user_input = st.text_input("🔍 Kis raha par chalna chahte hain? ")

# Generate roadmap
if st.button("Raha Dikhaiye"):
    if user_input.strip():
        with st.spinner("Roadmap tayaar ho raha hai..."):
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

# Helper to extract week-wise blocks
def extract_weeks(text):
    pattern = r"(Week \d+[\s\S]*?)(?=(Week \d+)|$)"
    matches = re.findall(pattern, text)
    return [match[0].strip() for match in matches]

# Helper to save PDF
def save_roadmap_as_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font("Arial", size=12)

    lines = content.split('\n')
    for line in lines:
        pdf.multi_cell(0, 10, txt=line)

    filename = f"raha_roadmap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    path = f"/tmp/{filename}"  # For Streamlit Cloud
    pdf.output(path)
    return path, filename

# Display roadmap
if st.session_state.response_text:
    weeks = extract_weeks(st.session_state.response_text)
    st.markdown("---")
    st.subheader("Chalna shuru kijiye:")

    full_content = ""
    for i, week_text in enumerate(weeks):
        week_num = i + 1
        header = week_text.splitlines()[0]
        content_lines = week_text.splitlines()[1:]

        if week_num <= st.session_state.unlocked_weeks:
            with st.expander(f"✅ {header}"):
                tasks = [line.strip() for line in content_lines if line.strip()]
                for j, task in enumerate(tasks):
                    key = f"week{week_num}_task{j}"
                    if key not in st.session_state.task_checkboxes:
                        st.session_state.task_checkboxes[key] = False
                    st.session_state.task_checkboxes[key] = st.checkbox(task, value=st.session_state.task_checkboxes[key], key=key)
                full_content += f"\n\n{header}\n" + "\n".join(tasks)

                if week_num == st.session_state.unlocked_weeks and week_num < len(weeks):
                    if st.button(f"🔓 Unlock Week {week_num + 1}", key=f"unlock_{week_num}"):
                        st.session_state.unlocked_weeks += 1
        else:
            st.markdown(f"🔒 **{header}** — Unlock previous weeks to access.", unsafe_allow_html=True)

    # Download as PDF
    st.markdown("---")
    if st.button("📄 Download Roadmap as PDF"):
        pdf_path, filename = save_roadmap_as_pdf(full_content)
        with open(pdf_path, "rb") as f:
            st.download_button(label="Download PDF", data=f, file_name=filename, mime="application/pdf")



