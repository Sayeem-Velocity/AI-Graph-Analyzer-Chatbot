# Groq Vision Chat

This project is a simple multimodal chat application built with **Streamlit** and **Groq API**.
It allows a user to upload a graph or chart image, type a query, and receive a grounded, human-like analysis of the graph.
The system prompt ensures every response begins with a concise **Title** of the graph and provides a clear descriptive summary.

---

## Features

* Upload a PNG or JPG image of a graph or chart.
* Ask any question about the uploaded figure.
* Get structured and human-like answers grounded in what is visible.
* Choose between two Groq LLM models:

  * `meta-llama/llama-4-scout-17b-16e-instruct`
  * `meta-llama/llama-4-maverick-17b-128e-instruct`
* ChatGPT-style interface with conversation history.

---

## Project Structure

```
.
├── agent.py         # Core Groq client and system prompt
├── appy.py          # Streamlit UI
├── requirements.txt # Python dependencies
├── .env             # Environment variables (API key)
└── README.md        # Documentation
```

---

## Requirements

* Python 3.10 or higher
* A Groq API key (sign up at [https://console.groq.com/](https://console.groq.com/))

---

## Installation

1. Clone the repository or copy the project files into a folder.

2. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/Mac
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your Groq API key:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

---

## Running the Application

Start the Streamlit app:

```bash
streamlit run appy.py
```

The application will launch in your default browser at:

```
http://localhost:8501
```

---

## Usage

1. Use the sidebar to select one of the two supported Groq models.
2. Upload a chart or graph image (PNG/JPG).
3. Type a question into the chat input box.
4. The assistant will provide a structured, human-like preview of the graph, beginning with a title and followed by descriptive insights.

---

## Notes

* The system prompt is tuned for graph and chart analysis. It does not generate code unless explicitly asked.
* If labels or scales are unclear in the image, the model will indicate uncertainty.
* Maximum output length is limited by the Groq model. Long responses may be truncated if they exceed the model’s completion cap.

---

## Support

For issues or collaboration, contact:
**[sayeem26s@gmail.com](mailto:sayeem26s@gmail.com)**
