from fastapi import APIRouter, Request, Form, Depends, UploadFile, File
from app.data_base import sessionLocal
from sqlalchemy.orm import Session
from app.models import User, Book
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional


router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/hello')
def request_1(request:Request):
    return 'privet'

@router.post('/register', tags=['Auth'])
def registerUser(username:str = Form(...), email:str = Form(...), password:str = Form(...),
                 db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return 'пользователь уже существует'
    new_user = User(username = username, email = email, password = password)
    db.add(new_user)
    db.commit()
    return 'пользователь успешно создан'

@router.post('/login', tags=['Auth'])
def login_user( username:str = Form(...), password:str = Form(...),
                 db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        return 'неверные данные'
    return 'вы успешно вошли'

@router.get('/', tags=['Auth'], response_class=HTMLResponse)
def auth_page(request:Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/register_form', tags=['Auth'], response_class=HTMLResponse)
def register_form(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

@router.get('/login_form', tags=['Auth'], response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.post('/add_book', tags=['Book'])
def add_book( title:str = Form(...), author:str = Form(...), description:Optional[str] = Form(None),
              image_url:UploadFile = File(None),
                 db:Session = Depends(get_db)):
    book = db.query(Book).filter(Book.title == title).first()
    if book:
        return 'книга уже существует'
    new_book = Book(title=title, author=author, description=description, image_url=None)
    db.add(new_book)
    db.commit()