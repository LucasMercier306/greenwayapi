from fastapi import APIRouter, Depends
from bson.objectid import ObjectId
from app.serializers.userSerializers import userResponseEntity
from fastapi.encoders import jsonable_encoder

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

#update user by id #work
@router.put('/user' )
def update_user(user_id: str, newval: schemas.UserUpdateSchema ):

    parse = jsonable_encoder(newval)
    print(parse)
        
    User.find_one_and_update({"_id" : ObjectId(f"{user_id}")}, {"$set": parse}, upsert=True)
    return {"status": "success update", "user": f"{user_id}"}

#delete user by id #work
@router.delete('/user')
def delete_user(user_id: str ):
    User.delete_one({'_id': ObjectId(str(user_id))})
    return {"status": "success delete", "user": user_id}


#get tout les users #work
@router.get('/userall', response_model=schemas.UserResponse )
def get_all_user():
    print(User.find_one())
    user = userResponseEntity(User.find_one())
    return  {"status": "success", "user": user}


