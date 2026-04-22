import os
import json
import re
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def explain_legal_document(text: str, domain: str = 'legal') -> dict:
    from services.rag import retrieve_relevant_context
    context = retrieve_relevant_context(text[:500], domain=domain)
    prompt = f'''
You are ClearSpeak AI. Analyze this {domain} document and respond ONLY in this exact JSON format:

{{
  "summary": "Plain English summary in 3-4 sentences.",
  "key_terms": [
    {{
      "term": "legal term",
      "explanation": "plain English explanation"
    }}
  ],
  "risk_flags": [
    {{
      "risk": "risky clause",
      "why_it_matters": "why this affects the person signing"
    }}
  ],
  "action_items": ["simple instruction for the person"],
  "overall_risk_level": "Low or Medium or High",
  "one_line_verdict": "One sentence on whether this is safe to sign"
}}

{context}

Document:
''' + text[:3000] + '''

Respond ONLY with JSON. No extra text.
'''
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content': 'You only respond in valid JSON format.'},
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.3,
    )
    raw = response.choices[0].message.content.strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            result = {'error': 'Could not parse response', 'raw': raw}
    return result

def generate_quiz_questions(text: str) -> list:
    prompt = f'''
You are ClearSpeak AI. Generate exactly 3 multiple choice questions from this document.

Respond ONLY in this JSON format:
[
  {{
    "question": "the question",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
    "correct": "A",
    "explanation": "why this is correct"
  }}
]

Document:
''' + text[:2000] + '''

Respond ONLY with the JSON array.
'''
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[
            {'role': 'system', 'content': 'You only respond in valid JSON format.'},
            {'role': 'user', 'content': prompt}
        ],
        temperature=0.3,
    )
    raw = response.choices[0].message.content.strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\[.*\]', raw, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            result = []
    return result
