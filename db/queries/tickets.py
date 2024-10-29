from sqlalchemy import Select,func,Update,desc
from db.db_tables.db_tables import (tickets_table,buyers_table)
from extra.helper_functions import (execute_get_one,execute_get,
                                    get_update_query,execute_update,
                                    get_insert_query,execute_insert)
from extra.schemas_function import scheme_available_ticket,scheme_booked_ticket,scheme_pending_sold_ticket
from entities.ticket import Ticket
from fastapi import HTTPException,status
from datetime import datetime

query_sold_tickets=(Select(
    tickets_table.c.id_ticket,
    tickets_table.c.number_ticket,
    buyers_table.c.first_name,
    buyers_table.c.last_name,
    buyers_table.c.DNI,
    buyers_table.c.email,
    buyers_table.c.cell_phone,
    tickets_table.c.booking_time,
    tickets_table.c.evidence
).join(buyers_table,buyers_table.c.id_buyer == tickets_table.c.id_buyer)
.where(tickets_table.c.id_status == 4))

query_available_tickets=(Select(
    tickets_table.c.id_ticket,
    tickets_table.c.number_ticket
).where(tickets_table.c.id_status == 1))

query_booked_tickets=(Select(
    tickets_table.c.id_ticket,
    tickets_table.c.number_ticket
).where(tickets_table.c.id_status == 2))

query_pending_tickets=(Select(
    tickets_table.c.id_ticket,
    tickets_table.c.number_ticket,
    buyers_table.c.first_name,
    buyers_table.c.last_name,
    buyers_table.c.DNI,
    buyers_table.c.email,
    buyers_table.c.cell_phone,
    tickets_table.c.booking_time,
    tickets_table.c.evidence
).join(buyers_table,buyers_table.c.id_buyer == tickets_table.c.id_buyer)
.where(tickets_table.c.id_status == 3))

query_last_sold_ticket=(Select(
    tickets_table.c.number_ticket
).where(tickets_table.c.id_status == 4)
.order_by(desc(tickets_table.c.booking_time))
.limit(1))

query_is_booked=(Select(
    tickets_table.c.id_status
))


def get_tickets(id_user,id_status:int):
    query=None
    list_tickets=[]

    match id_status:
        case 1: #available
            query = query_available_tickets.where(tickets_table.c.id_user == id_user)
        case 2: #booked
            query = query_booked_tickets.where(tickets_table.c.id_user == id_user)
        case 3: #pending
            query = query_pending_tickets.where(tickets_table.c.id_user == id_user)
        case 4: #sold
            query=query_sold_tickets.where(tickets_table.c.id_user == id_user)
            
    tickets_data = execute_get(query=query)
    for register in tickets_data:
        ticket=None
        match id_status:
            case 1: #available
                ticket=Ticket(**scheme_available_ticket(register))
            case 2: #booked
                ticket=Ticket(**scheme_booked_ticket(register))
            case _: #pending and sold
                ticket=Ticket(**scheme_pending_sold_ticket(register))
        list_tickets.append(ticket)

    return {
        "amount":len(list_tickets),
        "tickets":list_tickets
    }

def get_last_booked_ticket(id_user):
    query=query_last_sold_ticket.where(tickets_table.c.id_user == id_user)
    ticket_number = execute_get_one(query=query)
    if ticket_number is None:
        raise HTTPException(detail="No booked found",
                            status_code=status.HTTP_404_NOT_FOUND)
    else:
        return ticket_number
    

def register_ticket(id_tickets:list[int],
                    first_name:str,last_name:str,
                    dni:str,email:str,
                    cell_phone:str,booking_time:datetime):
    
    #TODO: Agregar el registro a la TABLA buyers
    params_buyer={
        "first_name":first_name,
        "last_name":last_name,
        "DNI":dni,
        "email":email,
        "cell_phone":cell_phone,
    }
    query_buyer=get_insert_query(table=buyers_table,params=params_buyer)
    id_buyer=execute_insert(query=query_buyer)

    #TODO: MODIFICAR LA TABLA tickets
    
    #filters = {"id_ticket": [781, 782]}

    query_ticket=get_update_query(table=tickets_table,filters={"id_ticket":id_tickets},params={"id_status":3,
                                                                                    "booking_time":booking_time,
                                                                                    "id_buyer":id_buyer})
    execute_update(query=query_ticket)

    return id_buyer

"""
action : 
    update_status


{
    "action":"something",
    "value":""
}
"""

def update_status_ticket(id_ticket:int,id_status:int):
    query=get_update_query(table=tickets_table,filters={"id_ticket":id_ticket},params={"id_status":id_status})
    execute_update(query=query)

def update_url_ticket(id_ticket:int,url_image:str):
    query=get_update_query(table=tickets_table,filters={"id_ticket":id_ticket},params={"evidence":url_image})
    execute_update(query=query)

def is_booked(id_ticket:int):
    query=query_is_booked.where(tickets_table.c.id_ticket == id_ticket)
    status=execute_get_one(query=query)[0]
    if status != 1:
        return False
    else:
        return True
