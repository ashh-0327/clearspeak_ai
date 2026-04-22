from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from routers import explain
from routers import frontend

app = FastAPI(title='ClearSpeak AI', docs_url='/docs', redoc_url='/redoc')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Static files
app.mount('/static', StaticFiles(directory='static'), name='static')

# Templates
templates = Jinja2Templates(directory='templates')

# Routers
app.include_router(explain.router, prefix='/api')
app.include_router(frontend.router)   
