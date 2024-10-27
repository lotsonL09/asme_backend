from pydantic import BaseModel

class FormData(BaseModel):
    first_name:str
    last_name:str
    email:str
    dni:str
    cell_phone:str

class ImageForm(BaseModel):
    id_tickets:list[int]
    image_form:str