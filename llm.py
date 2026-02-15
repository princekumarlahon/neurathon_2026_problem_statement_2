import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are an AI assistant for a small bakery.

Tasks:
1. Detect intent (menu, availability, order, unknown)
2. Extract item name if mentioned
3. Extract quantity if mentioned
4. Detect language (english, hindi, hinglish)

Return ONLY valid JSON like this:

{
  "intent": "...",
  "item": "...",
  "quantity": ...,
  "language": "english | hindi | hinglish"
}
"""
def analyze_message(message: str):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message}
        ],
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    # Remove markdown formatting if present
    if content.startswith("```"):
        content = content.split("```")[1]
        content = content.replace("json", "").strip()

    try:
        return json.loads(content)
    except:
        return {
            "intent": "unknown",
            "item": None,
            "quantity": None
        }
