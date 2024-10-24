from fastapi import APIRouter,status
from db.queries.tickets import get_tickets,get_last_booked_ticket

home=APIRouter(prefix="/home",
            tags=["home screen"],
            responses={status.HTTP_404_NOT_FOUND:{"message":"Screen not found"}})

@home.get("/booked_tickets")
async def get_booked_tickets(id:int):
    amount_tickets=get_tickets(id_user=id,booked=True)
    return {
        'detail':'Booked tickets',
        'amount':amount_tickets
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