# ✍️ Humanizer

A small web app that rewrites AI-sounding text so it reads like a real person wrote it. The meaning, facts and language of the original text stay the same.

You can choose the tone (Casual, Neutral, Professional) and how much to change (Light or Strong). The app makes one call to an LLM (`qwen/qwen3.8-27b` on [Groq](https://groq.com)) and shows only the rewritten text.

**Live app:** https://simple-humanizer.streamlit.app/

## Run locally

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/streamlit run app.py
```

You need a Groq API key. You can get one for free at [console.groq.com/keys](https://console.groq.com/keys). Enter it in the sidebar; the key is not stored anywhere.
