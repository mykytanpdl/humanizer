import streamlit as st
from groq import Groq

MODEL = "qwen/qwen3.8-27b"

SYSTEM_PROMPT = """You rewrite text so it sounds like it was written by a real person, not by an AI.

Rules:
- Keep the original meaning, facts, names and numbers. Do not add new information.
- Write in the same language as the input text.
- Remove typical AI phrases like "delve", "it's important to note", "in today's fast-paced world", "furthermore", "in conclusion", "seamless", "leverage".
- Mix short and long sentences. Use contractions where they fit the tone.
- Avoid em dashes, too many lists and too perfect structure.
- Tone: {tone}.
- Strength: {strength}.

Return only the rewritten text. No introduction, no explanation, no quotes around it."""

TONES = {
    "Casual": "relaxed and conversational, like a message to a friend",
    "Neutral": "natural and plain, like a normal blog post",
    "Professional": "polite and clear, like an email to a colleague, but not stiff",
}

STRENGTHS = {
    "Light": "change only what sounds robotic, keep most of the original wording",
    "Strong": "rewrite freely, change structure and wording as much as needed",
}


def clean(text):
    text = text.strip()
    first_line = text.split("\n")[0].lower()
    if first_line.endswith(":") and ("here" in first_line or "rewritten" in first_line):
        text = text.split("\n", 1)[1].strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    return text


def humanize(api_key, text, tone, strength):
    client = Groq(api_key=api_key)
    prompt = SYSTEM_PROMPT.format(tone=TONES[tone], strength=STRENGTHS[strength])
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        temperature=0.8,
        reasoning_format="hidden",
    )
    return clean(response.choices[0].message.content)


st.set_page_config(page_title="Humanizer", page_icon="✍️")
st.title("✍️ Humanizer")
st.write(
    "Does your text sound like it was written by a chatbot? Paste it below, and the app "
    "will rewrite it to sound more natural. The meaning stays the same.\n\n"
    "You need a Groq API key to use it. You can get one for free "
    "[here](https://console.groq.com/keys)."
)

api_key = st.sidebar.text_input("Groq API key", type="password")
tone = st.sidebar.selectbox("Tone", list(TONES.keys()), index=1)
strength = st.sidebar.radio("Strength", list(STRENGTHS.keys()))

text = st.text_area("Your text", height=250, placeholder="Paste your text here")

if st.button("Humanize", type="primary"):
    if not api_key:
        st.warning("Please enter your API key in the sidebar.")
    elif not text.strip():
        st.warning("Please enter some text first.")
    else:
        with st.spinner("Rewriting..."):
            result = humanize(api_key, text, tone, strength)
        st.subheader("Result")
        st.code(result, language=None, wrap_lines=True)
