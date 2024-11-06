from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            
        except UserModel.DoesNotExist:
            return None
        else:
            #print(password)
            if user.check_password(password):
                print(password)
                return user
        return None