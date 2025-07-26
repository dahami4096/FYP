import openai
import os
from dotenv import load_dotenv


load_dotenv()
print("API Key Loaded:", os.getenv("OPENROUTER_API_KEY"))


client = openai.OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.getenv("OPENROUTER_API_KEY"),
)

def ask_ai(question):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can use "gpt-4" if your account has access
        messages=[
            {"role": "system", "content": "You are a friendly Python tutor who explains things in simple ways with examples."},
            {"role": "user", "content": question}
        ]
    )
    
    return response.choices[0].message.content