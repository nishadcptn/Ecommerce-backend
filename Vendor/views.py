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
import environ

env = environ.Env()
environ.Env.read_env()

firebaseConfig = {
    "apiKey": env('API_KEY'),
    "authDomain": env('AUTH_DOMAIN'),
    "projectId": env('PROJECT_ID'),
    "storageBucket": env('STORAGE_BUCKET'),
    "messagingSenderId": env('MESSAGING_SENDER_ID'),
    "appId": env('APP_ID'),
    "measurementId": env('MEASURMENT_ID'),
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
        SerializedUser = UserSerializer(data=req.data)
        if SerializedUser.is_valid():
            SerializedUser.save()
            token = generateToken(req.data['username'])
            return Response({'msg': True, 'token': token})
        else:
            return Response({'msg': False, "error": SerializedUser.errors})


class OrganizationAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, req):
        details = req.data
        file = req.data["logo"]
        filename = str(time.time()) + str(uuid.uuid4())
        data = storage.child("files/org/" + filename).put(file)
        if data["name"] and data["downloadTokens"]:
            details["logo"] = "org%2F" + filename
            _serializer = OrganizationSerializer(data=details)
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
                    return Response({"msg": True})
                else:
                    return Response({'msg': False, "error": _memberSerializer.errors})
            else:
                return Response({'msg': False, "error": _serializer.errors})
        else:
            return Response({'msg': False, "error": "image upload filed"})
