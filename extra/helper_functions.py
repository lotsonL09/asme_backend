import cloudinary.uploader
from db.db_session import engine
from sqlalchemy.orm import sessionmaker
import qrcode
from fastapi import HTTPException,status
from itsdangerous import URLSafeTimedSerializer
import base64
from sqlalchemy import update,insert,delete
from config.config import settings
import cloudinary
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

Session=sessionmaker(engine)

serializer=URLSafeTimedSerializer(
    secret_key=settings.SECRET_KEY
)

def execute_get(query):
    with Session() as session:
        result=session.execute(query).fetchall()
        return result

def execute_get_one(query):
    with Session() as session:
        result=session.execute(query).first()
        return result

def execute_insert(query):
    with Session() as session:
        register_inserted=session.execute(query)
        session.commit()
        id=register_inserted.inserted_primary_key[0]
    return id

def execute_update(query):
    with Session() as session:
        session.execute(query)
        session.commit()

def get_update_query(table, filters: dict, params: dict):
    query = update(table)
    for column_name, value in filters.items():
        if isinstance(value, list):
            query = query.where(getattr(table.c, column_name).in_(value))
        else:
            query = query.where(getattr(table.c, column_name) == value)
    query = query.values(**params)
    return query


def get_insert_query(table,params:dict):
    query=insert(table).values(**params)
    return query

def get_delete_query(table:str,params:dict):
    query=delete(table)
    for colum_name,value in params.items():
        query=query.where(getattr(table.c,colum_name) == value)
    return query

def execute_delete(query):
    with Session() as session:
        session.execute(query)
        session.commit()

def create_url_safe_token(data):
    token=serializer.dumps(obj=data)
    return token

def decode_url_safe_token(token:str):
    try:
        token_data=serializer.loads(token)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

def get_qr(data):
    url="http://127.0.0.1:8000/form"
    encoded_data=create_url_safe_token(data=data)
    full_url=f"{url}/{encoded_data}"
    return {
        "link":full_url
    }


cloudinary.config(
    cloud_name="ddcb3fk7s",
    api_key="727551972448292",
    api_secret="vPMqCTqDL8QwFjqTqfCQkn-W0fk",
    secure=True
)

def upload_to_cloudinary(image,id_tickets:list[int]):

    public_id="voucher_yape_id_ticket"

    for id_ticket in id_tickets:
        public_id+=f"_{id_ticket}"

    response_cloud=cloudinary.uploader.upload(image,
                            public_id=public_id,
                            folder="asme_pruebas")
    url_file=response_cloud["secure_url"]

    return url_file


def generate_ticket(ticket:str):
    
    url_image="https://res.cloudinary.com/ddcb3fk7s/image/upload/v1730138591/asme_ticket_format_biaecm.jpg"   

    response=requests.get(url_image)

    text_ticket=f"N° {ticket}"

    font=ImageFont.truetype("arial.ttf",size=120)

    color_text=(165,42,42)

    x,y=1765,70

    if response.status_code == 200:
        image=Image.open(BytesIO(response.content))

        image_text=Image.new("RGBA",(500,500),(255,255,255,0))

        draw_text=ImageDraw.Draw(image_text)

        draw_text.text((0,0),text_ticket,font=font,fill=color_text)

        draw_text_rotate=image_text.rotate(90,expand=1)

        image.paste(draw_text_rotate,(x,y),draw_text_rotate)

        return image
