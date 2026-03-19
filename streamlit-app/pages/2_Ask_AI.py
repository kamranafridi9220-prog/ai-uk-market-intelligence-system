import os
import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

st.set_page_config(page_title="Ask AI", layout="wide")

st.title("🔍 Ask AI")
st.markdown("---")
st.info("💡 Ask any business question and get AI-powered insights instantly.")

st.markdown("""
Ask a business question and get:

- semantic matches
- structured insight
- recommended action
- confidence level
- GPT strategic summary
- downloadable AI report
- decision score
- follow-up questions
""")

uploaded_file = st.file_uploader("📂 Upload your own Excel dataset", type=["xlsx"])


# -----------------------------
# Helpers
# -----------------------------
def clean_columns(df):
    df.columns = df.columns.astype(str).str.strip()
    return df


def detect_columns(df):
    cols = {c.lower().strip(): c for c in df.columns}

    question_col = None
    for candidate in ["user question", "question", "questions"]:
        if candidate in cols:
            question_col = cols[candidate]
            break

    insight_col = None
    for candidate in ["suggested output", "insight", "answer", "example answer"]:
        if candidate in cols:
            insight_col = cols[candidate]
            break

    action_col = None
    for candidate in ["recommended action", "recommendation", "action"]:
        if candidate in cols:
            action_col = cols[candidate]
            break

    confidence_col = None
    for candidate in ["confidence level", "confidence"]:
        if candidate in cols:
            confidence_col = cols[candidate]
            break

    impact_col = None
    for candidate in ["business impact", "impact"]:
        if candidate in cols:
            impact_col = cols[candidate]
            break

    category_col = None
    for candidate in ["matched category", "category", "question type"]:
        if candidate in cols:
            category_col = cols[candidate]
            break

    chart_col = None
    for candidate in ["supporting chart", "data source", "chart reference"]:
        if candidate in cols:
            chart_col = cols[candidate]
            break

    return {
        "question": question_col,
        "insight": insight_col,
        "action": action_col,
        "confidence": confidence_col,
        "impact": impact_col,
        "category": category_col,
        "chart": chart_col,
    }


def calculate_decision_score(user_question, impact_value="", confidence_value=""):
    q = str(user_question).lower().strip()

    score = 7.0
    risk = "Medium"
    ai_confidence = "Medium"

    if any(word in q for word in ["expand", "growth", "target", "opportunity", "region"]):
        score = 8.6
        risk = "Medium"
        ai_confidence = "High"
    elif any(word in q for word in ["risk", "competition", "low activity"]):
        score = 6.4
        risk = "High"
        ai_confidence = "Medium"
    elif any(word in q for word in ["market", "company", "structure", "distribution"]):
        score = 7.8
        risk = "Low"
        ai_confidence = "High"

    impact_value = str(impact_value).lower()
    confidence_value = str(confidence_value).lower()

    if "high" in impact_value:
        score = min(score + 0.4, 10.0)
    elif "low" in impact_value:
        score = max(score - 0.3, 0.0)

    if "high" in confidence_value:
        ai_confidence = "High"
    elif "low" in confidence_value:
        ai_confidence = "Low"

    return round(score, 1), risk, ai_confidence


def get_follow_up_questions(questions, current_question, top_n=3):
    current_question = str(current_question).strip().lower()
    filtered = [q for q in questions if str(q).strip().lower() != current_question]
    return filtered[:top_n]


# -----------------------------
# Data loading
# -----------------------------
@st.cache_data
def load_data(uploaded_file):
    try:
        # Preferred order of sheets to load
        preferred_sheets = [
            "05_User_Query_Test",
            "03_Insights_Output",
            "01_insights_engine",
            "02_ai_response_templates",
            "04_Decision_Rules",
        ]

        if uploaded_file is not None:
            excel_file = pd.ExcelFile(uploaded_file)
            available_sheets = excel_file.sheet_names

            selected_sheet = None
            for sheet in preferred_sheets:
                if sheet in available_sheets:
                    selected_sheet = sheet
                    break

            if selected_sheet is None:
                selected_sheet = available_sheets[0]

            df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
            df = clean_columns(df)
            return df, selected_sheet, available_sheets

        else:
            file_path = os.path.join(
                os.path.dirname(_file_),
                "..",
                "ai_market_intelligence_engine_sample.xlsx"
            )

            excel_file = pd.ExcelFile(file_path)
            available_sheets = excel_file.sheet_names

            selected_sheet = None
            for sheet in preferred_sheets:
                if sheet in available_sheets:
                    selected_sheet = sheet
                    break

            if selected_sheet is None:
                selected_sheet = available_sheets[0]

            df = pd.read_excel(file_path, sheet_name=selected_sheet)
            df = clean_columns(df)
            return df, selected_sheet, available_sheets

    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return pd.DataFrame(), None, []


@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def load_openai_client():
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        if not api_key:
            return None
        return OpenAI(api_key=api_key)
    except Exception:
        return None


@st.cache_resource
def compute_embeddings(questions):
    model = load_model()
    return model.encode(list(questions))


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


# -----------------------------
# Load app resources
# -----------------------------
df, loaded_sheet_name, available_sheets = load_data(uploaded_file)

if df.empty:
    st.warning("No valid data loaded. Please upload a working Excel file.")
    st.stop()

detected = detect_columns(df)

question_col = detected["question"]
insight_col = detected["insight"]
action_col = detected["action"]
confidence_col = detected["confidence"]
impact_col = detected["impact"]
category_col = detected["category"]
chart_col = detected["chart"]

if question_col is None:
    st.error("No valid question column found.")
    st.write("Loaded sheet:", loaded_sheet_name)
    st.write("Available sheets:", available_sheets)
    st.write("Columns found:", list(df.columns))
    st.stop()

df = df.dropna(subset=[question_col]).copy()
df[question_col] = df[question_col].astype(str).str.strip()

questions = df[question_col].dropna().astype(str).tolist()

if len(questions) == 0:
    st.error("No questions found in the dataset.")
    st.stop()

model = load_model()
client = load_openai_client()
question_embeddings = compute_embeddings(tuple(questions))

if "q_count" not in st.session_state:
    st.session_state.q_count = 0

if "history" not in st.session_state:
    st.session_state.history = []


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("📊 Session Analytics")
st.sidebar.metric("Queries", st.session_state.q_count)

st.sidebar.markdown("### 🧾 Query History")
for i, q in enumerate(st.session_state.history[-5:], 1):
    st.sidebar.write(f"{i}. {q}")

st.sidebar.markdown("### 📁 Loaded Sheet")
st.sidebar.write(loaded_sheet_name)

st.sidebar.markdown("### 🧩 Detected Columns")
st.sidebar.write(detected)


# -----------------------------
# Example questions
# -----------------------------
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

user_query = st.text_input(
    "🔍 Ask a business question",
    value=example_query,
    placeholder="e.g. Where should we expand in the UK?"
)


# -----------------------------
# Main search
# -----------------------------
if st.button("Generate Insight"):
    if not user_query.strip():
        st.warning("Please enter a question.")
    else:
        st.session_state.q_count += 1
        st.session_state.history.append(user_query)

        with st.spinner("Analyzing with AI..."):
            user_embedding = model.encode([user_query])
            scores = cosine_similarity(user_embedding, question_embeddings)[0]
            top_indices = np.argsort(scores)[::-1][:3]

        st.markdown("---")
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

        if selected_index is not None:
            best_match = questions[selected_index]
            best_score = float(scores[selected_index])

            if best_score >= 0.40:
                row = df[df[question_col] == best_match].iloc[0]

                insight = row[insight_col] if insight_col and pd.notna(row.get(insight_col, None)) else "No insight available."
                action = row[action_col] if action_col and pd.notna(row.get(action_col, None)) else "No action available."
                confidence = row[confidence_col] if confidence_col and pd.notna(row.get(confidence_col, None)) else "N/A"
                impact = row[impact_col] if impact_col and pd.notna(row.get(impact_col, None)) else "N/A"
                category = row[category_col] if category_col and pd.notna(row.get(category_col, None)) else "N/A"
                chart = row[chart_col] if chart_col and pd.notna(row.get(chart_col, None)) else "N/A"

                decision_score, risk_level, calc_confidence = calculate_decision_score(
                    user_query, impact, confidence
                )

                st.markdown("### 🤖 Why this insight?")
                st.write(f"This result was selected using semantic similarity. Match score: {round(best_score, 3)}")

                st.progress(min(max(best_score, 0), 1))

                if best_score > 0.75:
                    st.success("High confidence match")
                elif best_score > 0.60:
                    st.info("Moderate confidence match")
                else:
                    st.warning("Low confidence match")

                st.subheader("📊 Insight")
                st.success(f"💡 {insight}")

                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("### ✅ Recommended Action")
                    st.info(action)

                    st.markdown("### 📈 Business Impact")
                    st.write(impact)

                    st.markdown("### 🗂 Category")
                    st.write(category)

                with col_b:
                    st.markdown("### 🎯 Confidence Level")
                    st.write(confidence)

                    st.markdown("### 📌 Supporting Source")
                    st.write(chart)

                    st.markdown("### ⚖️ Risk Level")
                    st.write(risk_level)

                st.markdown("---")
                st.subheader("📍 Decision Score")

                s1, s2, s3 = st.columns(3)
                s1.metric("Opportunity Score", f"{decision_score}/10")
                s2.metric("Risk Level", risk_level)
                s3.metric("AI Confidence", calc_confidence)

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

                st.markdown("---")
                st.subheader("➡️ Suggested Follow-up Questions")
                follow_ups = get_follow_up_questions(questions, best_match, top_n=3)
                for fq in follow_ups:
                    st.write(f"- {fq}")

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

Category:
{category}

Supporting Source:
{chart}

Decision Score:
{decision_score}/10

Risk Level:
{risk_level}

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

st.markdown("---")
with st.expander("Preview loaded dataset"):
    st.write("Loaded sheet:", loaded_sheet_name)
    st.write("Available sheets:", available_sheets)
    st.write("Columns:", list(df.columns))
    st.dataframe(df.head(20), use_container_width=True)

st.caption("AI Product Prototype | Built by Kamran Khan")
