from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse, ChangePasswordRequest, TokenResponse
from app.services.auth_service import auth_service
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    try:
        user = auth_service.create_user(
            db=db,
            username=user_data.username,
            password=user_data.password
        )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user, error_message = auth_service.authenticate_user(db, credentials.username, credentials.password)
    if not user:
        if error_message == "user_not_found":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="该用户尚未注册，请先注册",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:  # wrong_password
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="密码错误",
                headers={"WWW-Authenticate": "Bearer"},
            )

    token = auth_service.generate_token(user)
    return TokenResponse(
        access_token=token,
        user=UserResponse.from_orm(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改密码"""
    success = auth_service.change_password(
        db=db,
        user=current_user,
        old_password=request.old_password,
        new_password=request.new_password
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="原密码错误"
        )

    return {"message": "密码修改成功"}
