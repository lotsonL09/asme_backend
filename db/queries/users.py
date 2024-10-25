from sqlalchemy import Select
from db.db_tables.db_tables import (users_table,teams_table,areas_table)
from extra.schemas_function import scheme_user
from extra.helper_functions import execute_get_one
from entities.users import User

from fastapi import HTTPException,status

users_query=(Select(
    users_table.c.id_user,
    users_table.c.DNI,
    users_table.c.first_name,
    users_table.c.last_name,
    teams_table.c.team_name,
    areas_table.c.area_name
).join(teams_table,teams_table.c.id_team == users_table.c.id_team)
.join(areas_table,areas_table.c.id_area == users_table.c.id_area))


def get_user_by_dni(dni:str) -> User:
    query=users_query.where(users_table.c.DNI == dni)
    user_row=execute_get_one(query=query)
    if user_row != None:
        user_scheme=scheme_user(user_row=user_row)
        user_found=User(**user_scheme)
        return user_found
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
