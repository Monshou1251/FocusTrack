from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
