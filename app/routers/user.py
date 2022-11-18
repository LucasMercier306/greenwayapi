from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from app.serializers.userSerializers import userResponseEntity

from app.database import User
from .. import schemas, oauth2

router = APIRouter()

#get connected user #work
@router.get('/me', response_model=schemas.UserResponse )
def get_me(user_id: str = Depends(oauth2.require_user) ):
    print(user_id)
    print(User.find_one({'_id': ObjectId(str(user_id))}))
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    return {"status": "success", "user": user}

#update user by id
@router.put('/user')
def update_user(user_id: str ):
    
    newval = {
      "firstname": "string",
      "lastname": "string",
      "phone": "string",
      "wantnotification": True,
      "wanthistory": True,
      "level": 0,
      "co2saved": 0,
      "email": "lucasok@gmail.com",
      "photo": "string",
      "role": "string",
    }
    
    print(newval)
    
    User.update_one({"_id" : ObjectId(f"{user_id}")}, {"$set": newval}, upsert=True)
    
    return {"status": "success update", "user": f"{user_id}"}

#delete user by id #work
@router.delete('/user')
def delete_user(user_id: str ):
    User.delete_one({'_id': ObjectId(str(user_id))})
    return {"status": "success delete", "user": "byid"}


#get tout les users
@router.get('/user', response_model=schemas.UserResponse )
def get_all_user():
    
    print(User.find())
    user = userResponseEntity(User.find())
    return  {"status": "success", "user": user}


#get user by id
@router.get('/user', response_model=schemas.UserResponse)
def get_user_by_id(user_id: str ):
    print(user_id)
    print(User.find_one({'_id': ObjectId(str(user_id))}))
    user = userResponseEntity(User.find_one({'_id': ObjectId(str(user_id))}))
    return {"status": "success", "user": user}