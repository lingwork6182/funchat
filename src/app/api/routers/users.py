from fastapi import APIRouter, Depends, HTTPException

from src.app.repositories.crud_demo import UserDao

router = APIRouter(prefix="/users", tags=["users"])

# @router.post("/", response_model=UserResponse)
# async def create_user(user_data: UserCreate):
#     """创建用户API端点"""
#     try:
#         return await UserDao.create_user(user_data.dict())
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))