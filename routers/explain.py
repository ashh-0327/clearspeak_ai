from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from services.parser import parse_uploaded_file
from services.llm import explain_legal_document, generate_quiz_questions
from services.classifier import detect_domain
from services.validator import validate_understanding


router = APIRouter()


def about():
    return open("templates/about.html").read()
class QuizAnswer(BaseModel):
    question: str
    options: List[str]
    correct: str
    explanation: str

class ValidateRequest(BaseModel):
    document_text: str
    quiz: List[QuizAnswer]
    user_answers: List[str]

@router.get('/ping')
def ping():
    return {'message': 'explain router is alive'}

@router.post('/upload')
async def upload_document(file: UploadFile = File(...)):
    allowed_types = ['.pdf', '.jpg', '.jpeg', '.png', '.txt']
    filename = file.filename
    ext = filename[filename.rfind('.'):].lower()
    if ext not in allowed_types:
        raise HTTPException(status_code=400, detail='File type not supported.')
    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail='Uploaded file is empty.')
    try:
        extracted_text = parse_uploaded_file(file_bytes, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail='Text extraction failed: ' + str(e))
    return {
        'filename': filename,
        'characters_extracted': len(extracted_text),
        'preview': extracted_text[:500],
        'full_text': extracted_text
    }

@router.post('/explain')
async def explain_document(file: UploadFile = File(...)):
    allowed_types = ['.pdf', '.jpg', '.jpeg', '.png', '.txt']
    filename = file.filename
    ext = filename[filename.rfind('.'):].lower()
    if ext not in allowed_types:
        raise HTTPException(status_code=400, detail='File type not supported.')
    file_bytes = await file.read()
    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail='Uploaded file is empty.')
    try:
        extracted_text = parse_uploaded_file(file_bytes, filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail='Text extraction failed: ' + str(e))
    if len(extracted_text) < 50:
        raise HTTPException(status_code=400, detail='Not enough text extracted.')
    domain_result = detect_domain(extracted_text)
    detected_domain = domain_result['domain']
    try:
        explanation = explain_legal_document(extracted_text, domain=detected_domain)
    except Exception as e:
        raise HTTPException(status_code=500, detail='LLM explanation failed: ' + str(e))
    try:
        quiz = generate_quiz_questions(extracted_text)
    except Exception as e:
        quiz = []
    return {
        'filename': filename,
        'characters_extracted': len(extracted_text),
        'domain_detection': domain_result,
        'explanation': explanation,
        'quiz': quiz
    }

@router.post('/validate')
async def validate_answers(request: ValidateRequest):
    if not request.document_text:
        raise HTTPException(status_code=400, detail='Document text is required.')
    if not request.quiz:
        raise HTTPException(status_code=400, detail='Quiz is required.')
    if not request.user_answers:
        raise HTTPException(status_code=400, detail='User answers are required.')
    if len(request.user_answers) != len(request.quiz):
        raise HTTPException(status_code=400, detail='Number of answers must match number of questions.')
    quiz_list = [q.dict() for q in request.quiz]
    try:
        validation_result = validate_understanding(
            quiz_list,
            request.user_answers,
            request.document_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail='Validation failed: ' + str(e))
    return validation_result
