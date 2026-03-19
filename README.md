# 🚀 AI Market Intelligence Engine

An AI-powered decision intelligence platform that transforms natural language business questions into structured insights, strategic recommendations, and downloadable reports.

---

## 🌐 Live Demo

👉 https://ai-uk-market-intelligence-system-icoqpn7m2bjci3a4berqvq.streamlit.app

---

## 🧠 Project Vision

Most data projects stop at dashboards.

This project explores what happens when we go one step further — from *visualisation → decision intelligence*.

The goal was simple:

> Can we build a system where users ask business questions and get structured, actionable decisions instantly?

---

## ⚙️ What This System Does

Users can:

- Ask business questions in natural language  
- Retrieve semantically matched insights  
- Get AI-generated strategic recommendations  
- Understand confidence levels and business impact  
- Download decision-ready reports  
- Upload custom datasets  

---

## 🧩 Core Features

### 🔍 Semantic Search (NLP)
- Uses sentence-transformers (MiniLM model)
- Converts questions into embeddings
- Matches based on meaning (not keywords)

---

### 🤖 GPT-Powered Strategic Reasoning
- Uses OpenAI (gpt-4o-mini)
- Generates:
  - Explanation of insight
  - Business interpretation
  - Recommended next steps

---

### 📊 Structured Insights
Each result includes:
- Insight  
- Recommended Action  
- Confidence Level  
- Business Impact  

---

### 📥 Downloadable Reports
- Generates AI-powered reports
- Exportable directly from the app
- Business-ready outputs

---

### 📂 Custom Dataset Upload
- Upload Excel datasets
- System adapts dynamically

---

### 🧾 Query History
- Tracks last 5 user queries
- Enhances usability (SaaS feel)

---

### 🧭 Multi-Page SaaS Structure
- Home (Overview)
- Ask AI (Core Engine)
- Upload Data
- About

---

## 🏗️ System Architecture

User Question  
↓  
Sentence Transformer (Embeddings)  
↓  
Cosine Similarity Matching  
↓  
Best Match  
↓  
Structured Insight (Action + Impact + Confidence)  
↓  
GPT Strategic Explanation  
↓  
Downloadable Report  

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- Sentence Transformers  
- Scikit-learn  
- Pandas  
- OpenAI API  

---

## 📁 Project Structure

streamlit-app/  
│  
├── app.py  
├── requirements.txt  
├── ai_market_intelligence_engine_sample.xlsx  
│  
└── pages/  
  ├── 2_Ask_AI.py  
  ├── Upload_Data.py  
  └── About.py  

---

## 🔐 Environment Setup

Add your API key in Streamlit Secrets:
'''tom1
OPEN_AI_KEY = "your-api-key-here"
run locally
pip install -r requirements.txt
stramlit run app.py

---

## 🚀 Deployment

This project is deployed on Streamlit Community Cloud.

Deployment steps followed:
	1.	Created GitHub repository
	2.	Uploaded project files
	3.	Connected repository to Streamlit Community Cloud
	4.	Set main file path to:
streamlit-app/app.py
	5.	Added OpenAI API key to Streamlit Secrets
	6.	Fixed dependency and file path issues
	7.	Rebooted and tested the live app

---

# ⚠️ Challenges Faced and Solutions

This project involved multiple real-world problems during development and deployment. Solving them was an important part of the build process.

## 1. GitHub Structure Issues

At the start, the repository structure became confusing because files and folders were not in the correct place. The initial folder setup created unnecessary nesting and some files were uploaded into the wrong location.

Solution:
The repository was cleaned up and rebuilt properly. The final structure was standardised so that the Streamlit app files sat inside the correct streamlit-app folder and the page files were placed inside the pages folder.

⸻

## 2. Difficulty Deleting Folders in GitHub

Deleting folders directly from GitHub was not straightforward, especially when trying to remove incorrectly created folders.

Solution:
The original repository was deleted and recreated cleanly, which made the structure easier to control and removed earlier folder mistakes.

⸻

## 3. Running Streamlit Locally

There were several command prompt issues at the start, including:
	•	wrong folder location
	•	missing streamlit package
	•	app file not found
	•	Python path confusion

Solution:
The correct folder path was used, packages were installed properly, and the app was run from the correct directory with the correct command.

⸻

## 4. File Not Found Errors for Excel

The app initially could not locate the Excel file in deployed mode.

Cause:
Relative file paths worked locally but failed on Streamlit Cloud.

Solution:
The path was updated using:
os.path.join(os.path.dirname(_file_), "..", "ai_market_intelligence_engine_sample.xlsx") and the Excel file was uploaded to the correct folder in the repository.

⸻

## 5. Missing Excel Dependency

The deployed app failed because .xlsx files require openpyxl.

Error encountered:
Missing optional dependency openpyxl

Solution:
openpyxl was added to requirements.txt.

⸻

## 6. GPT Not Working Initially

The AI summary section originally showed fallback messages instead of GPT output.

Cause:
The OpenAI API key was either not loaded correctly or not set in the proper Streamlit format.

Solution:
The API key was added through Streamlit Secrets and accessed correctly using: st.secrets["OPENAI_API_KEY"] 

⸻

## 7. TOML Formatting Errors in Streamlit Secrets

There were errors caused by pasting the raw API key directly into the secrets box.

Solution:
The secrets were formatted correctly using:OPENAI_API_KEY = "your-api-key-here"

⸻

## 8. Secrets Object Error

An error occurred because st.secrets was mistakenly used like a function instead of like a dictionary.
Wrong: st.secrets("OPENAI_API_KEY")
Correct: st.secrets["OPENAI_API_KEY"]

⸻

## 9. NameError with _file_

A bug was created by typing file instead of _file_.

Solution:
The correct Python variable (__file__) was used.

⸻

## 10. GPT Client and Quota Problems

The OpenAI client initially failed because billing/quota issues and key setup prevented the GPT summary from being returned.

Solution:
Billing was enabled, the key was regenerated, and GPT logic was wrapped in safe fallback handling so the app could still return structured outputs even when GPT failed.

⸻

## 11. Semantic Matching Quality

Some user inputs were too short, such as “post code”, which led to low similarity scores.

Solution:
Several improvements were made:
	•	lowered the threshold
	•	added top 3 matched questions
	•	improved the dataset structure
	•	encouraged clearer user phrasing
	•	added example business questions

⸻

## 12. Download Button Not Showing

The download report button was not visible at first.

Cause:
The code block was not placed correctly inside the successful result section.

Solution:
The report generation and st.download_button() logic were inserted directly below the AI summary output.

⸻

## 13. Multi-Page App Confusion

When adding multi-page support, page files were first created in the wrong nested folder.

Solution:
The pages were moved into the correct structure: After that, streamlt automatically generated the slidebar navigation correctly.

⸻

## 14. Streamlit “Unable to Deploy” Popup

A popup appeared saying the app was not connected to a remote GitHub repository.

Cause:
This happened after clicking the internal Deploy button again even though the app was already deployed.

Solution:
The popup was ignored, the current deployment was kept, and the app was managed through Manage app → Reboot instead of redeploying from inside the running app.

⸻

## 💡 Key Learnings

This project provided several important lessons:
	•	Semantic search enables more human-like query handling
	•	Data becomes far more useful when linked to decisions
	•	GPT works best when layered on top of structured outputs
	•	Deployment issues are part of real product building
	•	Clean folder structure matters
	•	UI/UX matters just as much as model accuracy
	•	Real-world development is iterative, not linear

⸻

## 🚀 Product Positioning

This is not just a dashboard project.

It is a:
	•	Decision Intelligence System
	•	AI-powered Business Tool
	•	Multi-page SaaS Prototype
	•	Applied NLP + LLM product

⸻

## 💼 Use Cases

This system can be adapted for:
	•	Market expansion strategy
	•	Customer behaviour analysis
	•	Sales decision support
	•	Geographic intelligence
	•	Business prioritisation
	•	Opportunity and risk identification

⸻

## 📈 Future Improvements

Planned future upgrades include:
	•	User authentication
	•	Database integration
	•	Persistent query history
	•	More advanced GPT summaries
	•	Better dataset upload validation
	•	API-based backend
	•	Monetisation / SaaS business model
	•	Custom domain deployment
	•	Analytics dashboard for usage tracking

⸻

## ⭐ Final Thought

From dashboards to decisions.

This project represents a shift from analysing data to actually using it to support decision-making in a more intelligent, product-oriented way.

⸻

## 👤 Author

Kamran Khan
	•	MSc Business Intelligence & Digital Marketing
	•	Corporate Account Executive (UK)
	•	Building AI-driven business solutions with analytics, NLP, and applied AI
