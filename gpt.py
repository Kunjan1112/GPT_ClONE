import os
from openai import OpenAI
from dotenv import load_dotenv
from collections import deque

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

system_prompt = "You are a helpful assistant."
conversation_history = deque(maxlen=10)
MODEL = "llama3-70b-8192"

def get_response(user_message):
    if user_message.lower() == "clear":
        conversation_history.clear()
        return "Conversation cleared."

    conversation_history.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": system_prompt}] + list(conversation_history)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7
        )
        reply = response.choices[0].message.content.strip()
        conversation_history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        return f"⚠️ Error: {str(e)}"