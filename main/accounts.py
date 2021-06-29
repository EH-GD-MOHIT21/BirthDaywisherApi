from .models import *

def CreateUserAccount(data):
    username = data["username"]
    password = data["password"]
    first_name = data["first_name"]
    last_name = data["last_name"]
    email = data['email']

    user = User(username=username)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.set_password(password)


    user.save()

    return user

def CreateCustomUserAccount(user,data):
    date_of_birth = data["date_of_birth"]
    profile_pic = data["profile_pic"]

    cum = CustomUserModel(index=user)
    cum.date_of_birth = date_of_birth
    cum.profile_pic = profile_pic
    cum.auth_token = cum.authGenerator

    cum.save()

    return (True,cum.auth_token,cum)