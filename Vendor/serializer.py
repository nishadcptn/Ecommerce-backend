from rest_framework import routers, serializers, viewsets
from Vendor import models

# Serializers define the API representation.


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "password", "is_superuser", "first_name",
                  "last_name", "email", "is_staff", "is_active", "phone"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Organization
        fields = '__all__'


class OrgMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationMember
        fields = '__all__'
