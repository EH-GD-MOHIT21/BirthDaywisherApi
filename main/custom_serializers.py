from datetime import datetime,timedelta
from .models import CustomUserModel as cum,User
from rest_framework.response import Response



def HomePageSerializer(homecall=False):
    Results = User.objects.all()
    main_data = {}
    cntr = 0
    for index,user in enumerate(Results):
        data = {}
        data["username"] = str(user.username)
        data[f"first_name"] = str(user.first_name)
        data[f"last_name"] = str(user.last_name)
        data[f"email"] = str(user.email)


        # logic used

        #_____________________________________________________________________
        '''
            Replacing users dateofbirth corresponds to current year to locate 
            his dateofbirth is near to x days from today.
            Here the replacing is temporary we aren't saving them.
        '''
        #______________________________________________________________________


        personal = cum.objects.get(index=user)
        dob_user = personal.date_of_birth.replace(year=datetime.now().year)
        data[f"date_of_birth"] = str(personal.date_of_birth)
        data[f"profile_pic"] = str(personal.profile_pic)

        cur_date = datetime.now().date()

        # till we want to see results default 7 days ahead
        upto_days = cur_date + timedelta(days=7)

        if dob_user >= cur_date and dob_user <= upto_days:
            main_data[cntr] = data
            cntr +=1
            
    if not len(main_data):
        main_data = "Sorry No user Have Their BirthDay in Next 30 Days."
            
    if not homecall:
        return Response({'status':200,'payload':main_data})
    else:
        return main_data
