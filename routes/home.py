from fastapi import APIRouter,status,HTTPException
from db.queries.tickets import (get_tickets,get_last_booked_ticket,
                                update_status_ticket,is_available,
                                reset_ticket)
from extra.helper_functions import get_qr
from entities.ticket import To_Form_Tickets,Confirm_Ticket_Sale

home=APIRouter(prefix="/home",
            tags=["home screen"],
            responses={status.HTTP_404_NOT_FOUND:{"message":"Screen not found"}})

@home.get("/available_tickets")
async def get_available_tickets(id_user:int):
    tickets_data=get_tickets(id_user=id_user,id_status=1)
    return {
        'detail':'Available tickets',
        'tickets_data':tickets_data
    }

@home.get("/booked_tickets")
async def get_booked_tickets(id_user:int):
    tickets_data=get_tickets(id_user=id_user,id_status=2)
    return {
        'detail':'Booked tickets',
        'tickets_data':tickets_data
    }

@home.get("/pending_tickets")
async def get_booked_tickets(id_user:int):
    tickets_data=get_tickets(id_user=id_user,id_status=3)
    return {
        'detail':'Pending tickets',
        'tickets_data':tickets_data
    }

@home.get("/sold_tickets")
async def get_remain_tickets(id_user:int):
    amount_tickets=get_tickets(id_user=id_user,id_status=4)
    return {
        'detail':'Sold tickets',
        'amount':amount_tickets
    }

@home.get("/last_sold_ticket")
async def get_booked_ticket(id_user:int):
    ticket_number=get_last_booked_ticket(id_user=id_user)
    return {
            "detail":"Booked ticket found",
            "number":ticket_number[0]
        }

@home.post("/qr_section")
async def get_link_qr(data_tickets:To_Form_Tickets):
    
    #TODO: Verificar que a menos que este disponible, se bloquee el acceso al qr

    for ticket in data_tickets.tickets_data:
        if is_available(id_ticket=ticket.id_ticket):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Los tickets ya fueron reservados.")

    for ticket in data_tickets.tickets_data:
        update_status_ticket(id_ticket=ticket.id_ticket,id_status=2)

    link_data=get_qr(data=data_tickets.model_dump_json())
    return link_data

@home.put("/confirm_ticket_sale")
async def confirm_sale(confirm_ticket:Confirm_Ticket_Sale):
    if confirm_ticket.confirm:
        update_status_ticket(id_ticket=confirm_ticket.id_ticket,id_status=4)
    else:
        reset_ticket(id_ticket=confirm_ticket.id_ticket)
    return {
        "detail":"Ticket updated"
    }
