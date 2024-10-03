import os

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=os.getenv("HF_API_KEY"))

messages = [{"role": "system", "content": "You are an intelligent assistant."}]

def request_chatgpt_reply(user_request: str):
    messages.append({"role": "user", "content": user_request})

    response = client.chat_completion(
        messages,
        max_tokens=100
    )

    reply = response.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})

    return reply
