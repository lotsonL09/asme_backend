from pydantic import BaseModel

class User(BaseModel):
    id_user:int
    dni:str
    first_name:str
    last_name:str
    team_name:str
    area_name:str