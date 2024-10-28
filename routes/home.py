from fastapi import APIRouter,status
from db.queries.tickets import get_tickets,get_last_booked_ticket
from extra.helper_functions import get_qr
from entities.ticket import To_Form_Tickets

home=APIRouter(prefix="/home",
            tags=["home screen"],
            responses={status.HTTP_404_NOT_FOUND:{"message":"Screen not found"}})

@home.get("/booked_tickets")
async def get_booked_tickets(id:int):
    tickets_data=get_tickets(id_user=id,booked=True)
    return {
        'detail':'Booked tickets',
        'tickets_data':tickets_data
    }

@home.get("/remain_tickets")
async def get_remain_tickets(id:int):
    amount_tickets=get_tickets(id_user=id,booked=False)
    return {
        'detail':'Available tickets',
        'amount':amount_tickets
    }

@home.get("/last_booked_ticket")
async def get_booked_ticket(id:int):
    ticket_number=get_last_booked_ticket(id_user=id)
    return {
            "detail":"Booked ticket found",
            "number":ticket_number[0]
        }

@home.post("/qr_section")
async def get_link_qr(data_tickets:To_Form_Tickets):
    link_data=get_qr(data=data_tickets.model_dump_json())
    return link_data