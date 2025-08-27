from __future__ import annotations
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

from agent import ImageChatAgent, DEFAULT_MODEL, SCOUT, MAVERICK, SYSTEM_PROMPT

load_dotenv()

st.set_page_config(page_title="AI Graph Analyzer",  layout="centered")
st.title("AI Graph Analyzer")
#st.caption("Upload an image, type your question...")

# Sidebar: ONLY model select (as requested)
with st.sidebar:
    st.header("Settings")
    model = st.selectbox(
        "Groq model",
        [SCOUT, MAVERICK],
        index=0
    )

# Persist chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show history
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# Simple uploader above chat (Streamlit doesn't provide a '+' paperclip inside chat input)
uploaded = st.file_uploader("Upload an image (PNG/JPG)", type=["png", "jpg", "jpeg"])

# Chat input
prompt = st.chat_input("Ask something to llama-4…")

# Normal chat flow
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded:
            st.image(uploaded, caption="Uploaded image", use_container_width=True)

    # Use the fixed graph-analysis system prompt
    agent = ImageChatAgent(model=model, system_prompt=SYSTEM_PROMPT)

    # Stream response
    full = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        image_bytes: Optional[bytes] = uploaded.getvalue() if uploaded else None
        filename = uploaded.name if uploaded else None
        for token in agent.stream(prompt, image_bytes, filename):
            full += token or ""
            placeholder.markdown(full)

    st.session_state.messages.append({"role": "assistant", "content": full})
