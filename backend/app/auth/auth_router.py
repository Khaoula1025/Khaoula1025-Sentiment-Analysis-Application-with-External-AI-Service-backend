from app.schema import UserLoginSchema
from app.models import User
def check_user(data: UserLoginSchema,db):
    user=db.query(User).filter(
          (User.email == data.email) & (User.password==data.password)).first()
    if user :
            return True
    return False
