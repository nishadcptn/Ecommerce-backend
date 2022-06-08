
from django.urls import path
from Vendor.views import *

urlpatterns = [
    path('signup', UserSignUp.as_view(), name='signup'),
]
