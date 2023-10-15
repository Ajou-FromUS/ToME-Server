from fastapi import APIRouter
from views import auth_view

auth = APIRouter(
    prefix='/auth'
)


@auth.post("/")
def auth_token(token: str):
    res = auth_view.verify_jwt(token)
    return res
