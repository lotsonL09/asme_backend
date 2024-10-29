from fastapi import APIRouter,status,Request,Form,File,UploadFile,Query
from fastapi.templating import Jinja2Templates
from entities.ticket import From_Form_Tickets
from entities.form import ImageForm
from extra.helper_functions import decode_url_safe_token,upload_to_cloudinary
from db.queries.tickets import register_ticket,update_url_ticket,is_booked
from datetime import datetime
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
    form_data:From_Form_Tickets
):

    buyer_data=form_data.buyer_data
    #TODO: Verificar si los tickets ya fueron vendidos
    tickets_data=form_data.tickets_data

    id_tickets=[]

    for ticket_data in tickets_data:

        if is_booked(id_ticket=ticket_data.id_ticket):
            return templates.TemplateResponse("disclaimer.1.html",{"request":request})
        else:
            id_tickets.append(ticket_data.id_ticket)

    booking_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _=register_ticket(id_tickets=id_tickets,first_name=buyer_data.first_name,last_name=buyer_data.last_name,
                    dni=buyer_data.dni,email=buyer_data.email,cell_phone=buyer_data.cell_phone,
                    booking_time=booking_time)

    return templates.TemplateResponse("send_image.1.html",{"request":request,"data":{"id_tickets":id_tickets}})

@form.post("/image")
async def get_image_form(
    request:Request,
    id_tickets: str = Form(...), 
    image: UploadFile = File(...)):

    id_tickets_list=json.loads(id_tickets)

    image_content = await image.read()

    url_image=upload_to_cloudinary(image=image_content,id_tickets=id_tickets_list)

    for id_ticket in id_tickets_list:
        update_url_ticket(id_ticket=id_ticket,url_image=url_image)

    return templates.TemplateResponse("image_sent.1.html",{"request":request})



