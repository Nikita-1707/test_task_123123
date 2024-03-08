from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/')
def get_home_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})


@router.get('/registration')
def get_registration_page(request: Request):
    return templates.TemplateResponse('registration.html', {'request': request})


@router.get('/login')
def get_login_page(request: Request):
    return templates.TemplateResponse('authorization.html', {'request': request})
