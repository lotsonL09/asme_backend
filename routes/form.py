from fastapi import APIRouter,status,Request,Form,File,UploadFile,Query
from fastapi.templating import Jinja2Templates
from entities.ticket import From_Form_Tickets,Ticket_db
from entities.form import ImageForm
from extra.helper_functions import decode_url_safe_token,upload_to_cloudinary,generate_ticket
from db.queries.tickets import register_ticket,update_url_ticket,is_pending
from datetime import datetime
import json
from config.mail import send_message,make_email_html

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
        if is_pending(id_ticket=ticket_data.id_ticket):
            return templates.TemplateResponse("disclaimer.1.html",{"request":request})
        else:
            id_tickets.append(ticket_data.id_ticket)

    booking_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    _=register_ticket(id_tickets=id_tickets,first_name=buyer_data.first_name,last_name=buyer_data.last_name,
                    dni=buyer_data.dni,email=buyer_data.email,cell_phone=buyer_data.cell_phone,
                    booking_time=booking_time)

    return templates.TemplateResponse("send_image.1.html",{"request":request,"data":{"tickets_data":[ticket.model_dump() for ticket in tickets_data],
                                                                                    'email':buyer_data.email,
                                                                                    "buyer_data":buyer_data.model_dump() }})

@form.post("/image")
async def get_image_form(
    request:Request,
    tickets_data: str = Form(...), 
    image: UploadFile = File(...),
    email:str=Form(...),
    buyer:str=Form(...)):

    tickets_list:list[Ticket_db]=json.loads(tickets_data)

    image_content = await image.read()

    id_tickets_list=[ticket["id_ticket"] for ticket in tickets_list]

    url_image=upload_to_cloudinary(image=image_content,id_tickets=id_tickets_list)

    for id_ticket in id_tickets_list:
        update_url_ticket(id_ticket=id_ticket,url_image=url_image)
    

    ticket_numbers=[ticket["number_ticket"] for ticket in tickets_list]

    buyer=json.loads(buyer)
    
    body_html=make_email_html(buyer=buyer,tickets=ticket_numbers)
    
    await send_message(recipients=[email],subject="Rifa ASME 2024",body=body_html,tickets=ticket_numbers)


    return templates.TemplateResponse("image_sent.1.html",{"request":request})
