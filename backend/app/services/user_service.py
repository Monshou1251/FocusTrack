from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.user import User, OAuthAccount
from app.schemas.auth import UserAuthForm
from app.core.security import hash_password, verify_password, create_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login') 


async def register_user(form_data, db):
    email = form_data.email
    password = form_data.password
    result = await db.execute(select(User).filter(User.email == email))
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(password)
    user = User(email=email, hashed_password=hashed_password)
    
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {"msg": "User created successfully."}


# async def authenticate_user(email: str, password: str, db: AsyncSession):
async def authenticate_user(form_data: UserAuthForm, db: AsyncSession):
    
    print(form_data.password)
    check_user_exist = await db.execute(select(User).filter(User.email == form_data.email))
    user = check_user_exist.scalar()
    
    if not user or user.hashed_password is None:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, 
user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")


    return {"create_access_token": "Good job mista!"}

    # result = await db.execute(select(User).filter(User.email == email))
    # user = result.scalars().first()
    #
    # if not user:
    #     raise HTTPException(status_code=401, detail="Incorrect email or password")
    #
    # if not verify_password(password, user.hashed_password):
    #     raise HTTPException(status_code=401, detail="Incorrect email or password")
    #
    # access_token = create_access_token({"sub": user.email})
    # 
    # return {"access_token": access_token, "token_type": "bearer"}


async def register_oauth_user(provider: str, provider_id: str, email: str, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == email))

    existing_user = result.scalars().first()

    if existing_user:
        oauth_result = await db.execute(select(OAuthAccount).filter(
            OAuthAccount.provider == provider, OAuthAccount.user_id == existing_user.id
        ))
        oauth_account = oauth_result.scalars().first()

        if oauth_account:
            return {"msg": "User already registerd with this OAuth provider"}

        oauth_account = OAuthAccount(provider=provider, provider_id=provider_id, user_id=existing_user.id)
        db.add(oauth_account)
        await db.commit()

        return {"msg": "OAuth account linked to existing user."}

    user = User(email=email, is_verified=True)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    oauth_account = OAuthAccount(provider=provider, provider_id=provider_id, user_id=user.id)
    db.add(oauth_account)
    await db.commit()

    return {"msg": "User registered via OAuth."}


async def get_current_user(token):
    pass
