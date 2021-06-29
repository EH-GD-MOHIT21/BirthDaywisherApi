from django.db import models
from django.contrib.auth.models import User
from random import choice

# Create your models here.

class CustomUserModel(models.Model):
    index               =   models.OneToOneField(User,on_delete=models.CASCADE)
    date_of_birth       =   models.DateField()
    profile_pic         =   models.ImageField(upload_to='imgs')
    last_email_sent     =   models.IntegerField(default=0)
    auth_token          =   models.CharField(max_length=40,null=True,blank=True)
    password_Reseted    =   models.BooleanField(default=False)
    is_verified         =   models.BooleanField(default=False)
    
    

    def __str__(self):
        return self.index.first_name + " " + self.index.last_name + " " + str(self.date_of_birth)

    @property
    def authGenerator(self):
        key = ""
        allowlist = [chr(i) for i in range(65,91)] + [chr(i) for i in range(97,123)] + [str(i) for i in range(0,10)]
        for i in range(15):
            key += choice(allowlist)

        return key + self.index.username


#last email sent denotes when the last birthday wisher email (in which year) was sent.
#it can be sent only once per birth day and per user.