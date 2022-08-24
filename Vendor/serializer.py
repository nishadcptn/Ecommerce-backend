from rest_framework import routers, serializers, viewsets
from Vendor import models
from datetime import date
from django.contrib.auth.hashers import make_password
# Serializers define the API representation.


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,)

    class Meta:
        model = models.User
        fields = ["username", "password", "is_superuser", "first_name",
                  "last_name", "email", "is_staff", "is_active", "phone"]

        def create(self, validated_data):
            validated_data['password'] = make_password(
                validated_data.get('password'))
            validated_data['is_superuser'] = False
            validated_data['user_count'] = False
            validated_data['is_active'] = False
            validated_data['date_joined'] = date.today()
            return super(UserSerializer, self).create(validated_data)


class OrganizationSerializer(serializers.ModelSerializer):
    user_count = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:
        model = models.Organization
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user_count'] = 0
        return super(OrganizationSerializer, self).create(validated_data)


class OrgMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationMember
        fields = '__all__'


class AddOrgMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationMember
        fields = ('organization', 'email', 'added_by')
