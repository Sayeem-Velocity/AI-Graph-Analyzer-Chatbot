import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import base64
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage

# Load .env
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini LLM via LangChain
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    temperature=0,
    max_output_tokens=2048,
    google_api_key=GOOGLE_API_KEY
)

# System instruction for OCR receipts
system_prompt = """
You are a strict OCR analyst specialized in receipts.

- Extract ALL text from the uploaded receipt image.
- Organize it into a structured plain-text receipt format.
- Follow this general structure, but include extra sections if they exist in the receipt:

===============================
          {STORE NAME}
{STORE ADDRESS or LOCATION}
{PHONE (if present)}
===============================

{ORDER INFO: Order #, Table, Party size, Server, Time, Date}

-------------------------------
Items:
{QTY}  {ITEM NAME}              {PRICE}
{QTY}  {ITEM NAME}              {PRICE}
...
-------------------------------

{ANY SUBTOTALS (if present)}

Subtotal:                       {SUBTOTAL}
Tax:                            {TAX}
TOTAL:                          {TOTAL}
-------------------------------

{EXTRA SECTIONS: e.g., Gratuity, Discounts, Payment method}

{DATE & TIME again if present}

{FOOTER MESSAGES like "Thank you", "Visit again", etc.}
===============================

Rules:
- Keep spacing aligned so amounts are right-justified.
- Do not remove or skip fields that exist on the receipt (like gratuity suggestions).
- If a section is missing in the receipt, simply omit it (don’t insert nulls).
- Do not use Markdown, JSON, or explanations — only the plain structured receipt text.
- TOTAL must always be uppercase.
- If no receipt detected, reply: No receipt detected
"""


# Streamlit UI
st.set_page_config(page_title="Receipt OCR Chatbot", layout="centered")
st.title("Receipt OCR Chatbot (LangChain + Gemini)")

# Chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

uploaded_file = st.file_uploader("Upload a receipt image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Receipt", use_container_width=True)

    # Convert uploaded image to base64 string
    img_bytes = uploaded_file.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode("utf-8")

    # Build LangChain messages
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=[
            {"type": "text", "text": "Extract the receipt text and return JSON strictly."},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}}
        ])
    ]

    # Run OCR
    with st.spinner("Extracting text from receipt..."):
        response = llm.invoke(messages)

    extracted_text = response.content

    # Save to chat history
    st.session_state.chat_history.append(("You", "Uploaded a receipt"))
    st.session_state.chat_history.append(("Gemini", extracted_text))

# Display chat
st.subheader("Chat")
for role, msg in st.session_state.chat_history:
    st.markdown(f"**{role}:** {msg}")

# Export option
if st.session_state.chat_history:
    last_bot_response = st.session_state.chat_history[-1][1]
    st.download_button(
        "Export OCR Result as TXT",
        data=last_bot_response,
        file_name="receipt_output.txt",
        mime="text/plain"
    )
