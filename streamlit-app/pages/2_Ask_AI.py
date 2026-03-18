import os
import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

st.set_page_config(page_title="Ask AI", layout="wide")

st.title("🔍 Ask AI")

st.markdown("""
Ask a business question and get:

- semantic matches  
- structured insight  
- recommended action  
- confidence level  
- GPT strategic summary  
- downloadable AI report  
""")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader("📂 Upload your own Excel dataset", type=["xlsx"])

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        file_path = os.path.join(os.path.dirname(_file_), "..", "ai_market_intelligence_engine_sample.xlsx")
        df = pd.read_excel(file_path, sheet_name="05_User_Query_Test")

    df.columns = df.columns.str.strip()
    return df

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

# ---------------- LOAD OPENAI ----------------
@st.cache_resource
def load_openai_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except Exception:
        return None

# ---------------- EMBEDDINGS ----------------
@st.cache_resource
def compute_embeddings(questions):
    model = load_model()
    return model.encode(questions)

# ---------------- GPT FUNCTION ----------------
def generate_gpt_explanation(client, user_question, matched_question, insight, action, confidence, impact):
    if client is None:
        return "⚠️ GPT unavailable because no valid OpenAI API key was found."

    try:
        prompt = f"""
You are a senior business consultant.

User question:
{user_question}

Matched question:
{matched_question}

Insight:
{insight}

Recommended action:
{action}

Confidence:
{confidence}

Business impact:
{impact}

Explain:
1. What this means
2. Why it matters
3. What should be done next

Keep it short, clear, professional.
"""

        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"⚠️ GPT Error: {str(e)}"

# ---------------- LOAD EVERYTHING ----------------
df = load_data(uploaded_file)
model = load_model()
client = load_openai_client()

questions = df["User Question"].dropna().tolist()
question_embeddings = compute_embeddings(tuple(questions))

# ---------------- SESSION ANALYTICS ----------------
if "q_count" not in st.session_state:
    st.session_state.q_count = 0

st.sidebar.header("📊 Session Analytics")
st.sidebar.metric("Queries", st.session_state.q_count)

# ---------------- EXAMPLES ----------------
st.markdown("### 💡 Try example questions")

col1, col2, col3 = st.columns(3)

example_query = ""

with col1:
    if st.button("Where should we focus expansion?"):
        example_query = "Where should we focus expansion?"

with col2:
    if st.button("Which regions have highest activity?"):
        example_query = "Which regions have highest activity?"

with col3:
    if st.button("Why is postcode analysis useful?"):
        example_query = "Why is postcode analysis useful?"

# ---------------- INPUT ----------------
user_query = st.text_input(
    "🔍 Ask a business question",
    value=example_query,
    placeholder="e.g. Where should we expand in the UK?"
)

# ---------------- MAIN LOGIC ----------------
if st.button("Generate Insight"):

    if not user_query.strip():
        st.warning("Please enter a question.")
    else:
        st.session_state.q_count += 1

        with st.spinner("Analyzing with AI..."):
            user_embedding = model.encode([user_query])
            scores = cosine_similarity(user_embedding, question_embeddings)[0]
            top_indices = np.argsort(scores)[::-1][:3]

        st.success("Top matches found using semantic AI.")

        st.subheader("Top 3 Matches")

        options = []
        selected_index = None

        for rank, idx in enumerate(top_indices, start=1):
            q = questions[idx]
            score = float(scores[idx])
            label = f"{rank}. {q} | score: {score:.3f}"
            options.append((label, idx))

        selected_label = st.radio(
            "Choose the most relevant:",
            [opt[0] for opt in options]
        )

        for label, idx in options:
            if label == selected_label:
                selected_index = idx
                break

        # ---------------- RESULT ----------------
        if selected_index is not None:

            best_match = questions[selected_index]
            best_score = float(scores[selected_index])

            if best_score >= 0.40:
                row = df[df["User Question"] == best_match].iloc[0]

                insight = row["Suggested Output"]
                action = row["Recommended Action"]
                confidence = row["Confidence Level"]
                impact = row["Business Impact"]

                st.markdown("### 🤖 Why this insight?")
                st.write(f"Semantic similarity match score: {round(best_score, 3)}")

                st.progress(min(max(best_score, 0), 1))

                st.subheader("📊 Insight")
                st.success(insight)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### ✅ Recommended Action")
                    st.info(action)

                    st.markdown("### 📈 Business Impact")
                    st.write(impact)

                with col2:
                    st.markdown("### 🎯 Confidence Level")
                    st.write(confidence)

                st.markdown("---")

                st.subheader("🧠 AI Strategic Summary")

                with st.spinner("Generating AI explanation..."):
                    gpt_response = generate_gpt_explanation(
                        client,
                        user_query,
                        best_match,
                        insight,
                        action,
                        confidence,
                        impact
                    )

                st.write(gpt_response)

                # ---------------- DOWNLOAD REPORT ----------------
                report_text = f"""
AI MARKET INTELLIGENCE REPORT

User Question:
{user_query}

Matched Question:
{best_match}

Insight:
{insight}

Recommended Action:
{action}

Confidence Level:
{confidence}

Business Impact:
{impact}

AI Strategic Summary:
{gpt_response}
"""

                st.download_button(
                    label="📥 Download Report",
                    data=report_text,
                    file_name="ai_business_report.txt",
                    mime="text/plain"
                )

            else:
                st.warning("No strong match found. Try a clearer question.")
