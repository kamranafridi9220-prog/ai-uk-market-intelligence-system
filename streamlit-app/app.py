import os
import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

st.set_page_config(page_title="AI Market Intelligence System", layout="wide")

st.title("AI Market Intelligence System")
st.info("AI-powered business decision engine using semantic search + GPT reasoning")
st.write("Ask business questions and get structured insights")

@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "ai_market_intelligence_engine_sample.xlsx")
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
    api_key = st.secrets["OPENAI_API_KEY"]
    if not api_key:
        return None
    return OpenAI(api_key=api_key)

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
        return "GPT unavailable because no OpenAI API key was found."

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

st.sidebar.header("Session Analytics")
st.sidebar.metric("Queries this session", st.session_state.q_count)

user_input = st.text_input("Enter your question:")

if user_input:
    st.session_state.q_count += 1

    user_embedding = model.encode([user_input])
    scores = cosine_similarity(user_embedding, question_embeddings)[0]

    top_indices = np.argsort(scores)[::-1][:3]

    st.success("AI has interpreted your question and found the top matching business insights.")

    st.subheader("Top 3 Matched Questions")

    selected_index = None
    options = []

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

        if best_score >= 0.55:
            result = df[df["User Question"] == best_match]

            if not result.empty:
                insight = result["Suggested Output"].values[0]
                action = result["Recommended Action"].values[0]
                confidence = result["Confidence Level"].values[0]
                impact = result["Business Impact"].values[0]

                st.subheader("Best Matched Question")
                st.write(best_match)

                st.subheader("Similarity Score")
                st.write(round(best_score, 3))
                st.progress(min(max(best_score, 0.0), 1.0))
                st.caption("Match reason: semantic similarity between your query and historical business questions.")

                if best_score > 0.75:
                    st.success("High confidence match")
                elif best_score > 0.60:
                    st.info("Moderate confidence match")
                else:
                    st.warning("Low confidence match")

                st.subheader("Insight")
                st.write(insight)

                st.subheader("Recommended Action")
                st.write(action)

                st.subheader("Confidence Level")
                st.write(confidence)

                st.subheader("Business Impact")
                st.write(impact)

                st.markdown("---")
                st.subheader("AI Strategic Summary")
                with st.spinner("Generating AI explanation..."):
                    explanation = generate_gpt_explanation(
                        client=client,
                        user_question=user_input,
                        matched_question=best_match,
                        insight=insight,
                        action=action,
                        confidence=confidence,
                        impact=impact,
                    )
                st.write(explanation)
            else:
                st.write("Matched question found, but no result row was returned.")
        else:
            st.write("No semantically relevant insight found. Try another question.")
