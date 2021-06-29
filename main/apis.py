from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .custom_validation import *
from django.contrib.auth.models import User
from .models import CustomUserModel as cum
from random import choice
import smtplib
from email.message import EmailMessage
from django.conf import settings




# authentication_classes = [SessionAuthentication, BasicAuthentication]
# permission_classes = [IsAuthenticated]
# put inside the class where need authentication



#initial declaring class will overwrite in views.py if required

class LoginAPI(APIView):
    def post(self,request):
        data = request.data
        response_ = is_valid_credentials(data)
        if response_[0]:
            return Response({'status':200,'message':'Request Granted.'})
        else:
            return Response({'status':404,'message':response_[1]})




class SignUpAPI(APIView):
    def post(self,request):
        data = request.data
        response_ = MainDataChecker(data)
        if response_[0]:
            return Response({'status':200,'message':'Request Granted.','payload':data})
        else:
            return Response({'status':404,'message':response_[1],'payload':data})





class CheckForUsername(APIView):   
    def post(self,request):
        try:
            username = request.data["username"]
        except:
            return Response({'status':404,'message':'Please Provide Username Field for this.'})
        data = IsUserNameAvailable(username)
        if data[0]:
            return Response({'status':200,'message':data[1],'username':username})
        else:
            return Response({'status':404,"message":data[1],"username":username})






class HomePageAPiData(APIView):
    def get(self,request):
        # returns data that will show on home page
        pass





class PersonalDataApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        cum_data = cum.objects.get(index=user)
        # user Data
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        dob = cum_data.date_of_birth
        profile_pic = str(cum_data.profile_pic)
        returnable_obj = {
            "first_name":first_name,
            "last_name":last_name,
            "email":email,
            "dob":dob,
            "pic":profile_pic
        }
        return Response({'status':200,'message':'success','payload':returnable_obj})




class ForgotPassAPI(APIView):

    def get(self,request):
        try:
            username = request.data["username"]
            email = request.data["email"]
            try:
                user = User.objects.get(username=username,email=email)
                cum_ = cum.objects.get(index=user)
                if cum_.is_verified:
                    if not cum_.password_Reseted:
                        user_pass = passwordManager()
                        password = user_pass.passwordGenerator()
                        if user_pass.mailer(password,email):
                            cum_.password_Reseted = True
                            cum_.save()
                            user.set_password(password)
                            user.save()
                            return Response({'status':200,'message':'Your New password is mailed to you.'})
                        else:
                            return Response({'status':500,'message':'server Error..'}) 
                    else:
                        return Response({'status':404,'message':'Sorry You already Reseted Your Password please check mails.'})
                else:
                    return Response({'status':404,'message':'You are Not Authenticated please verify your account.'})
            except:
                # no user exists
                return Response({'status':404,'message':'user not found.'})
        except:
            return Response({'status':404,'message':'Please Provide username and email'})




class passwordManager:


    def mailer(self,password,to,subject=None,message=None,not_bulk=True):
        sender_mail = settings.EMAIL_SENDER   
        password_sender = settings.EMAIL_PASS

        messageEX = EmailMessage()
        if not_bulk:
            messageEX['To'] = to
        else:
            messageEX['Bcc'] = to
        messageEX['From'] = sender_mail
        if subject == None:
            messageEX['Subject'] = "Welcome User to Nested.com"
        else:
            messageEX['Subject'] = subject
        if message == None:
            messageEX.set_content(f"Hello User welcome to Nested.com Your password is {password}. \n \n \n You are not allowed to change this again.\n \n \n Regards\n Nested.com")
        else:
            messageEX.set_content(message)
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_mail, password_sender)
            server.send_message(messageEX)
            return True
        except Exception as e:
            return False



    def passwordGenerator(self):
        upper_case = [chr(i) for i in range(65,91)]
        lower_case = [chr(i) for i in range(97,123)]
        digits = [str(i) for i in range(0,10)]
        Garbage = ['!','#','$','&','~']
        password_length = choice([i for i in range(10,18)])
        Generated_Password = ''
        for i in range(password_length):
            Generated_Password += choice(choice([upper_case,lower_case,digits,Garbage]))
        return Generated_Password


class TokenVerifier(APIView):

    def get(self,request,token):


        try:
            user = User.objects.get(email=request.data["email"])
        except:
            return Response({'status':404,'message':'Please Provide correct email.'})


        try:
            _cum_ = cum.objects.get(auth_token=token)

            if cum.objects.get(index=user).auth_token != _cum_.auth_token:
                return Response({'status':500,'message':'Validation Failed due to incorrect Email.'})

            if _cum_.is_verified:
                return Response({'status':200,'message':'User Already Verified.','Token':token})

            else:
                _cum_.is_verified = True
                _cum_.save()
                return Response({'status':200,'message':'Received Request.','Token':token})
                
        except:
            return Response({'status':404,'message':'User Not Exists.'})