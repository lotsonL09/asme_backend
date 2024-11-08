from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.login import login
from routes.home import home
from routes.form import form
from fastapi.staticfiles import StaticFiles

import uvicorn

app=FastAPI()

app.mount("/static",StaticFiles(directory="static"),name="static")

app.include_router(login)
app.include_router(home)
app.include_router(form)

origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        'main:app',
        port=8080
    )


