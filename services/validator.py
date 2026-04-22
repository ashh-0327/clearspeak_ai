from groq import Groq
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

def evaluate_answer(question, options, correct_answer, user_answer, document_text):
    is_correct = user_answer.strip().upper() == correct_answer.strip().upper()
    return {
        'is_correct': is_correct,
        'correct_answer': correct_answer,
        'user_answer': user_answer
    }

def reexplain_topic(question, document_text, wrong_answer, correct_answer):
    prompt = '''
You are ClearSpeak AI. The user answered a comprehension question incorrectly.
Re-explain the specific topic from the document in even simpler terms.
Use a real life example to make it clearer.

Question they got wrong: ''' + question + '''
Their wrong answer: ''' + wrong_answer + '''
Correct answer: ''' + correct_answer + '''

Document context:
''' + document_text[:2000] + '''

Respond ONLY in this JSON format:
{
  "simple_explanation": "Explain the correct answer in 2-3 very simple sentences",
  "real_life_example": "Give a simple real life example to help them understand",
  "key_takeaway": "One sentence summary of what they should remember"
}

Respond ONLY with JSON.
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
            result = {'simple_explanation': 'Please re-read the document carefully.', 'real_life_example': '', 'key_takeaway': ''}
    return result

def validate_understanding(quiz, user_answers, document_text):
    results = []
    all_correct = True
    score = 0

    for i, question_data in enumerate(quiz):
        if i >= len(user_answers):
            break

        question = question_data['question']
        options = question_data['options']
        correct = question_data['correct']
        user_answer = user_answers[i]
        explanation = question_data.get('explanation', '')

        evaluation = evaluate_answer(question, options, correct, user_answer, document_text)
        is_correct = evaluation['is_correct']

        if is_correct:
            score += 1
            result = {
                'question_number': i + 1,
                'question': question,
                'user_answer': user_answer,
                'correct_answer': correct,
                'is_correct': True,
                'feedback': 'Correct! ' + explanation,
                'reexplanation': None
            }
        else:
            all_correct = False
            reexplanation = reexplain_topic(question, document_text, user_answer, correct)
            result = {
                'question_number': i + 1,
                'question': question,
                'user_answer': user_answer,
                'correct_answer': correct,
                'is_correct': False,
                'feedback': 'Incorrect. ' + explanation,
                'reexplanation': reexplanation
            }

        results.append(result)

    total = len(results)
    percentage = round((score / total) * 100) if total > 0 else 0

    if percentage == 100:
        understanding_level = 'Excellent'
        message = 'You fully understood this document. You can proceed with confidence.'
    elif percentage >= 66:
        understanding_level = 'Good'
        message = 'You understood most of this document. Review the incorrect answers above.'
    elif percentage >= 33:
        understanding_level = 'Partial'
        message = 'You partially understood this document. Please review the explanations carefully.'
    else:
        understanding_level = 'Low'
        message = 'You need to re-read this document. Go through the simplified explanations above.'

    return {
        'score': score,
        'total': total,
        'percentage': percentage,
        'understanding_level': understanding_level,
        'message': message,
        'all_correct': all_correct,
        'results': results
    }
