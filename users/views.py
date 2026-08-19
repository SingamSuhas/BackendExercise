from rest_framework.generics import (ListCreateAPIView,RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import User
from .pagination import UserCursorPagination
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .auth_serializers import SignInSerializer
# Create your views here.

class UserListCreateView(ListCreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    pagination_class=UserCursorPagination

    def get_permissions(self):
        if self.request.method=="POST":
            return[AllowAny()]
        else:
            return[IsAuthenticated()]

class UserRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated]

class SignInView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        serializer=SignInSerializer(data=request.data,context={"request":request,},)
        serializer.is_valid(raise_exception=True)
        tokens=serializer.save()
        return Response(tokens,status=status.HTTP_200_OK)

class SignOutView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        refresh_token=request.data.get("refresh")
        if not refresh_token:
            return Response({"detail":"From Signout Refresh token required"},status=status.HTTP_400_BAD_REQUEST,)

        try:
            token=RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response({"detail":"Invalid or Expired Token."},status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail":"Successfully signed out"},status=status.HTTP_200_OK)
