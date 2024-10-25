from fastapi import APIRouter,status,Request,Form,File,UploadFile,Query
from fastapi.templating import Jinja2Templates
from entities.ticket import To_Form_Tickets
from extra.helper_functions import decode_url_safe_token

import urllib.parse
import json

form=APIRouter(prefix="/form",
            tags=["Form page"],
            responses={status.HTTP_404_NOT_FOUND:{"message":"Page not found"}})

templates=Jinja2Templates(directory="templates")

@form.get("/{data}")
async def get_form(request:Request,data:str):
    tickets_data=decode_url_safe_token(token=data)
    tickets_data=json.loads(tickets_data)
    return templates.TemplateResponse("formulario.1.html",{"request":request,"data":tickets_data})

@form.post("/data_form")
async def get_data_form(
    request:Request,
    first_name:str = Form(...),
    last_name:str = Form(...),
    email:str = Form(...),
    dni:str = Form(...),
    cell_phone:str = Form(...),
):
    print(first_name)
    print(last_name)
    print(email)
    print(dni)
    print(cell_phone)
    return templates.TemplateResponse("send_image.1.html",{"request":request})

@form.post("/image")
async def get_image_form(
    request:Request,
    file:UploadFile=File()):

    contents=await file.read()

    print(contents)

    return templates.TemplateResponse("image_sent.1.html",{"request":request})



