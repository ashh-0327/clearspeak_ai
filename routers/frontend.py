from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/domains")
def domains(request: Request):
    return templates.TemplateResponse("domains.html", {"request": request})

@router.get("/about")
def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})