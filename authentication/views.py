import json
from .forms import ProfileForm, UserForm
from django.db import transaction, IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import User


# Create your views here.

class Auth(APIView):
    @transaction.atomic
    def post(self, request):
        saved_profile = None
        saved_user = None
        try:
            data = json.loads(request.body)

            userData = {
                "first_name": data['firstname'],
                "last_name": data['lastname'],
                "email": data['email'],
                "password": data['password']
            }
            profileData = {
                "phone": data['phone'],
                "address": data['address'],
                "country": data['country'],
                "position": data['position'],
                "gender": data['gender']
            }

            user = UserForm(userData)
            if user.is_valid():
                saved_user = User.objects.create(email=user.cleaned_data['email'],
                                                 first_name=user.cleaned_data['first_name'],
                                                 last_name=user.cleaned_data['last_name'],
                                                 password=user.cleaned_data['password'])
            profile = ProfileForm(profileData)
            if profile.is_valid():
                saved_profile = profile.save(commit=False)
                saved_profile.user = saved_user
                saved_profile.save()
            return Response({"status":'success', "id":saved_profile.id}, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"status": 'failed', "code":"email_exist", "msg": str(e)},
                            status=status.HTTP_208_ALREADY_REPORTED)
        except Exception as e:
            return Response({"status": 'failed', "code": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

