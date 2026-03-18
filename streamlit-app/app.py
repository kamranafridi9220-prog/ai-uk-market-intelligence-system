import os
import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

st.set_page_config(
    page_title="AI Market Intelligence",
    layout="wide",
)

st.title("🚀 AI Market Intelligence System")

st.markdown("""
AI-powered decision intelligence platform combining:
- Semantic search (embeddings)
- Business data modelling
- GPT-driven strategic reasoning
""")

st.write("Ask business questions and get structured, data-driven insights instantly.")

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(_file_), "ai_market_intelligence_engine_sample.xlsx")
    df = pd.read_excel(
        file_path,
        sheet_name="05_User_Query_Test"
    )
    df.columns = df.columns.str.strip()
    return df

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
def compute_embeddings(_questions):
    model = load_model()
    return model.encode(_questions)

def _generate_gpt_explanation_impl(client, user_question, matched_question, insight, action, confidence, impact):
    prompt = f"""
You are a senior strategy consultant (McKinsey/Bain style).

A user asked:
{user_question}

The system matched it to:
{matched_question}

Insight:
{insight}

Recommended action:
{action}

Confidence level:
{confidence}

Business impact:
{impact}

Now do the following:
1. Interpret what this means for the business in simple terms
2. Explain why this matters strategically
3. Suggest what the business should prioritise next

Keep it:
- Professional
- Clear
- Insightful
- 4–6 lines max

Avoid repeating the same sentences.
Write like a consultant summary.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output_text

def generate_gpt_explanation(client, user_question, matched_question, insight, action, confidence, impact):
    if client is None:
        return "GPT is unavailable because no valid OpenAI API key was found in Streamlit secrets."

    try:
        return _generate_gpt_explanation_impl(
            client,
            user_question,
            matched_question,
            insight,
            action,
            confidence,
            impact
        )
    except Exception:
        return "GPT is temporarily unavailable. Structured business insight is still shown above."

df = load_data()
model = load_model()
client = load_openai_client()

questions = df["User Question"].dropna().tolist()
question_embeddings = compute_embeddings(tuple(questions))

if "q_count" not in st.session_state:
    st.session_state.q_count = 0

if "example_query" not in st.session_state:
    st.session_state.example_query = ""

st.sidebar.header("Session Analytics")
st.sidebar.metric("Queries this session", st.session_state.q_count)

st.markdown("### 💡 Try example questions")

example_col1, example_col2, example_col3 = st.columns(3)

with example_col1:
    if st.button("Where should we focus expansion?"):
        st.session_state.example_query = "Where should we focus expansion?"

with example_col2:
    if st.button("Which regions have highest business activity?"):
        st.session_state.example_query = "Which regions have highest business activity?"

with example_col3:
    if st.button("Why is postcode analysis useful here?"):
        st.session_state.example_query = "Why is postcode analysis useful here?"

user_query = st.text_input(
    "🔍 Ask a business question",
    value=st.session_state.example_query,
    placeholder="e.g. Where should we focus expansion in the UK?"
)

if st.button("Generate Insight"):
    if not user_query.strip():
        st.warning("Please enter a business question first.")
    else:
        st.session_state.q_count += 1

        with st.spinner("Analyzing your question using AI..."):
            user_embedding = model.encode([user_query])
            scores = cosine_similarity(user_embedding, question_embeddings)[0]
            top_indices = np.argsort(scores)[::-1][:3]

        st.success("AI has interpreted your question and found the top matching business insights.")

        st.subheader("Top 3 Matched Questions")

        options = []
        selected_index = None

        for rank, idx in enumerate(top_indices, start=1):
            question = questions[idx]
            score = float(scores[idx])
            label = f"{rank}. {question} | score: {score:.3f}"
            options.append((label, idx))

        option_labels = [opt[0] for opt in options]
        selected_label = st.radio("Choose the most relevant match:", option_labels)

        for label, idx in options:
            if label == selected_label:
                selected_index = idx
                break

        if selected_index is not None:
            best_match = questions[selected_index]
            best_score = float(scores[selected_index])

            if best_score >= 0.40:
                result = df[df["User Question"] == best_match]

                if not result.empty:
                    selected_row = result.iloc[0]

                    insight = selected_row["Suggested Output"]
                    action = selected_row["Recommended Action"]
                    confidence = selected_row["Confidence Level"]
                    impact = selected_row["Business Impact"]

                    st.subheader("Best Matched Question")
                    st.write(best_match)

                    st.subheader("Similarity Score")
                    st.write(round(best_score, 3))
                    st.progress(min(max(best_score, 0.0), 1.0))

                    if best_score > 0.75:
                        st.success("High confidence match")
                    elif best_score > 0.60:
                        st.info("Moderate confidence match")
                    else:
                        st.warning("Low confidence match")

                    st.markdown("### 🤖 Why this insight?")
                    st.write(
                        f"This result was selected using semantic similarity between your query and stored business questions. "
                        f"Match score: {round(best_score, 3)}"
                    )

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
                            client=client,
                            user_question=user_query,
                            matched_question=best_match,
                            insight=insight,
                            action=action,
                            confidence=confidence,
                            impact=impact,
                        )

                    st.write(gpt_response)
                else:
                    st.error("Matched question found, but no result row was returned.")
            else:
                st.warning("No semantically relevant insight found. Try another question with more detail.")

st.markdown("---")
st.caption("Built by Kamran Khan | AI + Business Intelligence + Semantic Search")
