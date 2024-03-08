from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/')
def get_home_page(request: Request):
    return templates.TemplateResponse('base.html', {'request': request})
