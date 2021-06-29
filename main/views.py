from django.shortcuts import render
from .apis import *
from .models import CustomUserModel as cum
from .custom_serializers import HomePageSerializer
from .notify import *
from .custom_validation import is_already_notified , set_Notified


# over riding apis.py HomePageAPiData
class HomePageAPiData(APIView):
    
    def get(self,request):
        return HomePageSerializer()



class Birthdaymailer(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if cum.objects.get(index=request.user).is_verified:
            fetchedData = HomePageSerializer(homecall=True)
            if type(fetchedData) == type("d"):
                return Response({'status':404,'warning':'permission Denied.'})
            else:
                for index,data in enumerate(fetchedData):
                    if request.user.username == fetchedData[index]["username"]:
                        # notify others code here
                        if not is_already_notified(request.user):
                            try:
                                notify(request.user.username,request.user.email)
                                set_Notified(request.user)
                                return Response({'status':200,'data':fetchedData[index],'email_status':'sent'})
                            except:
                                return Response({'status':404,'message':'Server Error Occured..'})
                        else:
                            return Response({'status':404,'message':'You already Notified all about your birthday.'})
                return Response({'status':404,'warning':'You Need Permissions.'})
        else:
            return Response({'status':404,'message':'You are not authenticated please verify your account using provided link on email.'})