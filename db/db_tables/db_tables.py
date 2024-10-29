from sqlalchemy import (Table,Column,Integer,String,
                        Boolean,MetaData,ForeignKey,DateTime)

metadata_obj=MetaData()

groups_table=Table(
    "grupos",
    metadata_obj,
    Column('id_group',Integer,autoincrement=True,primary_key=True),
    Column('group_name',String,unique=True),
    Column('coordinator',String)
)

teams_table=Table(
    "teams",
    metadata_obj,
    Column("id_team",Integer,autoincrement=True,primary_key=True),
    Column("team_name",String)
)

areas_table=Table(
    "areas",
    metadata_obj,
    Column("id_area",Integer,autoincrement=True,primary_key=True),
    Column("area_name",String)
)

status_table=Table(
    "status",
    metadata_obj,
    Column("id_status",Integer,autoincrement=True,primary_key=True),
    Column("status_name",String)
)

users_table=Table(
    "users",
    metadata_obj,
    Column("id_user",Integer,autoincrement=True,primary_key=True),
    Column("DNI",String),
    Column("first_name",String),
    Column("last_name",String),
    Column("checkbooks",String),
    Column("id_group",Integer,ForeignKey("grupos.id_group")),
    Column("id_area",Integer,ForeignKey("areas.id_area")),
    Column("id_team",Integer,ForeignKey("teams.id_team"))
)

buyers_table=Table(
    "buyers",
    metadata_obj,
    Column("id_buyer",Integer,autoincrement=True,primary_key=True),
    Column("first_name",String),
    Column("last_name",String),
    Column("DNI",String),
    Column("email",String),
    Column("cell_phone",String),
)

tickets_table=Table(
    "tickets",
    metadata_obj,
    Column("id_ticket",Integer,autoincrement=True,primary_key=True),
    Column("number_ticket",String),
    Column("booked",Boolean),
    Column("booking_time",DateTime),
    Column("evidence",String),
    Column("id_status",ForeignKey("status.id_status")),
    Column("id_user",Integer,ForeignKey("users.id_user")),
    Column("id_buyer",Integer,ForeignKey("buyers.id_buyer"))
)

