from sqlalchemy import Select,func
from db.db_tables.db_tables import (tickets_table,buyers_table)
from extra.helper_functions import execute_get_one,execute_get
from extra.schemas_function import scheme_ticket
from entities.ticket import Ticket
from fastapi import HTTPException,status

query_booked_tickets=(Select(
    tickets_table.c.id_ticket,
    tickets_table.c.number_ticket,
    buyers_table.c.first_name,
    buyers_table.c.last_name,
    buyers_table.c.DNI,
    buyers_table.c.email,
    buyers_table.c.cell_phone,
    tickets_table.c.booking_time
).join(buyers_table,buyers_table.c.id_ticket == tickets_table.c.id_ticket))

query_remain_tickets=(Select(
    tickets_table.c.id_ticket,
    tickets_table.c.number_ticket
))

query_last_ticket=(Select(
    tickets_table.c.number_ticket
).where(tickets_table.c.booked == 1)
.limit(1))


def get_tickets(id_user,booked=False):
    query=None
    list_tickets=[]
    if booked:
        query=query_booked_tickets.where(tickets_table.c.booked == 1).where(tickets_table.c.id_user == id_user)
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
