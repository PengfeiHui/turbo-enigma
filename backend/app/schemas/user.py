from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=20, description="用户名（昵称）")


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=20, description="密码")

    @validator('username')
    def validate_username(cls, v):
        """验证用户名不能为纯数字"""
        if v.isdigit():
            raise ValueError('用户名不能为纯数字')
        # 只允许中文、英文、数字、下划线
        import re
        if not re.match(r'^[一-龥a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含中文、英文、数字和下划线')
        return v


class UserLogin(BaseModel):
    account: str = Field(..., description="11位数字账号")
    password: str = Field(..., description="密码")

    @validator('account')
    def validate_account(cls, v):
        """验证账号格式"""
        if not v.isdigit() or len(v) != 11:
            raise ValueError('账号必须是11位数字')
        return v


class UserResponse(UserBase):
    id: int
    account: str = Field(..., description="11位数字账号")
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=20)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
