from pydantic import BaseModel
from datetime import datetime

class Ticket(BaseModel):
    id_ticket:int | None
    number_ticket:str | None
    first_name:str | None
    last_name:str | None
    DNI:str | None
    email:str | None
    cell_phone:str | None
    booking_time:datetime | None

class Ticket_db(BaseModel):
    id_ticket:int | None
    number_ticket:str | None

class Seller(BaseModel):
    first_name:str
    last_name:str
    email:str
    dni:str
    cell_phone:str

class To_Form_Tickets(BaseModel):
    tickets_data:list[Ticket_db]
    seller:str

class From_Form_Tickets(BaseModel):
    tickets_data:list[Ticket_db]
    buyer_data:Seller