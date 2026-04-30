import streamlit as st
import requests 


def get_gemini_response(que):

    url = "http://localhost:8000/essay/invoke"
    payload = {
        "input": {
            "topic": que
        }
    }

    response = requests.post(url, json=payload)
    data = response.json()
    return data['output']['content']
    

def get_hf_response(que):
    url = "http://localhost:8000/poem/invoke"
    payload = {
        "input": {
            "topic": que
        }
    }

    response = requests.post(url, json=payload)
    data = response.json()
    return data['output'] 


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(
    page_title="LangChain AI Lab",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 LangChain AI Lab")
st.subheader("Essay + Bullet Generator (Gemini + HuggingFace)")

st.write("---")

topic = st.text_input("Enter your topic", placeholder="e.g. Artificial Intelligence")
col1, col2 = st.columns(2)

with col1:
    essay_btn = st.button("✍️ Generate Essay (Gemini)")

with col2:
    bullet_btn = st.button("🔹 Generate Poem (HF)")

# output
if essay_btn and topic:
    with st.spinner("Generating essay..."):
        result = get_gemini_response(topic)
    st.markdown("## 📝 Essay Output")
    st.write(result)


if bullet_btn and topic:
    with st.spinner("Generating Poem..."):
        result = get_hf_response(topic)

    st.markdown("## 🔹 Poem")
    st.write(result)


# Footer
st.write("---")
st.caption("Built with Streamlit + LangChain + FastAPI 🚀")
