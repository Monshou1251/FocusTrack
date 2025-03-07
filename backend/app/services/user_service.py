from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.db.models.user import User
from app.core.security import hash_password, verify_password, create_access_token

async def register_user(username: str, email: str, password: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    user = User(username=username, email=email, hashed_password=hashed_password)
    
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"msg": "User created successfully."}


async def authenticate_user(email: str, password: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == email))
    user = result.scalars().first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    
    # if not user.is_verified:
    #     raise HTTPException(status_code=403, detail="Email is not verified")
    
    access_token = create_access_token({"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}