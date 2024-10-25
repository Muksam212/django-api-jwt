from rest_framework import serializers
from users.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ("username", "email", "password", "confirm_password")
        extra_kwargs = {
            "password":{"write_only":True}
        }

    def validated(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"Error":"Password didn't match"})
        return attrs
    
    
    def create(self, validated_data):
        validated_data.pop("confirm_password", None)

        user = User.objects.create_user(**validated_data)
        return user
    

class UserListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = User
        fields = ("id","username", "email")



class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ("username", "password")


class UserProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    class Meta:
        model = User
        fields = ("id","username","email")


class UserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required = True)
    confirm_password = serializers.CharField(write_only = True, required = True)
    old_password = serializers.CharField(write_only = True, required = True)
    class Meta:
        model = User
        fields = ("password", "confirm_password", "old_password")