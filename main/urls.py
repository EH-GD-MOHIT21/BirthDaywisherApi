from django.urls import path
from .views import *


urlpatterns = [
    path('login',LoginAPI.as_view()),
    path('signup',SignUpAPI.as_view()),
    path('profile',PersonalDataApiView.as_view()),
    path('',HomePageAPiData.as_view()),
    path('forgot',ForgotPassAPI.as_view()),
    path('checkuser',CheckForUsername.as_view()),
    path('bmailer',Birthdaymailer.as_view()),
    path('verification/<token>',TokenVerifier.as_view())
]