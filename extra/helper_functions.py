import cloudinary.uploader
from db.db_session import engine
from sqlalchemy.orm import sessionmaker
import qrcode
from fastapi import HTTPException,status
from itsdangerous import URLSafeTimedSerializer
import base64
import io
from sqlalchemy import update,insert
from config.config import settings
import cloudinary


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
    qr=qrcode.make(full_url)

    image_io=io.BytesIO()

    qr.save(image_io,format="PNG")

    image_io.seek(0)

    qr_base64=base64.b64encode(image_io.getvalue()).decode('utf-8')

    return {
        "link":full_url,
        "qr":qr_base64
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
