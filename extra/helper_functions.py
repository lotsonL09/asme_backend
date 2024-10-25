from db.db_session import engine
from sqlalchemy.orm import sessionmaker
import qrcode
from fastapi import HTTPException,status
from itsdangerous import URLSafeTimedSerializer
import base64
import io

from config.config import settings

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