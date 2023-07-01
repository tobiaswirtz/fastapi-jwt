from pydantic import BaseModel, Field, EmailStr

class PostSchema(BaseModel):
    id : int = Field(default=None)
    title : str = Field(default=None)
    content : str = Field(default=None)
    class Config:
        schema_extra = {
            "post_demo": {
                "title": "To the Moon",
                "content": "We are going to get so rich"        
            }
        }

class UserSchema(BaseModel):
    fullname : str = Field(default=None)
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        schema_user = {
            "user_demo": {
                "name": "Tobias",
                "email": "tobias.wirtz1+test@gmail.com",
                "password": "123456"
            }
        }

class UserLoginSchema(BaseModel):
    email : EmailStr = Field(default=None)
    password : str = Field(default=None)
    class Config:
        schema_userlogin = {
            "user_demo": {
                "email": "tobias.wirtz1+test@gmail.com",
                "password": "123456"
            }
        }