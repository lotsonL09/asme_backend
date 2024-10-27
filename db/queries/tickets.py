from sqlalchemy import Select,func,Update
from db.db_tables.db_tables import (tickets_table,buyers_table)
from extra.helper_functions import (execute_get_one,execute_get,
                                    get_update_query,execute_update,
                                    get_insert_query,execute_insert)
from extra.schemas_function import scheme_ticket
from entities.ticket import Ticket
from fastapi import HTTPException,status
from datetime import datetime

query_booked_tickets=(Select(
    tickets_table.c.id_ticket,
    tickets_table.c.number_ticket,
    buyers_table.c.first_name,
    buyers_table.c.last_name,
    buyers_table.c.DNI,
    buyers_table.c.email,
    buyers_table.c.cell_phone,
    tickets_table.c.booking_time
).join(buyers_table,buyers_table.c.id_buyer == tickets_table.c.id_buyer))

query_remain_tickets=(Select(
    tickets_table.c.id_ticket,
    tickets_table.c.number_ticket
))

query_last_ticket=(Select(
    tickets_table.c.number_ticket
).where(tickets_table.c.booked == 1)
.limit(1))


query_update_ticket=()


def get_tickets(id_user,booked=False):
    query=None
    list_tickets=[]
    if booked:
        query=query_booked_tickets.where(tickets_table.c.id_user == id_user)
    else:
        query=query_remain_tickets.where(tickets_table.c.booked == 0).where(tickets_table.c.id_user == id_user)
    tickets_data = execute_get(query=query)
    for register in tickets_data:
        ticket=Ticket(**scheme_ticket(register))
        list_tickets.append(ticket)

    return {
        "amount":len(list_tickets),
        "tickets":list_tickets
    }

def get_last_booked_ticket(id_user):
    query=query_last_ticket.where(tickets_table.c.id_user == id_user)
    ticket_number = execute_get_one(query=query)
    print(ticket_number)
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

    query_ticket=get_update_query(table=tickets_table,filters={"id_ticket":id_tickets},params={"booked":True,
                                                                                    "booking_time":booking_time,
                                                                                    "id_buyer":id_buyer})
    execute_update(query=query_ticket)

    return id_buyer
