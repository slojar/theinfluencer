from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse

from rest_framework import generics, permissions, status, views
from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response

from .utils import get_user_detail, update_user_profile
from .serializers import ProfileSerializer, Profile


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        uid = request.data.get('uid')
        access_token = request.data.get('access_token')

        if not (uid and access_token):
            return Response({'detail': 'uid and access_token are required parameters'},
                            status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(username=uid)
        user.password = make_password(access_token)
        user.save()

        user = authenticate(request, username=uid, password=access_token)

        try:
            if user and user.is_active:
                login(request, user)
                response = get_user_detail(uid, access_token)
                update_user_profile(response, user)

                data = {
                    "detail": "Login successful",
                    "email": user.email,
                    "token": str(AccessToken.for_user(user)),
                    "user_data": ProfileSerializer(Profile.objects.get(user=user)).data
                }
                return Response(data)
        except Exception as err:
            return Response({'detail': 'An error has occurred', 'error_message': str(err)},
                            status=status.HTTP_400_BAD_REQUEST)


class HomeView(views.APIView):
    permission_classes = []

    def get(self, request):
        return HttpResponse('<p style="text-align:center"><span style="font-size:72px"><span style="color:#3498db">'
                            '<strong>Welcome to Influencer!!!</strong></span></span></p>')







