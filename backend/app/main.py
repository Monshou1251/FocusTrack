import os

from fastapi import FastAPI
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import auth, category, focus, journal
from app.core.rate_limiter import limiter

app = FastAPI()

# Configure rate limiter FIRST
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Then add routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(focus.router, prefix="/api/v1/focus", tags=["focus"])
app.include_router(category.router, prefix="/api/v1/category", tags=["category"])
app.include_router(journal.router, prefix="/api/v1/journal", tags=["journal"])

# CORS origins - для локального тестирования и production

# Разрешенные origins для CORS
# Для локального Docker тестирования: http://localhost
# Для локальной разработки: http://localhost:5173
# Для production: будет установлено через переменную окружения
cors_origins_str = os.getenv(
    "CORS_ORIGINS",
    "http://localhost,http://localhost:5173"
)
cors_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}
