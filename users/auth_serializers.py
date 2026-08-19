from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class SignInSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True)

    def validate(self,attrs):
        email=attrs.get("email")
        password=attrs.get("password")
        user=authenticate(
            request=self.context.get("request"),username=email,password=password
        )
        if user is None:
            raise serializers.ValidationError("Invalid email or password")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive")
        
        attrs["user"]=user

        return attrs
    
    def create(self,validated_data):
        user=validated_data["user"]
        refresh_token=RefreshToken.for_user(user)
        return {"refresh":str(refresh_token),"access":str(refresh_token.access_token)}