"""Auth Router — Login, Register, Token Refresh."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db
from models import User
from schemas import LoginRequest, RegisterRequest, TokenResponse, UserResponse
from auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token, get_current_user_id

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.username == req.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")

    token_data = {"sub": str(user.id), "role": user.role, "username": user.username}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token,
        role=user.role, username=user.username
    )


@router.post("/register", response_model=UserResponse)
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(select(User).where(
        (User.username == req.username) | (User.email == req.email)))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username or email already exists")

    user = User(
        username=req.username, email=req.email,
        password_hash=hash_password(req.password), role=req.role
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user_id = int(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or disabled")

    token_data = {"sub": str(user.id), "role": user.role, "username": user.username}
    new_access = create_access_token(token_data)
    new_refresh = create_refresh_token(token_data)
    return TokenResponse(
        access_token=new_access, refresh_token=new_refresh,
        role=user.role, username=user.username
    )


@router.get("/me", response_model=UserResponse)
async def get_me(user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
