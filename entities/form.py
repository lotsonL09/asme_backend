from pydantic import BaseModel

class FormData(BaseModel):
    first_name:str
    last_name:str
    email:str
    dni:str
    cell_phone:str