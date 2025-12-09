from pydantic import BaseModel

class UserInDB(BaseModel):
    """
    Represents how the User is stored in MongoDB.
    Unlike SQL, we don't define columns here, just the expected shape 
    for when we insert data.
    """
    full_name: str
    username: str
    email: str
    hashed_password: str
    is_active: bool = True
    role: str = "role_user"
    
    class Config:
        # Helper to allow Pydantic to work seamlessly with MongoDB BSON dicts
        populate_by_name = True