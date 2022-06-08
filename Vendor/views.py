from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import *
from django.contrib.auth.hashers import make_password, check_password
from Vendor.serializer import *
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken
from Vendor.models import *


def generateToken(username):
    user = User.objects.get(username=username)
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserSignUp(APIView):
    def post(self, req):
        details = req.data
        _user = {
            'username': details['username'],
            'password': make_password(details['password']),
            'is_superuser': False,
            'first_name': details['first_name'],
            'last_name': details['last_name'],
            'email': details['email'],
            'is_staff': False,
            'is_active': True,
            'date_joined': date.today(),
            'phone': details['phone']
        }
        SerializedUser = UserSerializer(data=_user)
        if SerializedUser.is_valid():
            SerializedUser.save()
            token = generateToken(details['username'])
            return Response({'msg': "true", 'token': token})
        else:
            return Response({'msg': "false", "error": SerializedUser.errors})
