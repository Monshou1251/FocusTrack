from fastapi import FastAPI
import uvicorn

from app.api.v1.endpoints import auth 

app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
