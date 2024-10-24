from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.login import login
from routes.home import home

import uvicorn

app=FastAPI()
app.include_router(login)
app.include_router(home)

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
        reload=True
    )


