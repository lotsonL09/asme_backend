from sqlalchemy import Select,func
from db.db_tables.db_tables import (tickets_table)
from extra.helper_functions import execute_get

from fastapi import HTTPException,status

query_amount_tickets=Select(func.count()).select_from(tickets_table)

query_last_ticket=(Select(
    tickets_table.c.number_ticket
).where(tickets_table.c.booked == 1)
.limit(1))


def get_tickets(id_user,booked=False):
    query=None
    if booked:
        query=query_amount_tickets.where(tickets_table.c.booked == 1).where(tickets_table.c.id_user == id_user)
    else:
        query=query_amount_tickets.where(tickets_table.c.booked == 0).where(tickets_table.c.id_user == id_user)
    amount = execute_get(query=query)[0]
    print(amount)
    return amount

def get_last_booked_ticket(id_user):
    query=query_last_ticket.where(tickets_table.c.id_user == id_user)
    ticket_number = execute_get(query=query)
    if ticket_number is None:
        raise HTTPException(detail="No booked found",
                            status_code=status.HTTP_404_NOT_FOUND)
    else:
        return ticket_number
