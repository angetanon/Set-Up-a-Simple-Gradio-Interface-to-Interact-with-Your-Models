import os
from pathlib import Path

import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).with_name(".env"))

if not os.environ.get("OPENAI_API_KEY", "").strip():
    raise RuntimeError("Set OPENAI_API_KEY in the .env file before starting the app.")

llm = ChatOpenAI(
    model="gpt-4o-mini",
    max_tokens=256,
    temperature=0.5,
)


def generate_response(prompt_txt: str) -> str:
    return llm.invoke(prompt_txt).text


chat_application = gr.Interface(
    fn=generate_response,
    flagging_mode="never",
    inputs=gr.Textbox(label="Input", lines=2, placeholder="Type your question here..."),
    outputs=gr.Textbox(label="Output"),
    title="OpenAI Chatbot",
    description="Ask any question and the chatbot will try to answer.",
)

if __name__ == "__main__":
    chat_application.launch(server_name="127.0.0.1", server_port=7860)
