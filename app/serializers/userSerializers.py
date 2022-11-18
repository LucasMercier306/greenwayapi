def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "phone": user["phone"],
        "wantnotification": user["wantnotification"],
        "wanthistory": user["wanthistory"],
        "level": user["level"],
        "co2saved": user["co2saved"],
        "email": user["email"],
        "role": user["role"],
        "photo": user["photo"],
        "verified": user["verified"],
        "password": user["password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def userResponseEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "phone": user["phone"],
        "wantnotification": user["wantnotification"],
        "wanthistory": user["wanthistory"],
        "level": user["level"],
        "co2saved": user["co2saved"],
        "email": user["email"],
        "role": user["role"],
        "photo": user["photo"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"]
    }


def embeddedUserResponse(user) -> dict:
    return {
        "id": str(user["_id"]),
        "firstname": user["firstname"],
        "lastname": user["lastname"],
        "phone": user["phone"],
        "wantnotification": user["wantnotification"],
        "wanthistory": user["wanthistory"],
        "level": user["level"],
        "co2saved": user["co2saved"],
        "email": user["email"],
        "photo": user["photo"]
    }


def userListEntity(users) -> list:
    return [userEntity(user) for user in users]
