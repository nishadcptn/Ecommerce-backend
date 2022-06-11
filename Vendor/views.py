import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import *
from django.contrib.auth.hashers import make_password, check_password
from Vendor.serializer import *
from datetime import date
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from Vendor.models import *
import pyrebase
import os
import time
from django.core.files.storage import default_storage

firebaseConfig = {
    "apiKey": "AIzaSyDzchysqA4fiCS64Msaf-Qp8rlG6Rgz0jY",
    "authDomain": "shopy-web-dev.firebaseapp.com",
    "projectId": "shopy-web-dev",
    "storageBucket": "shopy-web-dev.appspot.com",
    "messagingSenderId": "270017414316",
    "appId": "1:270017414316:web:a5e34c00ca252abea24b09",
    "measurementId": "G-ZT1C96YV3R",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()


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


class OrganizationAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, req):
        _org = {
            "name": req.data["name"],
            "type": req.data["type"],
            "user_count": 0,
            "address": req.data["address"],
            "pin": req.data["pin"],
            "phone": req.data["phone"],
            "email": req.data["email"]
        }
        file = req.data["logo"]
        filename = str(time.time()) + str(uuid.uuid4())
        data = storage.child("files/org/" + filename).put(file)
        if data["name"] and data["downloadTokens"]:
            _org["logo"] = "org%2F" + filename
            _serializer = OrganizationSerializer(data=_org)
            if _serializer.is_valid():
                _serializer.save()
                print(_serializer.data["uuid"])
                member_data = {
                    "organization": _serializer.data["uuid"],
                    "user": req.user.id,
                    "user_type": "admin"
                }
                _memberSerializer = OrgMemberSerializer(data=member_data)
                if _memberSerializer.is_valid():
                    _memberSerializer.save()
                    return Response({"msg": "true"})
                else:
                    return Response({'msg': "false", "error": _memberSerializer.errors})
            else:
                return Response({'msg': "false", "error": _serializer.errors})
        else:
            return Response({'msg': "false", "error": "image upload filed"})
