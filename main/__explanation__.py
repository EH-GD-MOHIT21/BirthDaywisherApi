############################################################################################################
####                                                                                                    ####
####                ###################################################################                 ####
####                Debug is True in settings.py also secrect key is visible change it.                 ####
####                ###################################################################                 ####
####                                                                                                    ####
############################################################################################################


'''

    This File Contains the main branching of Code Directory with Explanations of Functionality..

    |

    | main             ->


                        |   migrations/ -> # Migrations Directory Django Provided


                        |   __init__.py -> # Default Django Provided


                        |   __explanation__.py -> # Explanation of file system.


                        |   accounts.py -> # creating models object and saving them.


                        |   admin.py -> # Registering models customizing admin panel


                        |   apis.py -> # contains all base/permanent classes of all apies


                        |   apps.py -> # Default Django Provided


                        |   custom_serializers.py -> # Custom serializer for homePageData


                        |   custom_validation.py -> # verification of Data 


                        |   models.py -> # Database models/Tables


                        |   notify.py -> # If someone has birthday and want to notify others via mail.
                        

                        |   postman.py -> # logic to send mail(There is same method available in ForgotPassApi in apis.py Due to circular import error implemented this.)
                        

                        |   tests.py -> # Default Django Provided
                        

                        |   urls.py -> # managing urls of app
                        

                        |   views.py -> # contains all views/importing all apis allocating to urls overriding some APIS 





    | manager          ->


                        |   __init__.py -> # Default Django Provided


                        |   asgi.py     -> # Default Django Provided


                        |   settings.py -> # Project settings and all personal Datas/configurations


                        |   urls.py     -> # Project Level urls.py


                        |   wsgi.py     -> # Default Django Provided






    | media/imgs       ->   Server Files/imgs will be uploaded Here





    | manage.py        ->   Default Django Provided






    | db.sqlite3       ->   Temporary Database Django Provided Can Update to Any other using configurations in settings.py





    | Procfile         ->   Declares Type of web app when'll host at heroku.






    | requirements.txt ->   All External modules used to build this. 






'''