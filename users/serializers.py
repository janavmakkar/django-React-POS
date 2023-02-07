from rest_framework import serializers
from .models import User,Permission,Role

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Permission
        fields='__all__'

class PermissionRelatedSerializer(serializers.StringRelatedField):
    # function to how to show data from db(show whole object, instead of permission id's)
    def to_representation(self, value):
        return PermissionSerializer(value).data

    # function to how to save data in db while creating a new Role
    # (save permission id's, instead asking for whole permission object)
    def to_internal_value(self, data):
        return data

class RoleSerializer(serializers.ModelSerializer):
    permissions=PermissionRelatedSerializer(many=True)
    class Meta:
        model=Role
        fields='__all__'
