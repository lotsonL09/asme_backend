from pydantic import BaseModel
from datetime import datetime

class Ticket(BaseModel):
    id_ticket:int | None = None 
    number_ticket:str | None = None
    first_name:str | None = None
    last_name:str | None = None
    DNI:str | None = None
    email:str | None = None
    cell_phone:str | None = None
    booking_time:datetime | None = None
    evidence:str | None = None

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

class Confirm_Ticket_Sale(BaseModel):
    id_ticket:int
    confirm:bool