from fastapi import APIRouter, Request, Form, Depends, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import logging
from app.data_base import sessionLocal
from sqlalchemy.orm import Session
from app.models import User, Book, Review
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import Optional
from uuid import uuid4
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory='app/templates')


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/hello')
def request_1(request: Request):
    return 'privet'


@router.post('/register', tags=['Auth'])
def registerUser(
        username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if user:
        return 'пользователь уже существует'

    new_user = User(username=username, email=email, password=password)
    db.add(new_user)
    db.commit()

    return 'пользователь успешно создан'


@router.post('/login', tags=['Auth'])
def login_user(
        username: str = Form(...),
               password: str = Form(...),
               db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()

    if not user or user.password != password:
        return 'неверные данные'

    response = JSONResponse(content={'message': 'Вы успешно вошли'})
    response.set_cookie(key='user_id', value=str(user.id))

    return response


@router.get('/', tags=['Auth'], response_class=HTMLResponse)
def auth_page(
        request: Request
):
    return templates.TemplateResponse('index.html', {'request': request})


@router.get('/register_form', tags=['Auth'], response_class=HTMLResponse)
def register_form(
        request: Request
):
    return templates.TemplateResponse('register.html', {'request': request})


@router.get('/login_form', tags=['Auth'], response_class=HTMLResponse)
def login_form(
        request: Request

):
    return templates.TemplateResponse('login.html', {'request': request})


@router.post('/add_book', tags=['Book'])
def add_book(
        title: str = Form(...),
             author: str = Form(...),
             description: Optional[str] = Form(None),
             image_url: UploadFile = File(None),
             db: Session = Depends(get_db)
):
    book = db.query(Book).filter(Book.title == title).first()

    if book:
        return 'книга уже существует'
    image_path = None
    if image_url:
        ext = image_url.filename.split('.')[-1]
        filename = f"{uuid4().hex}.{ext}"
        save_path = os.path.join("app", "static", "images", filename)
        with open(save_path, mode="wb") as file:
            file.write(image_url.file.read())
        image_path = f"app/static/images/{filename}"

    new_book = Book(title=title, author=author, description=description, image_url=image_path)
    db.add(new_book)
    db.commit()


@router.post('/add_review', tags=['Review'])
def add_review(
        request: Request,
        book_id: int = Form(...), text: str = Form(...),
        rating: str = Form(...),
        db: Session = Depends(get_db)
):
    user_id = request.cookies.get('user_id')

    if not user_id:
        raise HTTPException(status_code=401, detail='Вы не авторизованы')

    user = db.query(User).filter(User.id == int(user_id)).first()
    book = db.query(Book).filter(Book.id == int(book_id)).first()

    if not user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')

    if not book:
        raise HTTPException(status_code=404, detail='Книга не найдена')

    new_review = Review(text=text, rating=rating, book_id=book.id, user_id=user.id)
    db.add(new_review)
    db.commit()


@router.delete('/delete_review', tags=['Review'])
def delete_review(
        request: Request,
                  review_id: int = Form(...),
                  db: Session = Depends(get_db)
                  ):
    user_id = request.cookies.get('user_id')

    if not user_id:
        raise HTTPException(status_code=401, detail='Вы не авторизованы')

    review = db.query(Review).filter(Review.id == int(review_id)).first()

    if not review:
        raise HTTPException(status_code=401, detail='Рецензия не найдена')

    if review.id != int(user_id):
        raise HTTPException(status_code=403, detail='Нельзя удалить чужую  рецензию')

    db.delete(review)
    db.commit()

    return 'Рецензия успешно удалена'


@router.get('/user_review/{user_id}', tags=['Review'])
def list_user_reviews(user_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.user_id == int(user_id)).all()
    response = []
    for review in reviews:
        response.append(
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "book_id": review.book_id
            }
        )
    return response

@router.get("/reviews", tags=['Review'])
def list_review(
        db: Session = Depends(get_db)
):
    all_reviews = db.query(Review).all()
    response = []

    for review in all_reviews:
        response.append(
            {
                "id": review.id,
                "text": review.text,
                "rating": review.rating,
                "user_id": review.user_id,
                "book_id": review.book_id
            }
        )
    return response
@router.get("/users", tags=['User'])
def list_user(
        db: Session = Depends(get_db)
):
    all_users = db.query(User).all()
    response = []

    for user in all_users:
        response.append(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        )
        return response