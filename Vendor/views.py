from cmath import exp
import json
from lib2to3.pgen2 import token
from pickle import TRUE
import re
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import *
from django.contrib.auth.hashers import make_password, check_password
from Vendor.serializer import *
from datetime import date, datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from Vendor.models import *
import pyrebase
import os
import time
from django.core.files.storage import default_storage
import environ
import string
import random
from django.contrib.auth.decorators import user_passes_test
from jose import jwt
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
    access_token = refresh.access_token
    access_token.set_exp(lifetime=timedelta(days=10))

    return {
        'refresh': str(refresh),
        'access': str(access_token),
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


class AddOrganizationMember(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, req):
        email = req.data.get('email')
        org = req.data.get('organization')
        is_exists = OrganizationMember.objects.filter(
            email=email, organization=org)
        if is_exists:
            expiry = datetime.now() + timedelta(hours=1)
            _member = {
                'email': email,
                'added_by': req.user.id,
                'organization': org,
                'expiry': str(expiry)
            }
            token = jwt.encode(_member, env('JWT_SECRET'), algorithm='HS256')
            "SEND EMAIL WITH TOKENN"
            return Response({'success': True})
        _member = {
            'email': email,
            'added_by': req.user.id,
            'organization': org
        }
        _serializer = AddOrgMemberSerializer(data=_member)
        if _serializer.is_valid():
            _serializer.save()
            expiry = datetime.now() + timedelta(hours=1)
            _member['expiry'] = str(expiry)
            token = jwt.encode(_member, env('JWT_SECRET'), algorithm='HS256')
            "SEND EMAIL WITH TOKENN"
            return Response({'success': True})
        return Response({'success': False, 'error': _serializer.errors})
