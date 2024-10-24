from fastapi import APIRouter,status
from entities.login import Login_Form
from db.queries.users import get_user_by_dni

login=APIRouter(prefix="/login",
                tags=["Login screen"],
                responses={status.HTTP_404_NOT_FOUND:{"message":"Screen not found"}})

@login.post('/')
async def login_root(form:Login_Form):
    user=get_user_by_dni(dni=form.dni)
    return {
        "detail":"User found",
        "user_data":user
    }