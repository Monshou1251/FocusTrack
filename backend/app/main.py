from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, category, focus, journal

app = FastAPI()

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(focus.router, prefix="/api/v1/focus", tags=["focus"])
app.include_router(category.router, prefix="/api/v1/category", tags=["category"])
app.include_router(journal.router, prefix="/api/v1/journal", tags=["journal"])

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
