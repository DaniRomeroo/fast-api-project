from pydantic import BaseModel, BeforeValidator, Field
from typing import Optional, Annotated

# --- ObjectId Helper ---
# MongoDB uses ObjectIds, but JSON uses strings. This helper converts them.
PyObjectId = Annotated[str, BeforeValidator(str)]

# --- Token Schemas ---
class LoginUser(BaseModel):
    user_id: str
    username: str
    role: str

class Login(BaseModel):
    code: int = 200
    message: str = "Login successful"
    access_token: str
    token_type: str
    user: LoginUser

class LoginData(BaseModel):
    username: Optional[str] = None

# --- User Schemas ---
class UserBase(BaseModel):
    full_name: str
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    # Map MongoDB's '_id' to 'id' in the JSON response
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    is_active: bool
    role: str

    class Config:
        populate_by_name = True
        from_attributes = True

class RegisterResponse(BaseModel):
    code: int = 201
    message: str = "User registered successfully",
    user_id: Optional[PyObjectId] = Field(alias="_id", default=None)
    email: str

    class Config:
        populate_by_name = True
        from_attributes = True

class LogoutRequest(BaseModel):
    token: str

class LogoutResponse(BaseModel):
    code: int = 200
    message: str = "Logout successful"