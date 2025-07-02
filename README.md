# raha.ai — Personalized AI-Powered Learning Roadmaps

**raha.ai** is a web application that generates structured, week-wise learning roadmaps for any topic using AI. It simplifies your learning journey by breaking it down into weekly milestones and tasks, encouraging consistent progress through an interactive, streak-based interface. Users can view, interact, and download their personalized roadmap.

---

## 🛠️ Technology Stack Used

- **Frontend**: Streamlit
- **AI Backend**: Groq API (LLaMA 3 model)
- **PDF Export**: FPDF
- **Styling**: Custom CSS for minimal UI
- **Version Control**: Git & GitHub
- **Hosting**: Streamlit Cloud

---

## 🚀 Features Implemented

- Personalized, AI-generated, week-wise learning roadmaps
- Click-to-unlock week-wise navigation
- Task checklist system for tracking completion
- Streak system to reward consistent learning
- One-click PDF export of entire roadmap
- Clean and minimal user interface

---

## ⚙️ Setup and Installation Instructions
🛠️ Setup and Installation Instructions
To run raha.ai locally on your system:

Clone the repository

git clone https://github.com/navyarangwani/ai-roadmap-generator.git
cd ai-roadmap-generator
Create a virtual environment

For Windows:

python -m venv venv
venv\Scripts\activate
For macOS/Linux:

python3 -m venv venv
source venv/bin/activate
Install dependencies


pip install -r requirements.txt
Add your Groq API key

Create a folder called .streamlit

Inside it, create a file named secrets.toml

Paste the following:

[general]
GROQ_API_KEY = "your_groq_api_key_here"
Run the app

streamlit run roadmap.py
App will open in your browser at http://localhost:8501
---
## Deployed Link
https://raha-ai-roadmap-generator.streamlit.app/
---
## 📊 App Flow / System Architecture

![App Flow](https://drive.google.com/uc?export=view&id=1kWufR8AnpmMYHilIyK2c4-O_T11EaKBG)
---
## Screenshots

![Home Page](https://drive.google.com/uc?export=view&id=1QSZ5ExK2OUwZYTc1PLkPlAvB9HDfz_DS)

![Week 1](https://drive.google.com/uc?export=view&id=1Bkfjn5ANHMleYOttEsOIy9Bs2BAHSt4S)

![Weeks View](https://drive.google.com/uc?export=view&id=1-7qt3ILXkrWAKsP_FriuDqfNg0anbCrx)


---

## 👥 Team Members and Contributions

### Team Name: procastiNOTers

- **Navya Rangwani**
  - Co-developed the full-stack web application using Streamlit.
  - Integrated the Groq API and designed the roadmap generation logic.
  - Worked on UI structuring, weekly unlock flow, and checklist functionality.
  - Co-created the walkthrough video and contributed to overall UX direction.

- **Mahek Hingorani**
  - Co-developed the roadmap logic and prompt engineering for Groq's LLM.
  - Designed the Figma UI prototype and created visual flow diagrams.
  - Worked on feature refinement, error handling, and feedback improvements.
  - Co-created the walkthrough video and led documentation and deployment.
  - ---
## 🌱 Future Scope / Improvements

- Add login/signup with user authentication and save progress across sessions.
- Improve mobile responsiveness and make UI more adaptive.
- Link trusted learning resources (videos, blogs, courses) to each roadmap step.
- Introduce gamified features like badges, streak analytics, and achievements.
- Allow users to share or collaborate on roadmaps with others.
- Support roadmap generation in multiple languages.






