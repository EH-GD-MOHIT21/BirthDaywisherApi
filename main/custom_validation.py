from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
import re
from datetime import datetime
from .models import CustomUserModel as cum
from .accounts import *
from .postman import *




def is_valid_username(username):
    if len(username) > 20 or len(username)<4:
        return (False,"username should be 4-20 chars long.")

    if username.isnumeric() or username.isalpha():
        return (False,"Username can't be only digits or alphabets.")

    userNameAllowedChars = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)] + ["-","_"] + [str(i) for i in range(0,10)]

    for char in username:
        if char not in userNameAllowedChars:
            return (False,f"Allowed characters as username: {userNameAllowedChars}")

    return (True,"Username Available")




def IsUserNameAvailable(username):

    try:

        User.objects.get(username=username)
        return (False,"Username Already Exists")

    except:

        data_obj = is_valid_username(username)
        if data_obj[0]:
            return (True,data_obj[1])
        else:
            return (False,data_obj[1])




def is_validatedPass(password,cnfrmpass):

    if password!=cnfrmpass:
        return False

    if len(password)<8:
        return False

    if password.isalpha() or password.isnumeric() or len(set(password))<3:
        return False

    return True




def iscorrectName(name):
    if name.isalpha() and len(name)>=3:
        return True

    else:
        return False





def is_valid_credentials(data):

    try:
        username = data['username']
        password = data['password']

        if check_password(password,User.objects.get(username=username).password) and cum.objects.get(index=User.objects.get(username=username)).is_verified:
            return (True,"success")

        elif check_password(password,User.objects.get(username=username).password):
            return (False,"Please Verify Yourself using link provided.")

        else:
            return (False,"No User Exists with credentials.")

    except Exception:
        return (False,"No User Exists with credentials.")



        

def is_validate_smvdu_mail(mail):

    REGEX_PATTERN = r"[1-9][1-9][a-z][a-z][a-z][0-9][0-9][0-9]@smvdu.ac.in"
    search_obj = re.search(REGEX_PATTERN,mail)

    if search_obj == ' ' or search_obj == None:
        return False

    else:
        if not alreadyexistsmail(mail):
            return True
        else:
            return False



def alreadyexistsmail(email):

    try:
        User.objects.get(email=email)
        return True

    except:
        return False



def MainDataChecker(data):

    parameters = [
        "username",
        "first_name",
        "last_name",
        "email",
        "date_of_birth",
        "profile_pic",
        "password",
        "cnfrmpass"
    ]

    if not AllFieldsPersent(data,parameters):
        return (False,f"Please provide All the fields: {parameters}")

    # checking username after final submission
    username = data["username"]
    fetchdata = IsUserNameAvailable(username)

    if not fetchdata[0]:
        return (False,fetchdata[1])

    if not iscorrectName(data['first_name']) or not iscorrectName(data["last_name"]):
        return (False,"Name should be Alphabetical no space and other chars min length 3.")

    if not is_validatedPass(data['password'],data['cnfrmpass']):
        return (False,"password and cnfrmpass should be match. min length 8 use a strong password.")

    if not is_validate_smvdu_mail(data['email']):
        return (False,"Please verify you are using smvdu mail id and don't have an account.")

    # date of birth validataion

    if not valid_Date(data["date_of_birth"]):
        return (False,"Invalid Date!!! Format is YYYY-MM-DD where Y is year M is month D is Date")


    # image validation

    # save user and custum user models here

    user = CreateUserAccount(data)
    response,token,cum = CreateCustomUserAccount(user,data)

    subject = f"Welcome {data['first_name']} to Nested.com"

    message = f"Your verification link is\n http://127.0.0.1:8000/verificiation/{token}"

    if response and send_mail(data["email"],subject=subject,message=message):
        return (True,"Data Saved SuccessFully.")
    
    else:
        try:
            user.delete()
            cum.delete()
        except:
            pass
        return (False,"Something went Wrong.")





def AllFieldsPersent(data,params):

    for para in params:
        try:
            some_data = data[para]

        except:
            return False

    return True



def is_already_notified(user):

    year_field_of_user = int(cum.objects.get(index=user).last_email_sent)
    curYear = int(datetime.now().year)

    if year_field_of_user == curYear:
        return True

    else:
        return False




def set_Notified(user):
    cum_obj = cum.objects.get(index=user)
    cum_obj.last_email_sent = int(datetime.now().year)
    cum_obj.save()
    return True


def valid_Date(date):

    if date.count('-')!=2:
        return False
    
    try:
        year,month,day = map(int,date.split('-'))
        cur_year = datetime.now().year

        if cur_year-year>100 or cur_year-year<=12:
            print("pass")
            return False

        if int(month)<1 or int(month)>12:
            return False
        if int(day)< 1 or int(day)>31:
            return False

    except:
        return False


    return True