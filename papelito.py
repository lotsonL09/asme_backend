from PIL import Image, ImageDraw, ImageFont
import cloudinary
from io import BytesIO
import requests

url_image="https://res.cloudinary.com/ddcb3fk7s/image/upload/v1730135721/asme_ticket_e3yljd.jpg"

response=requests.get(url_image)

id_ticket="2020"

font=ImageFont.truetype("arial.ttf",size=72)

x,y=1200,50

if response.status_code == 200:
    image=Image.open(BytesIO(response.content))

    image_draw=ImageDraw.Draw(image)

    for i, char in enumerate(id_ticket):
        image_draw.text((x,y+i * 60),char,font=font,fill='black')
    
    image.show()

